from load.database import establecer_conexion

def cargar_customers(customers_df):
    conexion = establecer_conexion()
    cursor = conexion.cursor()

    query = """
        INSERT INTO customers (
            customer_id,
            customer_unique_id,
            customer_zip_code_prefix,
            customer_city,
            customer_state
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    datos = customers_df[
        [
            "customer_id",
            "customer_unique_id",
            "customer_zip_code_prefix",
            "customer_city",
            "customer_state"
        ]
    ].itertuples(index=False, name=None)

    cursor.executemany(query, datos)

    conexion.commit()

    cursor.close()
    conexion.close()