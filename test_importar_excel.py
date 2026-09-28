from importacion.excel_reader import (
    leer_excel,
    validar_columnas
)

from importacion.database_importer import (
    importar_dataframe
)



ruta = r"C:\Users\CRISTOFER\Downloads\biometricos\biometrico_septiembre_2026_01.xlsx"

print("================================")
print("IMPORTACIÓN DE PRUEBA")
print("================================")


resultado = leer_excel(ruta)


if not resultado["ok"]:

    print("ERROR leyendo Excel:")
    print(resultado["error"])

    raise SystemExit


df = resultado["datos"]


print("Excel leído correctamente")
print("Registros encontrados:", len(df))


validacion = validar_columnas(df)


if not validacion["ok"]:

    print("Faltan columnas:")
    print(validacion["faltantes"])

    raise SystemExit


print("Columnas correctas")
print("Guardando en MySQL...")


resultado_bd = importar_dataframe(df)


if not resultado_bd["ok"]:

    print("ERROR:")
    print(resultado_bd["error"])

else:

    print("")
    print("================================")
    print("IMPORTACIÓN COMPLETADA")
    print("================================")

    print(
        "Empleados procesados:",
        resultado_bd["empleados"]
    )

    print(
        "Marcaciones nuevas:",
        resultado_bd["marcaciones"]
    )

    print(
        "Marcaciones duplicadas:",
        resultado_bd["duplicadas"]
    )