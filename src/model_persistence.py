"""Módulo: model_persistence.py.

Propósito: Serialización y deserialización de baselines operacionales
y parámetros analíticos con Joblib.
"""

from pathlib import Path
from typing import Any
import joblib


def guardar_objeto(objeto: Any, ruta_archivo: str) -> None:
  ruta = Path(ruta_archivo)
  ruta.parent.mkdir(parents=True, exist_ok=True)
  joblib.dump(objeto, ruta, compress=3)
  print(f'[Joblib] Objeto serializado con éxito en: {ruta}')


def cargar_objeto(ruta_archivo: str) -> Any:
  ruta = Path(ruta_archivo)
  if not ruta.exists():
    raise FileNotFoundError(f'No se encontró el archivo en la ruta: {ruta}')

  objeto = joblib.load(ruta)
  print(f'[Joblib] Objeto recuperado exitosamente desde: {ruta}')
  return objeto