import os

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


def establecer_conexion():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


# Si se ejecuta desde este mismo archivo
if __name__ == "__main__":
    conexion = establecer_conexion()
    print("Conexión exitosa")
    conexion.close()