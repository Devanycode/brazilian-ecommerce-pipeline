import main
import transform as tr

# 1. Extract
customers_df = main.customers_df
orders_df = main.orders_df 
order_items_df = main.order_items_df
order_products_df = main.order_products_df
order_payments_df = main.order_payments_df
sellers_df = main.sellers_df
order_reviews_df = main.order_reviews_df



# 2. Creación de tabla analítica
# Para evitar problemas de granularidad
order_reviews_df_modified = tr.preparacion_order_reviews(order_reviews_df)
tabla = tr.crear_tabla_analitica(
    customers_df, 
    orders_df, 
    order_items_df, 
    order_products_df,
    order_payments_df,
    sellers_df,
    order_reviews_df_modified
)

#  3. Transformaciones
tabla = tr.conversion_a_datetime(tabla)
tabla = tr.agregar_total_pedido(tabla)
tabla = tr.agregar_numero_items(tabla)
tabla = tr.agregar_porcentaje_item(tabla)
tabla = tr.agregar_columnas_fecha(tabla)
tabla = tr.agregar_indicador_venta_local(tabla)


print(f"Tabla analítica creada: {tabla.shape[0]} filas, {tabla.shape[1]} columnas")


