# Dashboard Power BI: versión ejecutiva

## Objetivo

Construir un dashboard con nivel de portafolio que se sienta ejecutivo, claro y orientado a decisiones. La idea no es saturarlo, sino mostrar criterio visual y lectura de negocio.

## Estilo recomendado

- Fondo marfil suave: `#F4EFE7`
- Tarjetas claras: `#FFFAF2`
- Texto principal: `#18230F`
- Color de énfasis: `#6B8A3A`
- Colores secundarios:
  - naranja: `#C97C2C`
  - azul petróleo: `#1F4E5F`
  - rojo ladrillo: `#A64032`

## Página 1: Resumen ejecutivo

### KPIs principales

- Ingreso neto
- Utilidad bruta
- Margen bruto %
- ROAS
- Tasa de recompra %
- Tasa de devoluciones %

### Visuales

- Línea: evolución mensual del ingreso neto
- Barras horizontales: utilidad por canal
- Barras horizontales: tasa de devolución por categoría
- Tarjeta de insight:
  - mejor canal por utilidad
  - peor canal por ROAS
  - categoría con mayor devolución

### Mensaje que debe dejar esta página

El negocio no tiene un problema de ventas únicamente, sino de calidad de ingresos y eficiencia comercial.

## Página 2: Canales y categorías

### Visuales

- Matriz por canal con:
  - órdenes
  - clientes
  - ingreso neto
  - utilidad bruta
  - margen %
  - ROAS
- Scatter plot:
  - eje X: ROAS
  - eje Y: margen bruto %
  - tamaño: ingreso neto
  - leyenda: canal
- Tabla por categoría con:
  - ingreso neto
  - utilidad
  - tasa de devolución
  - descuento promedio

### Mensaje que debe dejar esta página

No todos los canales valen lo mismo y no todas las categorías con ventas altas son sanas para el negocio.

## Página 3: Clientes y retención

### Visuales

- Barras: clientes por segmento RFM
- Tabla: top clientes por valor monetario
- Tarjetas:
  - clientes Champions
  - clientes At Risk
  - ingreso promedio por cliente
- Segmentador:
  - canal
  - región
  - segmento

### Mensaje que debe dejar esta página

La retención debe priorizarse por valor y riesgo, no de forma masiva e indiscriminada.

## Recomendaciones de diseño

- Usa suficiente espacio en blanco
- No metas más de 5 o 6 visuales por página
- Evita colores chillones o demasiadas líneas de cuadrícula
- Resalta 2 o 3 insights por página en texto corto
- Mantén consistencia tipográfica y de márgenes

## Storytelling sugerido al presentar

1. Primero muestro la foto general del negocio
2. Luego explico dónde se pierde eficiencia
3. Finalmente muestro a qué segmentos conviene atacar con retención
