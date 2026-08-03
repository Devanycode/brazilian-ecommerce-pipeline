import pandas as pd
from transform import agregar_columnas_fecha


# ========================================================
# Análisis de Negocio
# ========================================================

def ventas_por_estado(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula las ventas totales por estado"""
    return (
        df
        .groupby("customer_state", as_index=False)
        .agg(
            ventas_totales=("price", "sum")
        )
        .sort_values("ventas_totales", ascending=False)
    )


def ticket_promedio_por_estado(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula el ticket promedio por estado.

    Primero suma el valor de todos los ítems de cada pedido y,
    posteriormente, calcula el promedio de esos pedidos para cada estado.
    """
    ticket_precio = (
        df
        .groupby(
            ["order_id", "customer_state"],
            as_index=False
        )
        .agg(
            total_pedido=("price", "sum")
        )
    )

    return (
        ticket_precio
        .groupby(
            "customer_state",
            as_index=False
        )
        .agg(
            ticket_promedio=("total_pedido", "mean")
        )
        .sort_values(
            "ticket_promedio",
            ascending=False
        )
    )

def compras_por_mes(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve el valor total de las compras por cada mes."""
    df = df.copy()
    df = agregar_columnas_fecha(df)

    return (
        df
        .groupby(["numero_mes", "nombre_mes"], as_index=False)["price"]
        .sum()
        .sort_values(by=["numero_mes", "nombre_mes"])
    )


def tiempo_promedio_entrega_por_estado(orders_df: pd.DataFrame) -> pd.DataFrame:
    """Calcula el tiempo promedio por estado desde que
     se realiza la compra hasta que le llega el pedido al cliente"""
    tabla = orders_df.copy()

    # Eliminamos los pedidos que aparezcan duplicados debido a los items
    tabla = tabla.drop_duplicates(subset="order_id", keep="first")
    tabla["tiempo_de_entrega"] = tabla["order_delivered_customer_date"] - tabla["order_purchase_timestamp"]
    return (
        tabla
        .groupby("customer_state", as_index=False)
        .agg(tiempo_promedio_entrega = ("tiempo_de_entrega", "mean"))
        .sort_values(by="tiempo_promedio_entrega")
    )


def ingresos_por_categoria(tabla_analitica: pd.DataFrame) -> pd.DataFrame:
    """Calcula los ingresos que tuvo cada categoría de producto"""
    tabla = tabla_analitica.copy()

    return (
        tabla
        .groupby("product_category_name", as_index=False)
        .agg(ingresos_categoria = ("price", "sum"))
        .sort_values(ascending=False, by="ingresos_categoria")
    )





# ===========================================================
# SANITY CHECKS
# ===========================================================

def validar_ventas_vs_pagos(
    orders_df: pd.DataFrame,
    customers_df: pd.DataFrame,
    order_items_df: pd.DataFrame,
    order_payments_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Sanity check: compara (precio + envío) vs pagos reales por estado.
    """
    # 1. Camino de ÍTEMS: orders → customers → items
    # Agregamos price + freight_value para obtener el valor total del pedido
    ventas = (
        orders_df
        .merge(customers_df, on="customer_id", how="left", validate="many_to_one")
        .merge(order_items_df, on="order_id", how="left", validate="one_to_many")
        .groupby("customer_state", as_index=False)
        .agg(
            total_producto=("price", "sum"),
            total_envio=("freight_value", "sum")
        )
    )
    ventas["ventas_totales"] = ventas["total_producto"] + ventas["total_envio"]
    
    # 2. Camino de PAGOS: orders → customers → payments
    pagos = (
        orders_df
        .merge(customers_df, on="customer_id", how="left", validate="many_to_one")
        .merge(order_payments_df, on="order_id", how="left", validate="one_to_many")
        .groupby("customer_state", as_index=False)
        .agg(pagos_totales=("payment_value", "sum"))
    )
    
    # 3. Comparar
    comparacion = ventas.merge(pagos, on="customer_state", how="outer")
    comparacion["diferencia"] = comparacion["pagos_totales"] - comparacion["ventas_totales"]
    comparacion["diferencia_pct"] = (comparacion["diferencia"] / comparacion["ventas_totales"]) * 100
    
    return comparacion.sort_values("diferencia_pct", ascending=False)