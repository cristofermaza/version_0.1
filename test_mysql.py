from database.connection import obtener_conexion


try:

    conexion = obtener_conexion()

    print("================================")
    print("CONEXIÓN EXITOSA")
    print("================================")

    conexion.close()

except Exception as e:

    print("================================")
    print("ERROR DE CONEXIÓN")
    print("================================")
    print(e)