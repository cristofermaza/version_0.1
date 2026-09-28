from database.connection import obtener_conexion


try:

    conexion = obtener_conexion()

    print("Conexión establecida")

    cursor = conexion.cursor()

    sql = """
    INSERT INTO empleados
    (id_usuario, nombre, apellido, numero_tarjeta)
    VALUES (%s, %s, %s, %s)
    """

    datos = (
        "TEST001",
        "Juan",
        "Perez",
        "10001"
    )

    cursor.execute(sql, datos)

    conexion.commit()

    print("Empleado registrado correctamente")
    print("ID generado:", cursor.lastrowid)

    cursor.close()
    conexion.close()

except Exception as e:

    print("ERROR:")
    print(e)