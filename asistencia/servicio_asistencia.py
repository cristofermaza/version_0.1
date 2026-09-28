from asistencia.procesador import ProcesadorAsistencia


class ServicioAsistencia:

    def __init__(
        self,
        gestor_fuentes,
        gestor_configuracion
    ):

        self.gestor_fuentes = gestor_fuentes
        self.gestor_configuracion = (
            gestor_configuracion
        )

        configuracion = (
            self.gestor_configuracion.cargar()
        )

        configuracion_asistencia = (
            configuracion.get(
                "asistencia",
                {}
            )
        )

        horario = (
            configuracion_asistencia.get(
                "horario",
                {}
            )
        )

        tolerancia = (
            configuracion_asistencia.get(
                "tolerancia",
                {}
            )
        )

        self.procesador = ProcesadorAsistencia(

            hora_entrada=horario.get(
                "hora_entrada",
                "08:00"
            ),

            hora_salida=horario.get(
                "hora_salida",
                "17:00"
            ),

            tolerancia_entrada=tolerancia.get(
                "minutos_entrada",
                0
            )
        )

    # ==========================================
    # PROCESAR ASISTENCIA
    # ==========================================

    def procesar_asistencia(
    self,
    fecha_inicio=None,
    fecha_fin=None
):

        if not self.gestor_fuentes.esta_disponible():

            raise Exception(
                "La fuente de datos no está disponible."
            )

        marcaciones = (
            self.gestor_fuentes.obtener_marcaciones(
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
        )

        if not marcaciones:
            return 0

        registros = (
            self.procesador.procesar(
                marcaciones
            )
        )

        if not registros:
            return 0

        return (
            self.gestor_fuentes.guardar_asistencia_diaria(
                registros
            )
        )