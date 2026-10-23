from data_sources.fuente_mysql import FuenteMySQL


class GestorFuentes:

    def __init__(self):
        self.fuente_actual = None
        self.ultimo_error = None

    def configurar_mysql(
        self,
        servidor,
        puerto,
        base_datos,
        usuario,
        password
    ):
        self.fuente_actual = FuenteMySQL(
            servidor=servidor,
            puerto=puerto,
            base_datos=base_datos,
            usuario=usuario,
            password=password
        )

    def cargar_desde_configuracion(self, configuracion):
        self.fuente_actual = None
        self.ultimo_error = None

        fuente_datos = configuracion.get(
            "fuente_datos",
            {}
        )

        tipo = fuente_datos.get("tipo")

        # Configuración actual
        if tipo == "mysql":

            configuracion_mysql = fuente_datos.get(
                "mysql",
                {}
            )

            self.configurar_mysql(
                servidor=configuracion_mysql.get(
                    "servidor",
                    ""
                ),
                puerto=configuracion_mysql.get(
                    "puerto",
                    3306
                ),
                base_datos=configuracion_mysql.get(
                    "base_datos",
                    ""
                ),
                usuario=configuracion_mysql.get(
                    "usuario",
                    ""
                ),
                password=configuracion_mysql.get(
                    "password",
                    ""
                )
            )

        # Compatibilidad con configuraciones antiguas
        elif tipo == "bd":

            configuracion_bd = fuente_datos.get(
                "base_datos",
                {}
            )

            self.configurar_mysql(
                servidor=configuracion_bd.get(
                    "servidor",
                    ""
                ),
                puerto=configuracion_bd.get(
                    "puerto",
                    3306
                ),
                base_datos=configuracion_bd.get(
                    "base",
                    ""
                ),
                usuario=configuracion_bd.get(
                    "usuario",
                    ""
                ),
                password=configuracion_bd.get(
                    "password",
                    ""
                )
            )

    def conectar(self):

        if not self.fuente_actual:
            self.ultimo_error = (
                "No hay una fuente de datos configurada."
            )
            return False

        resultado = self.fuente_actual.conectar()

        if resultado:
            self.ultimo_error = None
        else:
            self.ultimo_error = (
                self.fuente_actual.ultimo_error
            )

        return resultado

    def desconectar(self):

        if self.fuente_actual:
            self.fuente_actual.desconectar()

    def esta_disponible(self):

        if not self.fuente_actual:
            return False

        return self.fuente_actual.esta_disponible()

    def obtener_error(self):

        return self.ultimo_error

    # ---------------------------------------------------------
    # PERSONAL
    # ---------------------------------------------------------

    def obtener_empleados(self):

        if not self.esta_disponible():
            return []

        return self.fuente_actual.obtener_empleados()

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

        return self.fuente_actual.crear_empleado(
            id_usuario=id_usuario,
            nombre=nombre,
            apellido=apellido,
            numero_tarjeta=numero_tarjeta,
            estado=estado,
            fecha_ingreso=fecha_ingreso,
            fecha_cese=fecha_cese
        )

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

        return self.fuente_actual.actualizar_empleado(
            id_usuario_original=id_usuario_original,
            id_usuario=id_usuario,
            nombre=nombre,
            apellido=apellido,
            numero_tarjeta=numero_tarjeta,
            estado=estado,
            fecha_ingreso=fecha_ingreso,
            fecha_cese=fecha_cese
        )

    def desactivar_empleado(self, id_usuario):

        if not self.esta_disponible():
            raise Exception(
                "La fuente de datos no está disponible."
            )

        return self.fuente_actual.desactivar_empleado(
            id_usuario
        )

    # ---------------------------------------------------------
    # ASISTENCIA
    # ---------------------------------------------------------

    def obtener_asistencia(
        self,
        fecha_inicio=None,
        fecha_fin=None
    ):

        if not self.esta_disponible():
            return []

        return self.fuente_actual.obtener_asistencia(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

    def obtener_marcaciones(
        self,
        fecha_inicio=None,
        fecha_fin=None
    ):

        if not self.esta_disponible():
            return []

        return self.fuente_actual.obtener_marcaciones(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

    def guardar_asistencia_diaria(self, registros):

        if not self.esta_disponible():
            raise Exception(
                "La fuente de datos no está disponible."
            )

        return self.fuente_actual.guardar_asistencia_diaria(
            registros
        )

    # ---------------------------------------------------------
    # CALENDARIO
    # ---------------------------------------------------------

    def obtener_calendario_laboral(
        self,
        fecha_inicio=None,
        fecha_fin=None
    ):

        if not self.esta_disponible():
            return []

        return self.fuente_actual.obtener_calendario_laboral(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )