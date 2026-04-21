# Medidas DAX sugeridas

Asumiendo que importas la tabla principal del análisis limpio como `ecommerce_clean`.

## Medidas base

```DAX
Ingreso Neto = SUM(ecommerce_clean[net_realized_revenue])
```

```DAX
Utilidad Bruta = SUM(ecommerce_clean[gross_profit])
```

```DAX
Ordenes = DISTINCTCOUNT(ecommerce_clean[order_id])
```

```DAX
Clientes = DISTINCTCOUNT(ecommerce_clean[customer_id])
```

```DAX
Ticket Promedio = DIVIDE([Ingreso Neto], [Ordenes])
```

```DAX
Margen Bruto % = DIVIDE([Utilidad Bruta], [Ingreso Neto])
```

```DAX
Tasa Devoluciones % = AVERAGE(ecommerce_clean[returned_flag])
```

```DAX
Descuento Promedio % = AVERAGE(ecommerce_clean[discount_rate])
```

## Medidas de retención

```DAX
Clientes Recompra =
CALCULATE(
    DISTINCTCOUNT(ecommerce_clean[customer_id]),
    FILTER(
        VALUES(ecommerce_clean[customer_id]),
        CALCULATE(DISTINCTCOUNT(ecommerce_clean[order_id])) > 1
    )
)
```

```DAX
Tasa Recompra % = DIVIDE([Clientes Recompra], [Clientes])
```

## Si importas marketing_spend como tabla separada

Asumiendo una tabla `marketing_spend`.

```DAX
Inversion Marketing = SUM(marketing_spend[spend])
```

```DAX
ROAS = DIVIDE([Ingreso Neto], [Inversion Marketing])
```

## Insights útiles como tarjetas

```DAX
Canal Top Utilidad =
TOPN(
    1,
    VALUES(ecommerce_clean[acquisition_channel]),
    [Utilidad Bruta],
    DESC
)
```

```DAX
Categoria Mayor Devolucion =
TOPN(
    1,
    VALUES(ecommerce_clean[category]),
    [Tasa Devoluciones %],
    DESC
)
```
