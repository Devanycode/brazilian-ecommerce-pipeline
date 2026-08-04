import pandas as pd
import extract
import transform as tr
import analytics as an

DATA_PATH = "../data"

# 1. EXTRACT
customers_df = extract.load_customers(f"{DATA_PATH}/olist_customers_dataset.csv")
orders_df = extract.load_orders(f"{DATA_PATH}/olist_orders_dataset.csv")
order_items_df = extract.load_order_items(f"{DATA_PATH}/olist_order_items_dataset.csv")
order_products_df = extract.load_order_products(f"{DATA_PATH}/olist_products_dataset.csv")
order_payments_df = extract.load_order_payments(f"{DATA_PATH}/olist_order_payments_dataset.csv")
sellers_df = extract.load_sellers(f"{DATA_PATH}/olist_sellers_dataset.csv")
reviews_df = pd.read_csv(f"{DATA_PATH}/olist_order_reviews_dataset.csv")

# 2. TRANSFORM - Pipeline completo
tabla = tr.crear_tabla_analitica(
    customers_df, 
    orders_df, 
    order_items_df, 
    order_products_df,
    order_payments_df,
    sellers_df
)
tabla = tr.conversion_a_datetime(tabla)
tabla = tr.agregar_total_pedido(tabla)
tabla = tr.agregar_numero_items(tabla)
tabla = tr.agregar_porcentaje_item(tabla)
tabla = tr.agregar_columnas_fecha(tabla)
tabla = tr.agregar_indicador_venta_local(tabla)

print(f"Tabla analítica creada: {tabla.shape[0]} filas, {tabla.shape[1]} columnas")

# 3. ANALYTICS
ventas_estado = an.ventas_por_estado(tabla)
ticket_estado = an.ticket_promedio_por_estado(tabla)
compras_mes = an.compras_por_mes(tabla)
tiempo_entrega = an.tiempo_promedio_entrega_por_estado(tabla)
ingresos_categoria = an.ingresos_por_categoria(tabla)
ingresos_estados_vendedores = an.ingresos_por_estado_del_vendedor(tabla)
ventas_locales_vs_foraneas = an.ventas_locales_vs_foraneas_por_estado(tabla)

print("\n--- TOP 5 ESTADOS POR VENTAS ---")
print(ventas_estado.head())

print("\n--- TOP 5 ESTADOS POR TICKET PROMEDIO ---")
print(ticket_estado.head())

print("\n--- COMPRAS POR MES ---")
print(compras_mes)

print("\n--- TIEMPO DE ENTREGA POR ESTADO ---")
print(tiempo_entrega)

print("\n--- INGRESOS POR CATEGORIA ---")
print(ingresos_categoria)

print("\n--- INGRESOS POR ESTADO DEL VENDEDOR ---")
print(ingresos_estados_vendedores)

print("\n--- VENTAS LOCALES VS FORÁNEAS POR ESTADO ---")
print(ventas_locales_vs_foraneas)

# SANITY CHECKS
validar_ventas_pagos = (an.validar_ventas_vs_pagos(
    orders_df,
    customers_df,
    order_items_df,
    order_payments_df
))

print("--- VALIDACIÓN DE VENTAS VS PAGOS ---")
print(validar_ventas_pagos)


















####-------



"""⬜ Número de pedidos únicos en orders vs número de pedidos
 únicos en order_items — debería ser casi igual. Si hay 100 pedidos en orders
  pero solo 80 en items, hay 20 pedidos vacíos.
⬜ Clientes únicos en customers vs clientes únicos en orders
 — si hay más en orders que en customers, hay customer_id rotos."""