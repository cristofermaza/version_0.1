from database.connection import obtener_conexion


def obtener_empleados():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        cursor.execute("""
            SELECT
                id_usuario,
                nombre,
                apellido,
                numero_tarjeta,
                estado
            FROM empleados
            ORDER BY apellido, nombre
        """)

        return cursor.fetchall()

    finally:

        cursor.close()
        conexion.close()


def crear_empleado(
    id_usuario,
    nombre,
    apellido,
    numero_tarjeta,
    estado
):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        cursor.execute("""
            INSERT INTO empleados
            (
                id_usuario,
                nombre,
                apellido,
                numero_tarjeta,
                estado
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            id_usuario,
            nombre,
            apellido,
            numero_tarjeta,
            estado
        ))

        conexion.commit()

    finally:

        cursor.close()
        conexion.close()


def actualizar_empleado(
    id_usuario_original,
    id_usuario,
    nombre,
    apellido,
    numero_tarjeta,
    estado
):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        cursor.execute("""
            UPDATE empleados
            SET
                id_usuario = %s,
                nombre = %s,
                apellido = %s,
                numero_tarjeta = %s,
                estado = %s
            WHERE id_usuario = %s
        """, (
            id_usuario,
            nombre,
            apellido,
            numero_tarjeta,
            estado,
            id_usuario_original
        ))

        conexion.commit()

    finally:

        cursor.close()
        conexion.close()


def desactivar_empleado(id_usuario):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        cursor.execute("""
            UPDATE empleados
            SET estado = FALSE
            WHERE id_usuario = %s
        """, (
            id_usuario,
        ))

        conexion.commit()

    finally:

        cursor.close()
        conexion.close()