from asistencia.procesador import procesar_asistencia


print("================================")
print("PROCESAMIENTO DE ASISTENCIA")
print("================================")

resultado = procesar_asistencia()

if resultado["ok"]:

    print("Procesamiento completado")
    print(
        "Registros diarios:",
        resultado["registros"]
    )

else:

    print("ERROR:")
    print(resultado["error"])