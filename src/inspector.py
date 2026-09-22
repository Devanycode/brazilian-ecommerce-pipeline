import pandas as pd

def inspect_csv(df: pd.DataFrame, primary_key, columnas_esperadas: dict) -> dict:
    """
    Verifica si el DataFrame cumple el contrato esperado por la tabla MySQL destino.
    columnas_esperadas: {"nombre_columna": int | float | str | datetime}
    """

    errores = []

    # Normalizamos la PK para trabajar siempre con una lista.
    if isinstance(primary_key, str):
        primary_key = [primary_key]
        

    # Columnas faltantes
    columnas_faltantes = set(columnas_esperadas) - set(df.columns)
    if columnas_faltantes:
        errores.append(f"Columnas faltantes: {columnas_faltantes}")
    
    # 2. Comprobar que las columnas de la PK existen
    pk_faltantes = [
        columna
        for columna in primary_key
        if columna not in df.columns
    ]

    if pk_faltantes:
        errores.append(
            f"Columnas de la PK faltantes: {pk_faltantes}"
        )
    # Solo continuamos con las comprobaciones de PK
    # si todas las columnas existen.
    if not pk_faltantes:

        # NULL en la PK
        pk_nulos = df[primary_key].isna().sum()
        pk_nulos = pk_nulos[pk_nulos > 0]    # Sólo dejar las columnas donde haya nulos 
        if not pk_nulos.empty:    # Si este objeto no está vacío
            errores.append(f"Nulos en la llave primaria: {pk_nulos}")
        
        # Duplicados en la PK
        pk_duplicados = df.duplicated(subset=primary_key).sum()
        if pk_duplicados > 0:
            errores.append(f"Duplicados en la llave primaria: {pk_duplicados}")

        # Tipos incompatibles
        tipos_incompatibles = {}
        for columna, tipo_esperado in columnas_esperadas.items():
            if columna not in df.columns:
                continue
            actual = df[columna].dtype
            if tipo_esperado == "int" and not pd.api.types.is_integer_dtype(actual):
                tipos_incompatibles[columna] = str(actual)
            elif tipo_esperado == "float" and not pd.api.types.is_float_dtype(actual):
                tipos_incompatibles[columna] = str(actual)
            elif tipo_esperado == "str" and not pd.api.types.is_string_dtype(actual):
                tipos_incompatibles[columna] = str(actual)
            elif tipo_esperado == "datetime" and not pd.api.types.is_datetime64_any_dtype(actual):
                tipos_incompatibles[columna] = str(actual)
        if tipos_incompatibles:
            errores.append(f"Tipos incompatibles: {tipos_incompatibles}")
        
    return {
        "cumple_contrato": len(errores) == 0,
        "errores": errores,
        "filas": df.shape[0],
        "nulos_por_columna": df.isnull().sum().to_dict(),
    }


def verificar_contratos(tablas: dict) -> tuple[bool, dict]:
    """Corre inspect_csv sobre cada tabla del diccionario y resume si todas cumplen."""

    resultados = {
        nombre: inspect_csv(df, pk, columns)
        for nombre, (df, pk, columns) in tablas.items()
    }
    
    incumplen_contrato = {
        nombre: resultado
        for nombre, resultado in resultados.items()
        if not resultado["cumple_contrato"]
    }

    if incumplen_contrato:
        print("\n"*2 + "---------------------------------------")
        print(f"No se permite cargar, incumplen contrato las siguientes tablas:\n{list(incumplen_contrato.keys())}")
        return False, resultados

    print("\n"*2 + "---------------------------------------")
    print("Se permite cargar, todas las tablas cumplen el contrato\n")
    return True, resultados