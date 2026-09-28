import mysql.connector

from data_sources.fuente_base import FuenteDatos


class FuenteMySQL(FuenteDatos):

    def __init__(
        self,
        servidor,
        puerto,
        base_datos,
        usuario,
        password
    ):
        self.servidor = servidor
        self.puerto = int(puerto)
        self.base_datos = base_datos
        self.usuario = usuario
        self.password = password

        self.conexion = None
        self.ultimo_error = None

    # ==========================================
    # CONEXIÓN
    # ==========================================

    def conectar(self):
        try:
            self.ultimo_error = None

            self.conexion = mysql.connector.connect(
                host=self.servidor,
                port=self.puerto,
                database=self.base_datos,
                user=self.usuario,
                password=self.password
            )

            return True

        except Exception as error:
            self.conexion = None
            self.ultimo_error = str(error)
            return False

    # ==========================================
    # DESCONECTAR
    # ==========================================

    def desconectar(self):
        if self.conexion:
            try:
                self.conexion.close()
            except Exception:
                pass

        self.conexion = None

    # ==========================================
    # COMPROBAR CONEXIÓN
    # ==========================================

    def esta_disponible(self):
        if not self.conexion:
            return False

        try:
            return self.conexion.is_connected()

        except Exception:
            return False

    # ==========================================
    # OBTENER EMPLEADOS
    # ==========================================

    def obtener_empleados(self):

        if not self.esta_disponible():
            return []

        cursor = self.conexion.cursor(dictionary=True)

        try:

            cursor.execute("""
                SELECT
                    id,
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

    # ==========================================
    # CREAR EMPLEADO
    # ==========================================

    def crear_empleado(
        self,
        id_usuario,
        nombre,
        apellido,
        numero_tarjeta,
        estado
    ):

        if not self.esta_disponible():
            raise Exception(
                "La fuente de datos no está disponible."
            )

        cursor = self.conexion.cursor()

        try:

            cursor.execute("""
                INSERT INTO empleados (
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

            self.conexion.commit()

        except Exception:

            self.conexion.rollback()
            raise

        finally:
            cursor.close()

    # ==========================================
    # ACTUALIZAR EMPLEADO
    # ==========================================

    def actualizar_empleado(
        self,
        id_usuario_original,
        id_usuario,
        nombre,
        apellido,
        numero_tarjeta,
        estado
    ):

        if not self.esta_disponible():
            raise Exception(
                "La fuente de datos no está disponible."
            )

        cursor = self.conexion.cursor()

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

            self.conexion.commit()

        except Exception:

            self.conexion.rollback()
            raise

        finally:
            cursor.close()

    # ==========================================
    # DESACTIVAR EMPLEADO
    # ==========================================

    def desactivar_empleado(self, id_usuario):

        if not self.esta_disponible():
            raise Exception(
                "La fuente de datos no está disponible."
            )

        cursor = self.conexion.cursor()

        try:

            cursor.execute("""
                UPDATE empleados
                SET estado = FALSE
                WHERE id_usuario = %s
            """, (id_usuario,))

            self.conexion.commit()

        except Exception:

            self.conexion.rollback()
            raise

        finally:
            cursor.close()

    # ==========================================
    # OBTENER ASISTENCIA
    # ==========================================

    def obtener_asistencia(
    self,
    fecha_inicio=None,
    fecha_fin=None):
        
        if not self.esta_disponible():
            return []

        cursor = self.conexion.cursor(dictionary=True)

        try:

            consulta = """
                SELECT
                    a.id,
                    a.fecha,
                    e.id_usuario,
                    e.nombre,
                    e.apellido,
                    a.hora_entrada,
                    a.hora_salida,
                    a.estado,
                    a.observaciones
                FROM asistencia_diaria a
                INNER JOIN empleados e
                    ON a.empleado_id = e.id
            """

            condiciones = []
            parametros = []

            if fecha_inicio is not None:

                condiciones.append(
                    "a.fecha >= %s"
                )

                parametros.append(
                    fecha_inicio
                )

            if fecha_fin is not None:

                condiciones.append(
                    "a.fecha < %s"
                )

                parametros.append(
                    fecha_fin
                )

            if condiciones:

                consulta += " WHERE "

                consulta += " AND ".join(
                    condiciones
                )

            consulta += """
                ORDER BY
                    a.fecha DESC,
                    e.apellido,
                    e.nombre
            """

            cursor.execute(
                consulta,
                parametros
            )

            return cursor.fetchall()

        finally:

            cursor.close()
    # ==========================================
    # OBTENER MARCACIONES
    # ==========================================

    def obtener_marcaciones(
    self,
    fecha_inicio=None,
    fecha_fin=None
):
        if not self.esta_disponible():
            return []

        cursor = self.conexion.cursor(dictionary=True)

        try:

            consulta = """
                SELECT
                    id,
                    empleado_id,
                    fecha_hora,
                    dispositivo,
                    verificacion,
                    estado,
                    evento,
                    notas
                FROM marcaciones
            """

            parametros = []

            condiciones = []

            if fecha_inicio is not None:

                condiciones.append(
                    "fecha_hora >= %s"
                )

                parametros.append(
                    fecha_inicio
                )

            if fecha_fin is not None:

                condiciones.append(
                    "fecha_hora < %s"
                )

                parametros.append(
                    fecha_fin
                )

            if condiciones:

                consulta += " WHERE "

                consulta += " AND ".join(
                    condiciones
                )

            consulta += """
                ORDER BY
                    empleado_id,
                    fecha_hora
            """

            cursor.execute(
                consulta,
                parametros
            )

            return cursor.fetchall()

        finally:

            cursor.close()
    # ==========================================
    # GUARDAR ASISTENCIA DIARIA
    # ==========================================

    def guardar_asistencia_diaria(self, registros):

        if not self.esta_disponible():
            raise Exception(
                "La fuente de datos no está disponible."
            )

        if not registros:
            return 0

        cursor = self.conexion.cursor()

        try:

            cantidad = 0

            for registro in registros:

                cursor.execute("""
                    INSERT INTO asistencia_diaria (
                        empleado_id,
                        fecha,
                        hora_entrada,
                        hora_salida,
                        estado,
                        observaciones
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s
                    )
                    ON DUPLICATE KEY UPDATE
                        hora_entrada = VALUES(hora_entrada),
                        hora_salida = VALUES(hora_salida),
                        estado = VALUES(estado),
                        observaciones = VALUES(observaciones)
                """, (
                    registro["empleado_id"],
                    registro["fecha"],
                    registro["hora_entrada"],
                    registro["hora_salida"],
                    registro["estado"],
                    registro["observaciones"]
                ))

                cantidad += 1

            self.conexion.commit()

            return cantidad

        except Exception:

            self.conexion.rollback()
            raise

        finally:
            cursor.close()