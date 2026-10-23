import pandas as pd

from importacion.excel_reader import COLUMNAS_REQUERIDAS


CAMPOS_OBLIGATORIOS = [
    "ID usuario",
    "Nombre",
    "Apellido",
    "Fecha y tiempo",
]


def validar_dataframe(df):
    if df is None:
        return {
            "ok": False,
            "errores": ["No se recibieron datos para validar."],
        }

    columnas_faltantes = [
        columna
        for columna in COLUMNAS_REQUERIDAS
        if columna not in df.columns
    ]

    if columnas_faltantes:
        return {
            "ok": False,
            "errores": [
                "Faltan columnas: " + ", ".join(columnas_faltantes)
            ],
        }

    if df.empty:
        return {
            "ok": False,
            "errores": ["El archivo no contiene marcaciones."],
        }

    datos = df.dropna(how="all").copy()

    if datos.empty:
        return {
            "ok": False,
            "errores": ["El archivo solo contiene filas vacías."],
        }

    errores = []

    for campo in CAMPOS_OBLIGATORIOS:
        vacios = datos[campo].isna() | (
            datos[campo].astype(str).str.strip() == ""
        )

        if vacios.any():
            errores.append(
                f"El campo '{campo}' está vacío en "
                f"{int(vacios.sum())} fila(s)."
            )

    fechas = pd.to_datetime(
        datos["Fecha y tiempo"],
        errors="coerce",
    )

    fechas_invalidas = fechas.isna()

    if fechas_invalidas.any():
        errores.append(
            f"Hay {int(fechas_invalidas.sum())} fecha(s) inválida(s)."
        )

    return {
        "ok": not errores,
        "errores": errores,
    }
