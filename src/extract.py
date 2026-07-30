import pandas as pd

def load_customers(path: str) -> pd.DataFrame:
    """Carga la tabla customers."""
    return pd.read_csv(path)


def load_orders(path: str) -> pd.DataFrame:
    """Carga la tabla orders."""
    return pd.read_csv(path)


def load_order_items(path: str) -> pd.DataFrame:
    """Carga la tabla order_items."""
    return pd.read_csv(path)