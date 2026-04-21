# Analisis de Rentabilidad y Retencion en E-commerce

Este proyecto lo arme pensando en el tipo de caso que de verdad me gustaria conversar en una entrevista. No queria hacer solo un analisis bonito o una coleccion de graficos. Queria trabajar sobre una situacion de negocio que se siente real: una empresa vende mas, pero no necesariamente gana mejor.

En muchos equipos de e-commerce pasa algo parecido. El volumen crece, pero el margen sigue bajo presion. Algunas campañas traen pedidos, aunque no siempre dejan buena utilidad. Algunas categorias parecen fuertes en ventas, pero generan demasiadas devoluciones. Y no todos los clientes que se adquieren terminan convirtiendose en clientes recurrentes.

La idea de este proyecto fue bajar ese problema a datos y responderlo con una mirada de negocio, no solo tecnica.

## Que problema intenta resolver

La pregunta de fondo es simple: como puede crecer un e-commerce sin deteriorar la calidad de sus ingresos?

Para aterrizarla mejor, trabaje sobre tres preguntas:

1. Que segmentos de clientes generan mas valor y cuales estan mas cerca de abandonar?
2. Que canales y categorias ayudan a crecer en ventas, pero castigan la rentabilidad?
3. Que decisiones tendrian mas sentido si el objetivo fuera mejorar retencion, margen y eficiencia comercial al mismo tiempo?

## Que incluye el proyecto

- un generador de datos sinteticos para simular un caso de negocio consistente
- un flujo de limpieza y analisis en Python
- consultas SQL orientadas a preguntas de negocio
- una API en FastAPI para exponer resultados
- una vista web simple
- un dashboard en Streamlit con lectura ejecutiva, insights y recomendaciones
- un notebook en español para contar mejor la historia del analisis

## Stack

- `Python`
- `Pandas`
- `SQL`
- `FastAPI`
- `Streamlit`
- `Plotly`

## Estructura

```text
.
|-- data
|   |-- processed
|   `-- raw
|-- notebooks
|   `-- ecommerce_storytelling_es.ipynb
|-- outputs
|   |-- charts
|   `-- tables
|-- sql
|   |-- business_queries.sql
|   `-- schema.sql
|-- src
|   |-- analyze_ecommerce.py
|   |-- app.py
|   `-- generate_sample_data.py
|-- templates
|   `-- index.html
|-- .streamlit
|   `-- config.toml
|-- render.yaml
|-- requirements.txt
`-- streamlit_app.py
```

## Como correrlo

Primero instala dependencias y genera los datos:

```bash
python -m pip install -r requirements.txt
python src/generate_sample_data.py
python src/analyze_ecommerce.py
```

Si quieres levantar la API:

```bash
python -m uvicorn src.app:app --reload
```

Si quieres abrir el dashboard:

```bash
python -m streamlit run streamlit_app.py
```

## Rutas utiles

API:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/api/summary`
- `http://127.0.0.1:8000/api/channels`
- `http://127.0.0.1:8000/api/categories`
- `http://127.0.0.1:8000/api/rfm`

Dashboard:

- `http://localhost:8501`

## Que salidas genera

Despues de correr el analisis, el proyecto deja:

- una tabla limpia a nivel transaccional
- KPIs ejecutivos
- desempeno por canal
- desempeno por categoria
- segmentacion RFM
- graficos listos para compartir

## Que tipo de lectura permite

Mas que responder "cuanto se vendio", este proyecto ayuda a conversar cosas como:

- si el crecimiento viene acompañado de buena rentabilidad o no
- que canales estan sosteniendo mejor el negocio
- donde los descuentos o las devoluciones se comen el margen
- que clientes conviene proteger, escalar o reactivar

## Por que me gusta como proyecto de portafolio

Porque no se queda solo en codigo. Tiene una historia clara. Parte de un problema entendible, construye una lectura analitica y termina en decisiones razonables. Tambien me gusta porque mezcla varias capas del trabajo de analisis: datos, negocio, comunicacion y visualizacion.

## Notebook en espanol

Tambien deje un notebook para contar el caso con mas calma:

- `notebooks/ecommerce_storytelling_es.ipynb`

Ese notebook me parece util cuando quiero presentar el proyecto de forma mas guiada, sobre todo si la conversacion va mas por el lado del razonamiento que por el producto final.

## Despliegue

El repo ya viene preparado para desplegar la API en Render con `render.yaml`.

Configuracion usada:

- Build Command: `pip install -r requirements.txt && python src/generate_sample_data.py && python src/analyze_ecommerce.py`
- Start Command: `uvicorn src.app:app --host 0.0.0.0 --port $PORT`

## Cierre

Si tuviera que resumir este proyecto en una linea, diria esto: es un intento de mostrar como llevar un problema comercial bastante cotidiano a una conversacion analitica mas clara, mas accionable y mas cercana a como realmente se toman decisiones.
