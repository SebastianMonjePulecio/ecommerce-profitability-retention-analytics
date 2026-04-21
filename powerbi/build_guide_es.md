# Guía de construcción en Power BI

## 1. Archivos que debes importar

Usa estos dos archivos:

- `data/processed/ecommerce_clean.csv`
- `data/raw/marketing_spend.csv`

## 2. Cargar datos

1. Abre Power BI Desktop.
2. Selecciona `Obtener datos` > `Texto/CSV`.
3. Importa `ecommerce_clean.csv`.
4. Repite el proceso con `marketing_spend.csv`.
5. Haz clic en `Transformar datos`.

## 3. Ajustes en Power Query

### Tabla `ecommerce_clean`

Confirma estos tipos:

- `order_date`: fecha
- `signup_date`: fecha
- `order_id`: número entero
- `customer_id`: número entero
- `product_id`: número entero
- `quantity`: número entero
- `unit_price`: decimal
- `discount_amount`: decimal
- `shipping_cost`: decimal
- `returned_flag`: número entero
- `gross_revenue`: decimal
- `net_revenue`: decimal
- `product_cost`: decimal
- `net_realized_revenue`: decimal
- `gross_profit`: decimal
- `discount_rate`: decimal
- `order_month`: texto

### Tabla `marketing_spend`

Confirma estos tipos:

- `spend_date`: fecha
- `acquisition_channel`: texto
- `spend`: decimal

## 4. Crear tabla calendario

En `Modelado` > `Nueva tabla`, crea:

```DAX
Calendar =
CALENDAR(
    MIN(ecommerce_clean[order_date]),
    MAX(ecommerce_clean[order_date])
)
```

Luego agrega columnas:

```DAX
Year = YEAR(Calendar[Date])
```

```DAX
Month Number = MONTH(Calendar[Date])
```

```DAX
Month Name = FORMAT(Calendar[Date], "MMMM")
```

```DAX
Year Month = FORMAT(Calendar[Date], "YYYY-MM")
```

Ordena `Month Name` por `Month Number`.

## 5. Crear relaciones

En la vista de modelo:

- Relaciona `Calendar[Date]` con `ecommerce_clean[order_date]`
- Relaciona `Calendar[Date]` con `marketing_spend[spend_date]`
- Relaciona `marketing_spend[acquisition_channel]` con `ecommerce_clean[acquisition_channel]` solo si lo necesitas para ciertos análisis

Si esa relación por canal te genera ambigüedad, no la conectes y usa la tabla de marketing solo para tarjetas o visuales separados.

## 6. Crear medidas DAX

Usa las medidas del archivo:

- `powerbi/dax_measures_es.md`

Además, crea estas medidas extra:

```DAX
Ingreso Neto MTD = TOTALMTD([Ingreso Neto], Calendar[Date])
```

```DAX
Utilidad Bruta MTD = TOTALMTD([Utilidad Bruta], Calendar[Date])
```

```DAX
Clientes Atendidos = DISTINCTCOUNT(ecommerce_clean[customer_id])
```

```DAX
Ingreso por Cliente = DIVIDE([Ingreso Neto], [Clientes])
```

```DAX
Ordenes Devueltas =
CALCULATE(
    DISTINCTCOUNT(ecommerce_clean[order_id]),
    ecommerce_clean[returned_flag] = 1
)
```

## 7. Aplicar tema visual

1. Ve a `Vista` > `Temas` > `Examinar temas`.
2. Carga `powerbi/theme.json`.

Eso te dará una base visual más premium y consistente.

## 8. Página 1: Resumen ejecutivo

### Layout recomendado

- Parte superior: 6 tarjetas KPI
- Centro izquierda: línea de ingreso neto mensual
- Centro derecha: barras de utilidad por canal
- Parte inferior izquierda: barras de tasa de devolución por categoría
- Parte inferior derecha: caja de insights con texto

### Tarjetas KPI

Usa estas medidas:

- `Ingreso Neto`
- `Utilidad Bruta`
- `Margen Bruto %`
- `ROAS`
- `Tasa Recompra %`
- `Tasa Devoluciones %`

### Visual 1: línea mensual

- Visual: gráfico de líneas
- Eje X: `Calendar[Year Month]`
- Valores: `Ingreso Neto`

Formato:

- activa marcadores
- elimina gridlines si se ve cargado
- usa color verde principal

### Visual 2: utilidad por canal

- Visual: barras horizontales
- Eje Y: `ecommerce_clean[acquisition_channel]`
- Valores: `Utilidad Bruta`

Ordena de mayor a menor.

### Visual 3: devoluciones por categoría

- Visual: barras horizontales
- Eje Y: `ecommerce_clean[category]`
- Valores: `Tasa Devoluciones %`

Usa un color cálido para que visualmente parezca una alerta.

### Insight box

Puedes hacerlo con un cuadro de texto y escribir algo como:

`Organic` y `Email` muestran mejor equilibrio entre rentabilidad y eficiencia, mientras que algunas categorías con alta devolución requieren intervención operativa.

## 9. Página 2: Canales y categorías

### Visual 1: matriz de canales

- Filas: `acquisition_channel`
- Valores:
  - `Ordenes`
  - `Clientes`
  - `Ingreso Neto`
  - `Utilidad Bruta`
  - `Margen Bruto %`
  - `ROAS`

Aplica formato condicional en:

- `Margen Bruto %`
- `ROAS`

### Visual 2: scatter de eficiencia

- Visual: dispersión
- Eje X: `ROAS`
- Eje Y: `Margen Bruto %`
- Tamaño: `Ingreso Neto`
- Leyenda: `acquisition_channel`

Este visual se ve muy bien en portafolio porque comunica trade-offs de forma madura.

### Visual 3: tabla de categorías

- Filas: `category`
- Valores:
  - `Ingreso Neto`
  - `Utilidad Bruta`
  - `Tasa Devoluciones %`
  - `Descuento Promedio %`

## 10. Página 3: Clientes y retención

### Visual 1: segmentos RFM

Si prefieres usar el archivo `outputs/tables/rfm_segments.csv`, puedes importarlo también. Si no, usa el que ya está en API como referencia y trabaja luego con el CSV exportado.

Lo más práctico es importar:

- `outputs/tables/rfm_segments.csv`

### Visual 2: barras por segmento

- Eje X: `segment`
- Valores: conteo de `customer_id`

### Visual 3: top clientes

- Tabla con:
  - `customer_id`
  - `monetary`
  - `frequency`
  - `recency`
  - `segment`

Ordena por `monetary` descendente.

### Tarjetas útiles

- número de `Champions`
- número de `At Risk`
- ingreso promedio por cliente

## 11. Segmentadores recomendados

Agrega slicers para:

- `Calendar[Year Month]`
- `acquisition_channel`
- `region`
- `category`

## 12. Cómo hacer que se vea más pro

- usa márgenes amplios entre visuales
- alinea todas las tarjetas
- evita tablas gigantes en la portada
- deja una lectura clara de arriba hacia abajo
- no uses demasiados colores a la vez
- resalta solo 1 o 2 alertas por página

## 13. Cómo contarlo en entrevista

Puedes presentar el dashboard así:

1. Empiezo mostrando la foto general del negocio con KPIs de ingreso, utilidad y eficiencia.
2. Luego bajo a canales y categorías para identificar dónde se gana y dónde se pierde valor.
3. Finalmente cierro con clientes y retención para mostrar cómo priorizar acciones comerciales.

## 14. Siguiente nivel

Si quieres llevarlo a nivel más fuerte todavía:

- agrega bookmarks para storytelling guiado
- crea tooltips personalizados
- usa botones de navegación entre páginas
- añade una portada breve con contexto del problema
