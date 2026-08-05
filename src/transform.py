import pandas as pd



# ========================
# Union de Tablas
# ========================


def merge_order_customers(
        orders_df: pd.DataFrame, 
        customers_df: pd.DataFrame
    ) -> pd.DataFrame:
    """Hace una unión entre la tabla 'order' y la tabla 'customers'."""
    return orders_df.merge(
        customers_df,
        on= "customer_id",
        how= "left",
        validate= "many_to_one"
    ) 
    
def merge_order_items(
        orders_customers_df: pd.DataFrame,
        order_items_df: pd.DataFrame
    ) -> pd.DataFrame: 
    """Une la tabla order_customers con order_items"""
    return orders_customers_df.merge(
        order_items_df,
        on= "order_id",
        how= "left",
        validate= "one_to_many"
    )

def merge_order_products(
        tabla_analitica: pd.DataFrame, 
        order_products_df: pd.DataFrame
    ) -> pd.DataFrame:
    """Une la tabla 'order_products' con la tabla analítica"""
    df = tabla_analitica.merge(
        order_products_df,
        on="product_id",
        how="left",
        validate="many_to_one"
    )

    df["product_category_name"] = (
        df["product_category_name"]
        .fillna("Sin categoría")
    )
    return df

def merge_order_payments(
        tabla_analitica: pd.DataFrame,
        order_payments_df: pd.DataFrame
    ) -> pd.DataFrame:
    """Une la tabla 'order_payments' con la tabla analítica"""
    order_payments_df = order_payments_df.copy()

    # Convertimos order_payments para no tener una unión N:N
    # Agregamos a nivel de pedido (1 fila = 1 pedido)
    pagos_por_pedido = (
        order_payments_df
        .groupby("order_id", as_index=False)
        .agg(
            num_pagos=("payment_sequential", "count"),
            tipo_pago_principal=("payment_type", "first"),
            cuotas_principales=("payment_installments", "first"),
            total_pagado=("payment_value", "sum")
        )
    )

    df = tabla_analitica.merge(
        pagos_por_pedido,
        on="order_id",
        how="left",
        validate="many_to_one"
    )
    return df

def merge_order_reviews(
        tabla_analitica: pd.DataFrame,
        order_reviews_df: pd.DataFrame
    ) -> pd.DataFrame:
    """Une la tabla 'order_reviews' con la tabla analítica"""
    reviews = order_reviews_df.copy()
    df = tabla_analitica.copy()

    df = df.merge(
        reviews,
        on="order_id",
        how="left",
        validate="many_to_one"
    )

    return df


def merge_sellers(
        tabla_analitica: pd.DataFrame,
        sellers_df: pd.DataFrame
    ) -> pd.DataFrame:
    """Une la tabla 'sellers' con la tabla analítica"""
    df = tabla_analitica.merge(
        sellers_df,
        on="seller_id",
        how="left",
        validate="many_to_one"
    )
    df["seller_state"] = df["seller_state"].fillna("sin_vendedor")
    df["seller_city"] = df["seller_city"].fillna("sin_vendedor")
    df["seller_zip_code_prefix"] = df["seller_zip_code_prefix"].fillna("00000")
    return df


def crear_tabla_analitica(
    customers_df: pd.DataFrame,
    orders_df: pd.DataFrame,
    order_items_df: pd.DataFrame,
    order_products_df: pd.DataFrame,
    order_payments_df: pd.DataFrame,
    sellers_df: pd.DataFrame,
    order_reviews_df: pd.DataFrame
) -> pd.DataFrame:
    """Construye la tabla analítica principal del proyecto."""
    tabla_analitica = merge_order_customers(orders_df, customers_df)
    tabla_analitica = merge_order_items(tabla_analitica, order_items_df)
    tabla_analitica = merge_order_products(tabla_analitica, order_products_df)
    tabla_analitica = merge_order_payments(tabla_analitica, order_payments_df)
    tabla_analitica = merge_sellers(tabla_analitica, sellers_df)
    tabla_analitica = merge_order_reviews(tabla_analitica, order_reviews_df)

    return tabla_analitica



# ==============================
# Preparación de Columnas 
# ==============================

def conversion_a_datetime(tabla_analitica: pd.DataFrame) -> pd.DataFrame:
    """Convierte las columnas de fechas en valores Datetime"""
    tabla = tabla_analitica.copy()
    tabla["order_purchase_timestamp"] = pd.to_datetime(tabla["order_purchase_timestamp"])
    tabla["order_approved_at"] = pd.to_datetime(tabla["order_approved_at"])
    tabla["order_delivered_carrier_date"] = pd.to_datetime(tabla["order_delivered_carrier_date"])
    tabla["order_delivered_customer_date"] = pd.to_datetime(tabla["order_delivered_customer_date"])
    tabla["order_estimated_delivery_date"] = pd.to_datetime(tabla["order_estimated_delivery_date"])
    return tabla

def preparacion_order_reviews(order_reviews_df: pd.DataFrame) -> pd.DataFrame:
    """Prepara los datos de order reviews para evitar duplicados en los análisis"""
    df = order_reviews_df.copy()
    
    # Debido a que su llave primaria es compuesta vamos a eliminar los duplicados de 'review_id'
    df = df.drop_duplicates(subset="review_id", keep="first")
    # Ahora vamos a agrupar todo a un mismo order_id
    df = df.groupby("order_id").agg(
        review_score_promedio=("review_score","mean"),
        num_reviews=("review_id","count"),
        primer_titulo=("review_comment_title","first"),
        primer_comentario=("review_comment_message","first"),
    )
    # Rellenamos los títulos y comentarios vacíos
    df["primer_titulo"] = df["primer_titulo"].fillna("sin titulo")
    df["primer_comentario"] = df["primer_comentario"].fillna("sin mensaje")
    return df


# ==============================
# Agregar Columnas 
# ==============================


def agregar_total_pedido(df: pd.DataFrame) -> pd.DataFrame:
    """agrega una columna con el total de cada pedido."""
    df["total_pedido"] = df.groupby("order_id")["price"].transform("sum")
    return df

def agregar_numero_items(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega la cantidad de productos que tiene cada pedido."""
    df["total_items"] = df.groupby("order_id")["order_item_id"].transform("size")
    return df

def agregar_porcentaje_item(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega el porcentaje que representa cada ítem dentro de su pedido."""
    df = df.copy()
    tabla_total_pedido = agregar_total_pedido(df)

    tabla_total_pedido["porcentaje_item"] = (
        tabla_total_pedido["price"] / 
        tabla_total_pedido["total_pedido"]
    ) * 100

    return tabla_total_pedido

def agregar_columnas_fecha(df: pd.DataFrame) -> pd.DataFrame:
    """ 
    - Convierte la columna de la fecha y hora de compra en un datetime
    - Agrega dos columnas nuevas:
        Una con el número del mes 
        Otra con el nombre del mes
    """
    df = df.copy()

    df["nombre_mes"] = (
        df["order_purchase_timestamp"].dt.month_name(locale='es_ES.utf8')
    )

    df["numero_mes"] = (
        df["order_purchase_timestamp"].dt.month
    )

    return df

def agregar_indicador_venta_local(df: pd.DataFrame) -> pd.DataFrame:
    """Indica si el vendedor y el cliente están en el mismo estado."""
    df = df.copy()
    df["es_venta_local"] = df["customer_state"] == df["seller_state"]
    return df



