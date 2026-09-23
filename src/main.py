import pandas as pd
import extract
import contracts
from inspector import inspect_csv, verificar_contratos
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
order_reviews_df = extract.load_order_reviews(f"{DATA_PATH}/olist_order_reviews_dataset.csv")


# 2. TRANSFORM 
orders_df = tr.conversion_a_datetime(orders_df)
order_items_df = tr.order_items_shipping_limit_convert_datetime(order_items_df) 
order_products_df = tr.order_products_convert_float_to_int(order_products_df)
order_reviews_df = tr.order_reviews_convert_datetime(order_reviews_df)


# 3. SANITY CHECKS
validar_ventas_pagos = (an.validar_ventas_vs_pagos(
    orders_df,
    customers_df,
    order_items_df,
    order_payments_df
))
pedidos_sin_items = an.pedidos_sin_items(orders_df, order_items_df)
customer_id_rotos = an.customer_id_rotos(customers_df, orders_df)

print("\n--- VALIDACIÓN DE VENTAS VS PAGOS ---")
print(validar_ventas_pagos)

print("\n--- PEDIDOS SIN ITEMS ---")
print(pedidos_sin_items)

print("\n--- CUSTOMER_ID ROTOS ---")
print(customer_id_rotos)


# 4. Inspección de tablas
tablas = {
    "customers": (customers_df, contracts.CUSTOMERS_PRIMARY_KEY, contracts.CUSTOMERS_COLUMNS),
    "orders": (orders_df, contracts.ORDERS_PRIMARY_KEY, contracts.ORDERS_COLUMNS),
    "order_items": (order_items_df, contracts.ORDER_ITEMS_PRIMARY_KEY, contracts.ORDER_ITEMS_COLUMNS),
    "order_products": (order_products_df, contracts.ORDER_PRODUCTS_PRIMARY_KEY, contracts.ORDER_PRODUCTS_COLUMNS),
    "order_payments": (order_payments_df, contracts.ORDER_PAYMENTS_PRIMARY_KEY, contracts.ORDER_PAYMENTS_COLUMNS),
    "sellers": (sellers_df, contracts.SELLERS_PRIMARY_KEY, contracts.SELLERS_COLUMNS),
    "order_reviews":(order_reviews_df, contracts.ORDER_REVIEWS_PRIMARY_KEY, contracts.ORDER_REVIEWS_COLUMNS)
}

todas_cumplen, resultados = verificar_contratos(tablas)
print(resultados)


# 5. Load
if todas_cumplen:
    pass

