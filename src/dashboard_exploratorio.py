"""
Módulo: dashboard_exploratorio.py
Propósito: Análisis operacional, construcción de dashboard comparativo
           y generación de reportes para RedConecta Telecom S.A.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def cargar_datos(ruta_archivo: str) -> pd.DataFrame:
  """Carga y valida el dataset de telecomunicaciones."""
  df = pd.read_excel(ruta_archivo)
  df['fecha_registro'] = pd.to_datetime(df['fecha_registro'])
  return df


def generar_archivos_salida(df: pd.DataFrame, ruta_destino: Path):
  """Exporta los datasets especializados para Soporte Técnico y Experiencia de Clientes."""
  ruta_destino.mkdir(parents=True, exist_ok=True)

  # 1. Archivo de salida para Soporte Técnico (foco en infraestructura y resolución)
  df_soporte = df[[
      'fecha_registro',
      'region',
      'tipo_servicio',
      'latencia_ms',
      'tiempo_resolucion_hr',
      'incidencias_reportadas',
      'tickets_soporte',
      'cumplimiento_sla',
  ]].copy()
  ruta_soporte = ruta_destino / 'reporte_soporte_tecnico.csv'
  df_soporte.to_csv(ruta_soporte, index=False, sep=';', encoding='utf-8')
  print(
      f'[OK] Archivo para Soporte Técnico exportado en: {ruta_soporte} (filas:'
      f' {len(df_soporte)})'
  )

  # 2. Archivo de salida para Experiencia de Clientes (foco en impacto e incidencias)
  df_cx = df[[
      'fecha_registro',
      'region',
      'tipo_servicio',
      'clientes_afectados',
      'tickets_soporte',
      'tiempo_resolucion_hr',
      'cumplimiento_sla',
  ]].copy()
  ruta_cx = ruta_destino / 'reporte_experiencia_clientes.csv'
  df_cx.to_csv(ruta_cx, index=False, sep=';', encoding='utf-8')
  print(
      f'[OK] Archivo para Experiencia de Clientes exportado en: {ruta_cx}'
      f' (filas: {len(df_cx)})'
  )


def construir_dashboard(df: pd.DataFrame, ruta_salida_figura: str):
  """Construye e ilustra un dashboard comparativo 2x2 por Región y Tipo de Servicio."""
  sns.set_theme(style='whitegrid')
  fig, axes = plt.subplots(2, 2, figsize=(14, 10))

  # Resumen agrupado
  resumen_region = (
      df.groupby('region')
      .agg(
          cumplimiento_sla=(
              'cumplimiento_sla',
              lambda x: np.mean(x == 'Cumple') * 100,
          )
      )
      .reset_index()
  )

  resumen_servicio = (
      df.groupby('tipo_servicio')
      .agg(
          latencia_media=('latencia_ms', 'mean'),
          clientes_afectados_total=('clientes_afectados', 'sum'),
      )
      .reset_index()
  )

  cruce_region_servicio = (
      df.groupby(['region', 'tipo_servicio'])['tiempo_resolucion_hr']
      .mean()
      .reset_index()
  )

  # Gráfico 1: Cumplimiento SLA por Región
  b1 = sns.barplot(
      data=resumen_region,
      x='region',
      y='cumplimiento_sla',
      palette='Blues_d',
      ax=axes[0, 0],
  )
  axes[0, 0].set_title(
      'Tasa de Cumplimiento SLA por Región (%)', fontsize=12, fontweight='bold'
  )
  axes[0, 0].set_ylim(0, 100)
  axes[0, 0].set_ylabel('% Cumplimiento SLA')
  axes[0, 0].set_xlabel('Región')
  for p in b1.patches:
    axes[0, 0].annotate(
        f'{p.get_height():.1f}%',
        (p.get_x() + p.get_width() / 2.0, p.get_height()),
        ha='center',
        va='center',
        xytext=(0, 6),
        textcoords='offset points',
        fontweight='semibold',
    )

  # Gráfico 2: Latencia Promedio por Tipo de Servicio
  b2 = sns.barplot(
      data=resumen_servicio,
      x='tipo_servicio',
      y='latencia_media',
      palette='Reds_d',
      ax=axes[0, 1],
  )
  axes[0, 1].set_title(
      'Latencia Promedio por Tipo de Servicio (ms)',
      fontsize=12,
      fontweight='bold',
  )
  axes[0, 1].set_ylabel('Latencia (ms)')
  axes[0, 1].set_xlabel('Tipo de Servicio')
  for p in b2.patches:
    axes[0, 1].annotate(
        f'{p.get_height():.1f} ms',
        (p.get_x() + p.get_width() / 2.0, p.get_height()),
        ha='center',
        va='center',
        xytext=(0, 6),
        textcoords='offset points',
        fontweight='semibold',
    )

  # Gráfico 3: Tiempo de Resolución Medio por Región y Tipo de Servicio
  sns.barplot(
      data=cruce_region_servicio,
      x='region',
      y='tiempo_resolucion_hr',
      hue='tipo_servicio',
      palette='viridis',
      ax=axes[1, 0],
  )
  axes[1, 0].set_title(
      'Tiempo de Resolución Medio por Región y Servicio (hrs)',
      fontsize=12,
      fontweight='bold',
  )
  axes[1, 0].set_ylabel('Horas')
  axes[1, 0].set_xlabel('Región')

  # Gráfico 4: Total de Clientes Afectados por Servicio
  b4 = sns.barplot(
      data=resumen_servicio,
      x='tipo_servicio',
      y='clientes_afectados_total',
      palette='Oranges_d',
      ax=axes[1, 1],
  )
  axes[1, 1].set_title(
      'Total Acumulado de Clientes Afectados', fontsize=12, fontweight='bold'
  )
  axes[1, 1].set_ylabel('N° de Clientes')
  axes[1, 1].set_xlabel('Tipo de Servicio')
  for p in b4.patches:
    axes[1, 1].annotate(
        f'{int(p.get_height()):,}',
        (p.get_x() + p.get_width() / 2.0, p.get_height()),
        ha='center',
        va='center',
        xytext=(0, 6),
        textcoords='offset points',
        fontweight='semibold',
    )

  plt.tight_layout()
  plt.savefig(ruta_salida_figura, dpi=300)
  plt.close()
  print(f'[OK] Dashboard guardado en: {ruta_salida_figura}')


if __name__ == '__main__':
  archivo_datos = 'data/raw/dataset_set_D_telecomunicaciones.xlsx'
  df_telecom = cargar_datos(archivo_datos)

  # 1. Exportar reportes operativos
  generar_archivos_salida(df_telecom, Path('./data/processed'))

  # 2. Construir y guardar dashboard
  construir_dashboard(df_telecom, './reports/figures/dashboard_exploratorio.png')