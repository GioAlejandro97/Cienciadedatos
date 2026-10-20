"""
Módulo: stats_engine.py
Propósito: Funciones estadísticas vectorizadas y pruebas de hipótesis
           utilizando NumPy y SciPy para redes de telecomunicaciones.
"""
from typing import Dict, Tuple
import numpy as np
import pandas as pd
from scipy import stats


def calcular_metricas_vectorizadas(serie_datos: pd.Series) -> Dict[str, float]:
    valores = np.array(serie_datos.dropna())

    p25 = float(np.percentile(valores, 25))
    p75 = float(np.percentile(valores, 75))

    metricas = {
        "media": float(np.mean(valores)),
        "desviacion_estandar": float(np.std(valores, ddof=1)),
        "mediana": float(np.median(valores)),
        "percentil_25": p25,
        "percentil_75": p75,
        "iqr": float(p75 - p25),
    }
    return metricas


def detectar_anomalias_zscore(df: pd.DataFrame, columna: str, umbral_z: float = 2.5) -> pd.DataFrame:
    z_scores = np.abs(stats.zscore(df[columna]))
    mascara = z_scores > umbral_z

    df_anomalias = df[mascara].copy()
    df_anomalias["z_score"] = z_scores[mascara]
    return df_anomalias


def ejecutar_anova_regiones(df: pd.DataFrame, columna_metrica: str) -> Tuple[float, float, str]:
    grupo_centro = df[df["region"] == "Centro"][columna_metrica]
    grupo_norte = df[df["region"] == "Norte"][columna_metrica]
    grupo_sur = df[df["region"] == "Sur"][columna_metrica]

    f_stat, p_valor = stats.f_oneway(grupo_centro, grupo_norte, grupo_sur)

    if p_valor < 0.05:
        conclusion = f"Diferencias estadísticamente significativas (p = {p_valor:.4f} < 0.05)"
    else:
        conclusion = f"Sin diferencias estadísticamente significativas (p = {p_valor:.4f} >= 0.05)"

    return float(f_stat), float(p_valor), conclusion