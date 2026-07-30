import pandas as pd

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


def crear_tabla_analitica(
    customers_df: pd.DataFrame,
    orders_df: pd.DataFrame,
    order_items_df: pd.DataFrame
) -> pd.DataFrame:
    """Construye la tabla analítica principal del proyecto."""
    orders_customers = merge_order_customers(orders_df, customers_df)
    tabla_analitica = merge_order_items(orders_customers, order_items_df)

    return tabla_analitica


def agregar_total_pedido(df: pd.DataFrame) -> pd.DataFrame:
    """agrega una columna con el total de cada pedido."""
    df["total_pedido"] = df.groupby("order_id", as_index=False)["price"].transform("sum")
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

    df["order_purchase_timestamp"] = (
        pd.to_datetime(df["order_purchase_timestamp"])
    )

    df["nombre_mes"] = (
        df["order_purchase_timestamp"].dt.month_name(locale='es_ES.utf8')
    )

    df["numero_mes"] = (
        df["order_purchase_timestamp"].dt.month
    )

    return df


