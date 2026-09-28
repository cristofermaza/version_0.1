from database.connection import obtener_conexion


print("Iniciando prueba...")

try:

    conexion = obtener_conexion()

    print("Conexión a MySQL: OK")

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, id_usuario, nombre, apellido, numero_tarjeta
        FROM empleados
    """)

    resultados = cursor.fetchall()

    print("Cantidad de empleados:", len(resultados))

    print("--------------------------------")

    for empleado in resultados:
        print(empleado)

    print("--------------------------------")

    cursor.close()
    conexion.close()

    print("Prueba terminada.")

except Exception as e:

    print("ERROR:")
    print(e)