RedConecta Telecom S.A. - Analitica Operacional y Calidad de Servicio

Este proyecto presenta el flujo analitico reproducible desarrollado para RedConecta Telecom S.A., con el proposito de analizar la operacion diaria, diagnosticar problemas de latencia y tiempos de resolucion, y apoyar el cumplimiento de los acuerdos de nivel de servicio (SLA).



1\. Objetivos del Proyecto

Objetivo General:

Evaluar el comportamiento operacional de la red de telecomunicaciones mediante un flujo analitico ordenado y reproducible, identificando cuellos de botella para mejorar el cumplimiento de SLA y reducir el impacto en los clientes.



Objetivos Especificos:



Comparar el rendimiento de la red (latencia y tiempos de resolucion) por region geografica y tipo de servicio.



Cuantificar el volumen acumulado de clientes afectados por incidencias operacionales.



Crear visualizaciones claras para facilitar la toma de decisiones tecnicas y gerenciales.



Generar archivos de datos procesados especificos para las areas de Soporte Tecnico y Experiencia de Clientes.



2\. Descripcion del Conjunto de Datos

El analisis se realiza sobre el archivo dataset\_set\_D\_telecomunicaciones.xlsx, el cual contiene 200 registros diarios entre el 1 de marzo de 2025 y el 16 de septiembre de 2025, sin datos faltantes.



Variables analizadas:



fecha\_registro: Fecha del evento operativo (marzo a septiembre de 2025).



region: Zona geografica (Centro, Norte, Sur).



tipo\_servicio: Linea comercial (Empresas, Internet Hogar, Movil).



trafico\_datos\_gb: Volumen de trafico cursado en gigabytes (entre 50.5 y 497.9 GB).



latencia\_ms: Retardo de la senal en milisegundos (entre 11.2 y 119.9 ms).



incidencias\_reportadas: Fallas tecnicas detectadas en el dia (de 0 a 29).



tickets\_soporte: Solicitudes ingresadas a mesa de ayuda (de 5 a 59).



tiempo\_resolucion\_hr: Horas dedicadas a solucionar las fallas (de 1.2 a 47.2 horas).



clientes\_afectados: Usuarios impactados (de 10 a 499 clientes por registro).



cumplimiento\_sla: Indicador de cumplimiento del acuerdo (Cumple o No cumple).



3\. Metodologia y Flujo de Trabajo

El proyecto organiza el analisis en etapas modulares para que sea auditable y facil de reproducir:



Carga de datos:

Se lee el archivo original en formato Excel y se almacena en la carpeta data/raw sin modificar la fuente original.



Evaluacion de calidad:

Se verifica que las 10 columnas existan, no presenten valores nulos y que los tipos de datos correspondan a fechas, enteros y decimales.



Procesamiento y calculo:

Se calculan promedios, desviaciones estandar y tasas porcentuales de cumplimiento de SLA segmentadas por region y servicio con Pandas y NumPy.



Visualizacion:

Se construye un dashboard comparativo guardado automaticamente en reports/figures en formato de imagen de alta calidad.



Generacion de salidas:

Se exportan dos archivos CSV independientes en data/processed listos para el trabajo operativo de cada area.



4\. Estructura de Carpetas del Proyecto

redconecta/

.gitignore

README.md

requirements.txt

data/

raw/

dataset\_set\_D\_telecomunicaciones.xlsx

processed/

reporte\_soporte\_tecnico.csv

reporte\_experiencia\_clientes.csv

notebooks/

01\_exploracion\_inicial.ipynb

src/

init.py

dashboard\_exploratorio.py

reports/

figures/

dashboard\_exploratorio\_telecom.png



5\. Principales Hallazgos y Resultados

Cumplimiento Global de SLA:

De los 200 dias analizados, el 52% (104 casos) no cumplio la meta de SLA, alcanzando solo un 48% de cumplimiento global.



Comparativa por Regiones:

Region Sur: Obtuvo el mayor cumplimiento de SLA (55.2%) y la menor latencia (61.8 ms), pero presento el tiempo de resolucion de incidencias mas lento (28.2 horas promedio).

Region Centro: Registro el menor cumplimiento (44.1%), la mayor latencia promedio (68.1 ms) y la mayor cantidad de clientes afectados acumulados (18,478).

Region Norte: Mostro un cumplimiento bajo (44.6%) y una latencia promedio de 64.6 ms, pero con tiempos de resolucion mas rapidos (23.2 horas).



Comparativa por Tipo de Servicio:

Internet Hogar: Fue el servicio con mayor trafico total y el que acumulo mas clientes afectados (20,925), teniendo ademas el cumplimiento mas bajo de SLA (46.8%).

Empresas: Tuvo la latencia promedio mas alta de la red (69.2 ms).

Punto critico identificado: Internet Hogar en la Region Sur presento el tiempo promedio de resolucion mas alto, superando las 30.6 horas.



6\. Instrucciones para Ejecutar y Reproducir

Paso 1: Clonar o descargar la carpeta del proyecto y abrir una terminal en la ruta raiz redconecta.



Paso 2: Crear y activar un entorno virtual de Python:



python -m venv venv

.\\venv\\Scripts\\activate



Paso 3: Instalar las dependencias necesarias:

pip install -r requirements.txt



Paso 4: Verificar que el archivo original este en la ruta:

data/raw/dataset\_set\_D\_telecomunicaciones.xlsx



Paso 5: Ejecutar el script analitico:

python src/dashboard\_exploratorio.py



Paso 6: Revisar los resultados generados:

Los reportes estaran en data/processed/ y la imagen del dashboard en reports/figures/.

