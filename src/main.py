from inspector import inspect_csv 
import extract
import pandas as pd
import transform as tr

DATA_PATH = "../data"

customers_df = load_customers(path=f"{DATA_PATH}/olist_customers_dataset.csv")
orders_df = load_orders(path=f"{DATA_PATH}/olist_orders_dataset.csv")
order_items_df = load_order_items(path=f"{DATA_PATH}/olist_order_items_dataset.csv")

geolocation = pd.read_csv(path=f"{DATA_PATH}/olist_geolocation_dataset.csv")
payments = pd.read_csv(path=f"{DATA_PATH}/olist_order_payments_dataset.csv")



# Transformaciones

orders_customers = tr.merge_order_customers(orders_df, customers_df)
tabla_analitica = tr.merge_order_items(orders_customers, order_items_df)
