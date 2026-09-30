import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import time



load_dotenv()
HOST=os.getenv("DB_HOST")
PORT=os.getenv("DB_PORT")
USER=os.getenv("DB_USER")
PASSWORD=os.getenv("DB_PASSWORD")
DATABASE=os.getenv("DB_NAME")


url = URL.create(
    "mysql+pymysql",
    username=USER,
    password=PASSWORD,
    host=HOST,
    port=int(PORT),
    database=DATABASE,
)
engine = create_engine(url)

def cargar_tablas(dataframes: dict[str:"nombre_tabla", pd.DataFrame:"tabla"]) -> None:
    """Función para cargar cualquier tabla a mi conexión en MySQL"""
    with engine.begin() as conn:
        for nombre_tabla, df in dataframes.items():
            inicio = time.time()
            print(f"Cargando {nombre_tabla} ({len(df)} filas)...", flush=True)
            df.to_sql(
                name=nombre_tabla,
                con=conn,
                if_exists="replace",
                index=False,
                chunksize=10_000,
            )
            print(f"  listo en {time.time() - inicio:.1f} s", flush=True)

def verificar_carga(dataframes):
    """Compara filas en MySQL vs. filas en cada dataframe."""
    for nombre_tabla, df in dataframes.items():
        total = pd.read_sql(f"SELECT COUNT(*) AS total FROM {nombre_tabla}", engine)["total"][0]
        estado = "OK" if total == len(df) else "NO COINCIDE"
        print(f"{nombre_tabla}: {total} en MySQL vs {len(df)} en pandas -> {estado}")