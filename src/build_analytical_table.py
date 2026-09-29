import contracts
import extract
from inspector import verificar_contratos
import transform as tr

DATA_PATH = "../data"

# 1. EXTRACT
customers_df = extract.load_customers(f"{DATA_PATH}/olist_customers_dataset.csv")
orders_df = extract.load_orders(f"{DATA_PATH}/olist_orders_dataset.csv")
order_items_df = extract.load_order_items(f"{DATA_PATH}/olist_order_items_dataset.csv")
order_products_df = extract.load_order_products(f"{DATA_PATH}/olist_products_dataset.csv")
order_payments_df = extract.load_order_payments(f"{DATA_PATH}/olist_order_payments_dataset.csv")
sellers_df = extract.load_sellers(f"{DATA_PATH}/olist_sellers_dataset.csv")
order_reviews_df = extract.load_order_reviews(f"{DATA_PATH}/olist_order_reviews_dataset.csv")


# 2. TRANSFORM: tablas individuales
orders_df = tr.conversion_a_datetime(orders_df)
order_items_df = tr.order_items_shipping_limit_convert_datetime(order_items_df) 
order_products_df = tr.order_products_convert_float_to_int(order_products_df)
order_reviews_df = tr.order_reviews_convert_datetime(order_reviews_df)


# 3. Creación de tabla analítica
# Para evitar problemas de granularidad
order_reviews_df_modified = tr.preparacion_order_reviews(order_reviews_df)
order_payments_df_modified = tr.preparacion_order_payments(order_payments_df)
tabla = tr.crear_tabla_analitica(
    customers_df, 
    orders_df, 
    order_items_df, 
    order_products_df,
    order_payments_df_modified,
    sellers_df,
    order_reviews_df_modified
)
######### tabla = tr.normalizar_dtypes_tabla_analitica(tabla)

#  3.1 Transform tabla analítica
tabla = tr.agregar_total_pedido(tabla)
tabla = tr.agregar_numero_items(tabla)
tabla = tr.agregar_porcentaje_item(tabla)
tabla = tr.agregar_columnas_fecha(tabla)
tabla = tr.agregar_indicador_venta_local(tabla)
tabla = tr.solucion_contrato_tabla_analitica(tabla)

print(f"Tabla analítica creada: {tabla.shape[0]} filas, {tabla.shape[1]} columnas")


# 4. Inspección de tablas
todas_cumplen, resultados = verificar_contratos(
    {"tabla_analitica": (
        tabla, 
        contracts.TABLA_ANALITICA_PRIMARY_KEY, 
        contracts.TABLA_ANALITICA_COLUMNS
        )
    }
)

print(resultados)

"""
Tipos incompatibles 
seller_<ip_code_prefix int -> str (se debe convertir antes del merge)
"""




print(sellers_df["seller_zip_code_prefix"].dtype)