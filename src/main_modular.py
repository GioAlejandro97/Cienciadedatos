"""
Script principal: main_modular.py
Propósito: Integrar módulos externos (NumPy, SciPy, Joblib) para el análisis.
"""
import sys
from pathlib import Path

# Garantiza que Python reconozca los módulos de la carpeta src
sys.path.append(str(Path(__file__).resolve().parent))

import pandas as pd
from stats_engine import (
    calcular_metricas_vectorizadas,
    detectar_anomalias_zscore,
    ejecutar_anova_regiones,
)
from model_persistence import guardar_objeto, cargar_objeto


def ejecutar_pipeline_modular():
    # Buscar el dataset en data/raw o en la raíz
    ruta_dataset = Path("data/raw/dataset_set_D_telecomunicaciones.xlsx")
    if not ruta_dataset.exists():
        ruta_dataset = Path("dataset_set_D_telecomunicaciones.xlsx")

    if not ruta_dataset.exists():
        print(f"[Error] No se encontró el dataset en {ruta_dataset}")
        return

    print("=== 1. CARGA DE DATOS ===")
    df = pd.read_excel(ruta_dataset)
    print(f"Registros leídos: {len(df)}")

    print("\n=== 2. CÁLCULO DE MÉTRICAS VECTORIZADAS (NumPy) ===")
    metricas_latencia = calcular_metricas_vectorizadas(df["latencia_ms"])
    metricas_resolucion = calcular_metricas_vectorizadas(df["tiempo_resolucion_hr"])

    print(f"Latencia (ms)  -> Media: {metricas_latencia['media']:.2f} | Mediana: {metricas_latencia['mediana']:.2f} | IQR: {metricas_latencia['iqr']:.2f}")
    print(f"Resolución (hr) -> Media: {metricas_resolucion['media']:.2f} | Mediana: {metricas_resolucion['mediana']:.2f} | IQR: {metricas_resolucion['iqr']:.2f}")

    print("\n=== 3. PRUEBAS DE HIPÓTESIS Y ANOMALÍAS (SciPy) ===")
    f_lat, p_lat, conc_lat = ejecutar_anova_regiones(df, "latencia_ms")
    print(f"ANOVA Latencia por Región: F = {f_lat:.4f}, p = {p_lat:.4f}")
    print(f"Resultado: {conc_lat}")

    f_res, p_res, conc_res = ejecutar_anova_regiones(df, "tiempo_resolucion_hr")
    print(f"ANOVA Resolución por Región: F = {f_res:.4f}, p = {p_res:.4f}")
    print(f"Resultado: {conc_res}")

    anomalias_lat = detectar_anomalias_zscore(df, "latencia_ms", umbral_z=2.5)
    print(f"Alertas de latencia crítica (|Z| > 2.5): {len(anomalias_lat)} casos")

    print("\n=== 4. SERIALIZACIÓN Y PERSISTENCIA (Joblib) ===")
    baseline_operacional = {
        "version": "1.0.0",
        "metricas_latencia": metricas_latencia,
        "metricas_resolucion": metricas_resolucion,
        "anova_resolucion": {"f_stat": f_res, "p_valor": p_res},
        "tasa_cumplimiento_historica": float((df["cumplimiento_sla"] == "Cumple").mean()),
    }

    ruta_modelo = "models/baseline_operacional.joblib"
    guardar_objeto(baseline_operacional, ruta_modelo)

    recuperado = cargar_objeto(ruta_modelo)
    print(f"Validación post-carga: Tasa SLA en baseline = {recuperado['tasa_cumplimiento_historica']*100:.1f}%")


if __name__ == "__main__":
    ejecutar_pipeline_modular()