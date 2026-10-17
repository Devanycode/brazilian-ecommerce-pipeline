# Documentación del Modelo DAX

Este documento centraliza la lógica de negocio y las fórmulas DAX desarrolladas para el Dashboard de Olist.

## Resumen de Componentes

| Nombre                            | Tipo                | Descripción Corta                                                                      |
| --------------------------------- | ------------------- | -------------------------------------------------------------------------------------- |
| Ingresos Totales                  | KPI (medida)        | Suma total de todas las compras                                                          |
| Pedidos Totales                   | KPI (medida)        | Conteo del total de pedidos                                                         |
| Ticket Promedio                   | KPI (medida)        | Valor promedio de cada compra                                                             |
| Tiempo Promedio de Entrega (Días) | KPI (medida)        | Tiempo promedio que tarda un pedido en ser entregado desde que se crea la orden   |
| Satisfacción Promedio             | KPI (medida)        | En base a las encuestas mide la calificación promedio que le dan a un pedido           |
| Porcentaje de Entregas a Tiempo   | KPI (medida)        | Porcentaje de los pedidos que se entregaron dentro del rango de tiempo estimado        |
| Dias Entrega                      | Columna Calculada   | Diferencia en días desde que la orden de un pedido es creada y se entrega el pedido    |
| Cumplimiento Entrega              | Columna Calculada   | Categoriza los pedidos en base a si cumplieron o no con su tiempo estimado de entrega  |
| Total Entregas a Tiempo           | Medida Auxiliar | Cuenta el total de pedidos que se entregaron en el rango de tiempo estimado            |
| Conteo Pedidos Entregados         | Medida Auxiliar | Cuenta el total de pedidos que ya fueron entregados                                    |
| Conteo Items Vendidos             | Medida Auxiliar | Cuenta el total de ítems vendidos                                                      |

---
## Contexto de Reporte

> Filtro avanzado sobre `order_purchase_timestamp`: desde el **01/01/2017** hasta el **31/08/2018**, en todas las páginas.

> **Razón:** Los meses fuera de ese rango tienen muy pocos pedidos y distorsionan tendencias y promedios.

> **Efecto:** Todas las medidas se calculan dentro de ese período. 

> **Dónde Cambiarlo:** Panel Filtros → “Filtros en todas las páginas" y también modificando el filtro de año para poder analizar el año 2016.

---
## KPIs

### Ingresos Totales

```dax

Ingresos Totales =
	SUM(
	    'brazilian_ecommerce tabla_analitica'[price]
	)

```
> **Nota de Desarrollo:**
- Estos son los ingresos totales basados únicamente en el precio de los productos, sin incluir el valor del envío.

### Pedidos Totales

```dax

Pedidos Totales =
	DISTINCTCOUNT(
	    'brazilian_ecommerce tabla_analitica'[order_id]
	)

```
> **Nota de Desarrollo:**
- Cuenta únicamente los pedidos que no son vacíos y tienen al menos un ítem.


### Ticket Promedio

```dax

Ticket Promedio =
	DIVIDE(
		[Ingresos Totales], [Pedidos Totales]
	)

```

### Tiempo Promedio de Entrega (Días)

```dax

Tiempo Promedio de Entrega =
	AVERAGEX(
	    DISTINCT(
	        'brazilian_ecommerce tabla_analitica'[order_id]),
	    CALCULATE(
	        AVERAGE(
	            'brazilian_ecommerce tabla_analitica'[Dias Entrega]
	        )
	    )
	)

```

> **Notas de desarrollo**
- **Optimización del grano:** Si un pedido contiene 5 productos, la tabla analítica presenta 5 filas repetidas con el mismo `order_id`. Un `AVERAGE` directo duplicaría el peso de ese pedido en el reporte.
- **Preservación de Linaje:** Aunque `DISTINCT` genera una lista virtual de una sola columna, esta conserva su linaje de datos nativo. Esto permite que `CALCULATE` realice la transición de contexto y use un filtro automático sobre la tabla completa, simulando un comportamiento de `GROUP BY` dinámico, asegurando que el promedio de `dias_entrega` se evalúe de manera aislada para cada orden antes de promediar el total general.

### Satisfacción Promedio

```dax

Satisfaccion Promedio = 
	AVERAGEX(
		DISTINCT('brazilian_ecommerce tabla_analitica'[order_id]),
		CALCULATE(
			AVERAGE(
				'brazilian_ecommerce tabla_analitica'[review_score_promedio]
			)
		)
	)
	
```

> **Notas de Desarrollo:**
- **Optimización del grano:** Las calificaciones a las encuestas son por pedidos y no por ítems, para no tener información duplicada cambiamos la granularidad agrupando y promediando para conservar una única calificación por pedido. 
- **Mecanismo Técnico:** Esta fórmula opera bajo el mismo principio de *Preservación de Linaje* y *Transición de Contexto* explicado detalladamente en el KPI anterior `[Tiempo Promedio de Entrega]`, garantizando un comportamiento analítico idéntico sobre el `order_id`.

### Porcentaje de Entregas a Tiempo

```dax
Porcentaje de Entregas a Tiempo = 
	DIVIDE(
		[total entregas a tiempo], 
		[conteo pedidos entregados] 
	)
```
> **Nota de desarrollo:**
+ Para el cálculo se toma en cuenta únicamente los pedidos que ya fueron entregados, para evitar hacer cálculos con valores nulos.

---
## Columnas Calculadas

### Dias Entrega
```dax
Dias Entrega = 
	DATEDIFF(
		[order_purchase_timestamp], 
		[order_delivered_customer_date], 
		DAY
	)
```
> **Nota de Desarrollo:**
- Es la diferencia en días desde que se creó la orden de pedido hasta que el pedido fue entregado al cliente.

### Cumplimiento Entrega 

```dax
Cumplimiento Entrega =
    SWITCH(
        TRUE(),
        ISBLANK([order_estimated_delivery_date])
            || ISBLANK([order_delivered_customer_date]),
        "sin fecha de entrega",
        DATEDIFF(
            [order_estimated_delivery_date],
            [order_delivered_customer_date],
            DAY
        ) > 0,
        "despues de tiempo",
        DATEDIFF(
            [order_estimated_delivery_date],
            [order_delivered_customer_date],
            DAY
        ) = 0,
        "mismo dia",
        "antes de tiempo"
    )
```
> **Notas de Negocio:**
- Esta columna está categorizada en base a si se cumple o no con los tiempos estimados de entrega.
- Se usa `ISBLANK` para categorizar también esos pedidos que fueron cancelados o que no han sido entregados.

--- 
## Medidas Auxiliares

### Total Entregas a Tiempo

```dax
Total Entregas a Tiempo = 
	CALCULATE(
	    DISTINCTCOUNT('brazilian_ecommerce tabla_analitica'[order_id]),
	    'brazilian_ecommerce tabla_analitica'[Cumplimiento Entrega] = 
	    "mismo dia"           
	    ||
		'brazilian_ecommerce tabla_analitica'[Cumplimiento Entrega] = 
		"antes de tiempo"
	)
```

### Conteo Pedidos Entregados

```dax
Conteo Pedidos Entregados = 
	CALCULATE(
	    DISTINCTCOUNT('brazilian_ecommerce tabla_analitica'[order_id]),
	    'brazilian_ecommerce tabla_analitica'[Cumplimiento Entrega] <> 
	    "sin fecha de entrega"
	)
```

### Conteo Items Vendidos

```dax
Conteo Items Vendidos = 
	COUNT(
		'brazilian_ecommerce tabla_analitica'[order_item_id]
	)
```

