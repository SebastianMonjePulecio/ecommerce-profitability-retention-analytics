# Análisis de Rentabilidad y Retención en E-commerce

Este proyecto fue construido como un caso de portafolio enfocado en un problema muy común en e-commerce: la empresa vende más, pero la rentabilidad no mejora al mismo ritmo. El objetivo no es solo reportar ventas, sino entender qué está afectando el margen, qué canales realmente aportan valor y dónde se están perdiendo oportunidades de retención.

## Contexto del negocio

El escenario es realista y fácil de explicar en una entrevista. Una empresa de e-commerce está creciendo, pero el equipo comercial empieza a notar señales de alerta: presión sobre el margen, devoluciones altas y una dependencia excesiva de descuentos para sostener el volumen. Algunos canales traen pedidos, pero no suficiente utilidad. Algunas categorías venden bien, pero generan costos altos por devoluciones. Además, no todos los clientes adquiridos vuelven a comprar.

La idea del proyecto es abordar el problema como lo haría un Senior Data Analyst: partir del dolor del negocio, traducirlo en preguntas medibles y terminar con recomendaciones accionables.

## Preguntas de negocio

1. ¿Qué segmentos de clientes generan más valor en el tiempo y cuáles tienen mayor riesgo de abandono?
2. ¿Qué canales y categorías ayudan a crecer en ventas, pero perjudican la rentabilidad?
3. ¿Qué acciones podrían mejorar la retención, reducir ineficiencias y aumentar el ingreso neto?

## Stack tecnológico

- `SQL` para consultas de negocio y cálculo de KPIs
- `Python` para generación de datos, limpieza, análisis exploratorio y segmentación RFM
- `FastAPI` para exponer resultados en un endpoint y una vista web simple
- `Power BI` o `Tableau` como siguiente paso para dashboard ejecutivo

## Estructura del proyecto

```text
.
|-- data
|   |-- processed
|   `-- raw
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
|-- .gitignore
|-- README.md
`-- requirements.txt
```

## Cómo ejecutarlo

1. Instala las dependencias.
2. Genera el dataset sintético.
3. Corre el análisis.
4. Levanta la API para ver los resultados.

```bash
python -m pip install -r requirements.txt
python src/generate_sample_data.py
python src/analyze_ecommerce.py
python -m uvicorn src.app:app --reload
```

Cuando el servidor esté arriba, abre:

- `http://127.0.0.1:8000/` para ver la vista web
- `http://127.0.0.1:8000/api/summary` para ver los KPIs
- `http://127.0.0.1:8000/api/channels` para ver desempeño por canal
- `http://127.0.0.1:8000/api/categories` para ver desempeño por categoría
- `http://127.0.0.1:8000/api/rfm` para ver segmentación de clientes

## Salidas del análisis

Después de correr los scripts, el proyecto genera:

- datos limpios a nivel transaccional en `data/processed`
- tablas de KPIs en `outputs/tables`
- gráficos listos para compartir en `outputs/charts`
- un archivo de segmentación RFM para dashboard o storytelling

## KPIs incluidos

- ingreso neto
- utilidad bruta
- porcentaje de margen bruto
- ticket promedio
- tasa de recompra
- tasa de devoluciones
- intensidad de descuento
- ROAS por canal

## Valor estratégico

Este análisis ayuda a tomar decisiones como:

- reasignar inversión hacia canales con mejor aporte a utilidad
- reducir descuentos agresivos donde no son necesarios
- priorizar campañas de retención para clientes valiosos en riesgo
- revisar categorías con comportamiento anormal en devoluciones

## Por qué funciona bien en portafolio

Este proyecto no solo demuestra manejo de herramientas. También muestra criterio de negocio, capacidad para priorizar y habilidad para traducir datos en decisiones que impactan ingresos, margen y eficiencia operativa.
