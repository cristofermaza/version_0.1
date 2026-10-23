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

        cursor = self.conexion.cursor(
            dictionary=True
        )

        try:

            cursor.execute("""
                SELECT
                    id,
                    id_usuario,
                    nombre,
                    apellido,
                    numero_tarjeta,
                    fecha_ingreso,
                    fecha_cese,
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
        estado=True,
        fecha_ingreso=None,
        fecha_cese=None
    ):

        if not self.esta_disponible():
            raise Exception(
                "La fuente de datos no está disponible."
            )

        cursor = self.conexion.cursor()

        try:

            consulta = """
                INSERT INTO empleados (
                    id_usuario,
                    nombre,
                    apellido,
                    numero_tarjeta,
                    fecha_ingreso,
                    fecha_cese,
                    estado
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s
                )
            """

            cursor.execute(
                consulta,
                (
                    id_usuario,
                    nombre,
                    apellido,
                    numero_tarjeta,
                    fecha_ingreso,
                    fecha_cese,
                    estado
                )
            )

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
        estado=True,
        fecha_ingreso=None,
        fecha_cese=None
    ):

        if not self.esta_disponible():
            raise Exception(
                "La fuente de datos no está disponible."
            )

        cursor = self.conexion.cursor()

        try:

            consulta = """
                UPDATE empleados
                SET
                    id_usuario = %s,
                    nombre = %s,
                    apellido = %s,
                    numero_tarjeta = %s,
                    fecha_ingreso = %s,
                    fecha_cese = %s,
                    estado = %s
                WHERE id_usuario = %s
            """

            cursor.execute(
                consulta,
                (
                    id_usuario,
                    nombre,
                    apellido,
                    numero_tarjeta,
                    fecha_ingreso,
                    fecha_cese,
                    estado,
                    id_usuario_original
                )
            )

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
        fecha_fin=None
    ):

        if not self.esta_disponible():
            return []

        cursor = self.conexion.cursor(
            dictionary=True
        )

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

        cursor = self.conexion.cursor(
            dictionary=True
        )

        try:

            consulta = """
                SELECT
                    m.id,
                    m.empleado_id,
                    m.fecha_hora,
                    m.dispositivo,
                    m.verificacion,
                    m.estado,
                    m.evento,
                    m.notas,
                    e.id_usuario,
                    e.nombre,
                    e.apellido,
                    e.fecha_ingreso,
                    e.fecha_cese
                FROM marcaciones m
                INNER JOIN empleados e
                    ON m.empleado_id = e.id
            """

            condiciones = []
            parametros = []

            if fecha_inicio is not None:

                condiciones.append(
                    "m.fecha_hora >= %s"
                )

                parametros.append(
                    fecha_inicio
                )

            if fecha_fin is not None:

                condiciones.append(
                    "m.fecha_hora < %s"
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
                    m.empleado_id,
                    m.fecha_hora
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

    def guardar_asistencia_diaria(
        self,
        registros
    ):

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

    # ==========================================
    # OBTENER CALENDARIO LABORAL
    # ==========================================

    def obtener_calendario_laboral(
        self,
        fecha_inicio=None,
        fecha_fin=None
    ):

        if not self.esta_disponible():
            return []

        cursor = self.conexion.cursor(
            dictionary=True
        )

        try:

            consulta = """
                SELECT
                    id,
                    fecha,
                    tipo_dia,
                    descripcion,
                    es_laborable
                FROM calendario_laboral
            """

            condiciones = []
            parametros = []

            if fecha_inicio is not None:

                condiciones.append(
                    "fecha >= %s"
                )

                parametros.append(
                    fecha_inicio
                )

            if fecha_fin is not None:

                condiciones.append(
                    "fecha < %s"
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
                ORDER BY fecha
            """

            cursor.execute(
                consulta,
                parametros
            )

            return cursor.fetchall()

        finally:
            cursor.close()

    # ==========================================
    # OBTENER TIPOS DE PERMISOS
    # ==========================================

    def obtener_tipos_permisos(
        self,
        solo_activos=True
    ):

        if not self.esta_disponible():
            return []

        cursor = self.conexion.cursor(
            dictionary=True
        )

        try:

            consulta = """
                SELECT
                    id,
                    codigo,
                    nombre,
                    descripcion,
                    afecta_asistencia,
                    requiere_aprobacion,
                    remunerado,
                    activo
                FROM tipos_permisos
            """

            parametros = []

            if solo_activos:

                consulta += """
                    WHERE activo = TRUE
                """

            consulta += """
                ORDER BY nombre
            """

            cursor.execute(
                consulta,
                parametros
            )

            return cursor.fetchall()

        finally:
            cursor.close()

    # ==========================================
    # CREAR TIPO DE PERMISO
    # ==========================================

    def crear_tipo_permiso(
        self,
        codigo,
        nombre,
        descripcion=None,
        afecta_asistencia=True,
        requiere_aprobacion=True,
        remunerado=True
    ):

        if not self.esta_disponible():
            raise Exception(
                "La fuente de datos no está disponible."
            )

        cursor = self.conexion.cursor()

        try:

            consulta = """
                INSERT INTO tipos_permisos (
                    codigo,
                    nombre,
                    descripcion,
                    afecta_asistencia,
                    requiere_aprobacion,
                    remunerado,
                    activo
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, TRUE
                )
            """

            cursor.execute(
                consulta,
                (
                    codigo,
                    nombre,
                    descripcion,
                    afecta_asistencia,
                    requiere_aprobacion,
                    remunerado
                )
            )

            self.conexion.commit()

        except Exception:

            self.conexion.rollback()
            raise

        finally:
            cursor.close()

    # ==========================================
    # ACTUALIZAR TIPO DE PERMISO
    # ==========================================

    def actualizar_tipo_permiso(
        self,
        id_tipo_permiso,
        codigo,
        nombre,
        descripcion=None,
        afecta_asistencia=True,
        requiere_aprobacion=True,
        remunerado=True
    ):

        if not self.esta_disponible():
            raise Exception(
                "La fuente de datos no está disponible."
            )

        cursor = self.conexion.cursor()

        try:

            consulta = """
                UPDATE tipos_permisos
                SET
                    codigo = %s,
                    nombre = %s,
                    descripcion = %s,
                    afecta_asistencia = %s,
                    requiere_aprobacion = %s,
                    remunerado = %s
                WHERE id = %s
            """

            cursor.execute(
                consulta,
                (
                    codigo,
                    nombre,
                    descripcion,
                    afecta_asistencia,
                    requiere_aprobacion,
                    remunerado,
                    id_tipo_permiso
                )
            )

            self.conexion.commit()

        except Exception:

            self.conexion.rollback()
            raise

        finally:
            cursor.close()

    # ==========================================
    # DESACTIVAR TIPO DE PERMISO
    # ==========================================

    def desactivar_tipo_permiso(
        self,
        id_tipo_permiso
    ):

        if not self.esta_disponible():
            raise Exception(
                "La fuente de datos no está disponible."
            )

        cursor = self.conexion.cursor()

        try:

            cursor.execute(
                """
                UPDATE tipos_permisos
                SET activo = FALSE
                WHERE id = %s
                """,
                (id_tipo_permiso,)
            )

            self.conexion.commit()

        except Exception:

            self.conexion.rollback()
            raise

        finally:
            cursor.close()