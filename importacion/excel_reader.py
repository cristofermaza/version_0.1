import pandas as pd


COLUMNAS_REQUERIDAS = [
    "Fecha y tiempo",
    "ID usuario",
    "Nombre",
    "Apellido",
    "Número de tarjeta",
    "Dispositivo",
    "Verificación",
    "Estado",
    "Evento",
    "Notas"
]


def leer_excel(ruta):

    try:

        df = pd.read_excel(ruta)

        return {
            "ok": True,
            "datos": df,
            "error": None
        }

    except Exception as e:

        return {
            "ok": False,
            "datos": None,
            "error": str(e)
        }


def validar_columnas(df):

    columnas_faltantes = []

    for columna in COLUMNAS_REQUERIDAS:

        if columna not in df.columns:
            columnas_faltantes.append(columna)

    if columnas_faltantes:

        return {
            "ok": False,
            "faltantes": columnas_faltantes
        }

    return {
        "ok": True,
        "faltantes": []
    }