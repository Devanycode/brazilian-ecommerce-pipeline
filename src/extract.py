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

def load_order_products(path: str) -> pd.DataFrame:
    """Carga la tabla order_products"""
    return pd.read_csv(path)

def load_order_payments(path: str) -> pd.DataFrame:
    """Carga la tabla order_payments"""
    return pd.read_csv(path)

def load_sellers(path: str) -> pd.DataFrame:
    """Carga la tabla sellers"""
    return pd.read_csv(path)