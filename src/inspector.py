import pandas as pd

def inspect_csv(df: pd.DataFrame) -> None:
    """Devolverá un reporte detallado del archivo csv que se cargó"""
    report = {
        "filas": df.shape[0],
        "columnas": df.shape[1],
        "tipos de datos": df.dtypes,
        "nulos": df.isnull().sum(),
        "duplicados": df.duplicated().sum(),
        "candidate_keys":[
            column for column in df.columns
            if df[column].nunique() == len(df)
        ]
    }
    
    for key, value in report.items():
        print(f"{key}:\n{value}\n")
        
    return 