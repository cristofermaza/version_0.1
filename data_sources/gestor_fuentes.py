from data_sources.fuente_mysql import FuenteMySQL


class GestorFuentes:

    def __init__(self):

        self.fuente_actual = None
        self.tipo_fuente = None

    # ==========================================
    # CONFIGURAR MYSQL
    # ==========================================

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

        self.tipo_fuente = "mysql"

    # ==========================================
    # CARGAR CONFIGURACIÓN
    # ==========================================

    def cargar_desde_configuracion(self, configuracion):

        fuente_datos = configuracion.get(
            "fuente_datos",
            {}
        )

        tipo = fuente_datos.get("tipo")

        if tipo != "mysql":

            self.fuente_actual = None
            self.tipo_fuente = None

            return False

        mysql = fuente_datos.get(
            "mysql",
            {}
        )

        servidor = mysql.get(
            "servidor",
            ""
        )

        puerto = mysql.get(
            "puerto",
            3306
        )

        base_datos = mysql.get(
            "base_datos",
            ""
        )

        usuario = mysql.get(
            "usuario",
            ""
        )

        password = mysql.get(
            "password",
            ""
        )

        if not servidor or not base_datos or not usuario:

            self.fuente_actual = None
            self.tipo_fuente = None

            return False

        self.configurar_mysql(
            servidor=servidor,
            puerto=puerto,
            base_datos=base_datos,
            usuario=usuario,
            password=password
        )

        return True

    # ==========================================
    # CONECTAR
    # ==========================================

    def conectar(self):

        if not self.fuente_actual:
            return False

        return self.fuente_actual.conectar()

    # ==========================================
    # DESCONECTAR
    # ==========================================

    def desconectar(self):

        if self.fuente_actual:
            self.fuente_actual.desconectar()

    # ==========================================
    # ESTADO DE LA FUENTE
    # ==========================================

    def esta_disponible(self):

        if not self.fuente_actual:
            return False

        return self.fuente_actual.esta_disponible()

    # ==========================================
    # OBTENER ERROR
    # ==========================================

    def obtener_error(self):

        if not self.fuente_actual:

            return (
                "No hay una fuente de datos configurada."
            )

        return self.fuente_actual.ultimo_error

    # ==========================================
    # EMPLEADOS
    # ==========================================

    def obtener_empleados(self):

        if not self.esta_disponible():
            return []

        return self.fuente_actual.obtener_empleados()

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

        return self.fuente_actual.crear_empleado(
            id_usuario,
            nombre,
            apellido,
            numero_tarjeta,
            estado
        )

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

        return self.fuente_actual.actualizar_empleado(
            id_usuario_original,
            id_usuario,
            nombre,
            apellido,
            numero_tarjeta,
            estado
        )

    # ==========================================
    # DESACTIVAR EMPLEADO
    # ==========================================

    def desactivar_empleado(self, id_usuario):

        if not self.esta_disponible():

            raise Exception(
                "La fuente de datos no está disponible."
            )

        return self.fuente_actual.desactivar_empleado(
            id_usuario
        )

    # ==========================================
    # ASISTENCIA
    # ==========================================

    def obtener_asistencia(
    self,
    fecha_inicio=None,
    fecha_fin=None):
        
        if not self.esta_disponible():
            return []

        return self.fuente_actual.obtener_asistencia(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
    
     # ==========================================
    # MARCACIONES
    # ==========================================

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
    
     # ==========================================
    # GUARDAR ASISTENCIA
    # ==========================================

    def guardar_asistencia_diaria(self, registros):

        if not self.esta_disponible():
            raise Exception(
                "La fuente de datos no está disponible."
            )

        return self.fuente_actual.guardar_asistencia_diaria(
            registros
        )