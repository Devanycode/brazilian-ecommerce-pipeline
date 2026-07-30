import pandas as pd


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
