
from database.connection import obtener_conexion
from importacion.hash_marcacion import generar_hash_marcacion
from importacion.validacion_marcaciones import validar_dataframe


def importar_dataframe(df):
    validacion = validar_dataframe(df)

    if not validacion["ok"]:
        return {
            "ok": False,
            "error": "\n".join(validacion["errores"]),
            "empleados": 0,
            "marcaciones": 0,
            "duplicadas": 0
        }
        df = validacion["datos"]

    conexion = None
    cursor = None

    empleados_nuevos = 0
    marcaciones_nuevas = 0
    marcaciones_duplicadas = 0

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        for _, fila in df.iterrows():
            id_usuario = str(fila["ID usuario"]).strip()
            nombre = str(fila["Nombre"]).strip()
            apellido = str(fila["Apellido"]).strip()
            numero_tarjeta = str(
                fila["Número de tarjeta"]
            ).strip()

            fecha_hora = fila["Fecha y tiempo"]

            dispositivo = str(
                fila["Dispositivo"]
            ).strip()

            verificacion = str(
                fila["Verificación"]
            ).strip()

            estado = str(
                fila["Estado"]
            ).strip()

            evento = str(
                fila["Evento"]
            ).strip()

            notas = fila["Notas"]

            if str(notas).lower() == "nan":
                notas = ""
            else:
                notas = str(notas).strip()

            # 1. REGISTRAR EMPLEADO
            sql_empleado = """
                INSERT INTO empleados
                (
                    id_usuario,
                    nombre,
                    apellido,
                    numero_tarjeta
                )
                VALUES (%s, %s, %s, %s)

                ON DUPLICATE KEY UPDATE
                    nombre = VALUES(nombre),
                    apellido = VALUES(apellido),
                    numero_tarjeta = VALUES(numero_tarjeta)
            """

            cursor.execute(
                sql_empleado,
                (
                    id_usuario,
                    nombre,
                    apellido,
                    numero_tarjeta
                )
            )

            if cursor.rowcount == 1:
                empleados_nuevos += 1

            # 2. OBTENER ID DEL EMPLEADO
            cursor.execute(
                """
                SELECT id
                FROM empleados
                WHERE id_usuario = %s
                """,
                (id_usuario,)
            )

            empleado = cursor.fetchone()

            if not empleado:
                raise RuntimeError(
                    f"No se encontró empleado {id_usuario}"
                )

            empleado_id = empleado[0]

            # 3. GENERAR HASH
            hash_marcacion = generar_hash_marcacion(
                id_usuario,
                fecha_hora,
                numero_tarjeta,
                dispositivo,
                evento
            )

            # 4. GUARDAR MARCACIÓN
            sql_marcacion = """
                INSERT IGNORE INTO marcaciones
                (
                    empleado_id,
                    fecha_hora,
                    dispositivo,
                    verificacion,
                    estado,
                    evento,
                    notas,
                    hash_marcacion
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(
                sql_marcacion,
                (
                    empleado_id,
                    fecha_hora,
                    dispositivo,
                    verificacion,
                    estado,
                    evento,
                    notas,
                    hash_marcacion
                )
            )

            if cursor.rowcount == 1:
                marcaciones_nuevas += 1
            else:
                marcaciones_duplicadas += 1

        conexion.commit()

        return {
            "ok": True,
            "empleados": empleados_nuevos,
            "marcaciones": marcaciones_nuevas,
            "duplicadas": marcaciones_duplicadas
        }

    except Exception as e:
        if conexion is not None:
            try:
                conexion.rollback()
            except Exception:
                pass

        return {
            "ok": False,
            "error": str(e),
            "empleados": 0,
            "marcaciones": 0,
            "duplicadas": 0
        }

    finally:
        if cursor is not None:
            try:
                cursor.close()
            except Exception:
                pass

        if conexion is not None:
            try:
                conexion.close()
            except Exception:
                pass
