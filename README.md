# Analisis de Rentabilidad y Retencion en E-commerce

Este proyecto nace de una situacion bastante comun en e-commerce: la empresa vende mas, pero eso no siempre se traduce en mejor rentabilidad. La idea no fue solo mostrar tecnicas de analisis, sino construir un caso de portafolio que se sienta cercano a un problema real de negocio.

## Contexto del negocio

Una empresa de e-commerce viene creciendo, pero el equipo comercial empieza a notar algunas señales de alerta: margen presionado, devoluciones altas y demasiada dependencia de descuentos para sostener el volumen. Algunos canales traen pedidos, pero no dejan suficiente utilidad. Algunas categorias venden bien, pero generan friccion operativa por devoluciones. Y no todos los clientes que se adquieren vuelven a comprar.

El proyecto esta pensado desde una mirada de analista senior: partir del problema, hacer preguntas utiles y terminar con recomendaciones que podrian defenderse frente a negocio.

## Preguntas de negocio

1. Que segmentos de clientes generan mas valor y cuales muestran mayor riesgo de abandono?
2. Que canales y categorias ayudan a crecer en ventas, pero castigan la rentabilidad?
3. Que decisiones podrian mejorar retencion, eficiencia comercial e ingreso neto?

## Stack tecnologico

- `SQL` para consultas de negocio y calculo de KPIs
- `Python` para generacion de datos, limpieza, analisis exploratorio y segmentacion RFM
- `FastAPI` para exponer resultados en endpoints
- `Streamlit` para un dashboard visual, mas ejecutivo y facil de mostrar

## Estructura del proyecto

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

## Como ejecutarlo

1. Instala dependencias.
2. Genera el dataset sintetico.
3. Corre el analisis.
4. Levanta la API si quieres revisar endpoints.
5. Levanta Streamlit si quieres ver la parte mas visual.

```bash
python -m pip install -r requirements.txt
python src/generate_sample_data.py
python src/analyze_ecommerce.py
```

Para la API:

```bash
python -m uvicorn src.app:app --reload
```

Para el dashboard:

```bash
python -m streamlit run streamlit_app.py
```

## Rutas utiles

Si corres la API:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/api/summary`
- `http://127.0.0.1:8000/api/channels`
- `http://127.0.0.1:8000/api/categories`
- `http://127.0.0.1:8000/api/rfm`

Si corres Streamlit:

- `http://localhost:8501`

## Notebook en espanol

Tambien deje un notebook pensado para contar la historia del proyecto de forma mas clara:

- `notebooks/ecommerce_storytelling_es.ipynb`

Sirve bien para entrevistas porque resume el problema, muestra hallazgos y conecta el analisis con decisiones de negocio sin ponerse demasiado tecnico.

## Despliegue en Render

El repo ya incluye `render.yaml`, asi que se puede desplegar en Render sin demasiada configuracion manual.

Configuracion usada:

- Build Command: `pip install -r requirements.txt && python src/generate_sample_data.py && python src/analyze_ecommerce.py`
- Start Command: `uvicorn src.app:app --host 0.0.0.0 --port $PORT`

## Salidas del analisis

Despues de correr los scripts, el proyecto genera:

- datos limpios en `data/processed`
- tablas de KPIs en `outputs/tables`
- graficos exportados en `outputs/charts`
- segmentacion RFM para storytelling y dashboard

## KPIs incluidos

- ingreso neto
- utilidad bruta
- margen bruto
- ticket promedio
- tasa de recompra
- tasa de devoluciones
- descuento promedio
- ROAS por canal

## Valor del proyecto

Lo que hace fuerte este proyecto no es solo que corre, sino que conecta bien con negocio. Permite hablar de mezcla de canales, calidad del ingreso, devoluciones, eficiencia comercial y retencion de clientes de una forma bastante natural.

## Por que queda mejor asi

Decidi dejar el proyecto mas enfocado en lo que ya estaba funcionando mejor: analisis, notebook, API y dashboard en Streamlit. En vez de abrir demasiados frentes, la idea fue dejar una historia mas limpia y creible.
