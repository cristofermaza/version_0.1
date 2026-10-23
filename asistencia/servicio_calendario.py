from asistencia.calendario import CalendarioLaboral


class ServicioCalendario:

    def __init__(self, gestor_fuentes):

        self.gestor_fuentes = gestor_fuentes

        self.calendario = CalendarioLaboral()

    def obtener_periodo(
        self,
        fecha_inicio,
        fecha_fin
    ):

        if not self.gestor_fuentes.esta_disponible():

            raise Exception(
                "La fuente de datos no está disponible."
            )

        registros = (
            self.gestor_fuentes
            .obtener_calendario_laboral(
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
        )

        return registros

    def generar_periodo(
        self,
        fecha_inicio,
        fecha_fin
    ):

        return self.calendario.generar_periodo(
            fecha_inicio,
            fecha_fin
        )

    def obtener_calendario_completo(
        self,
        fecha_inicio,
        fecha_fin
    ):

        calendario_base = self.generar_periodo(
            fecha_inicio,
            fecha_fin
        )

        excepciones = self.obtener_periodo(
            fecha_inicio,
            fecha_fin
        )

        return self.calendario.aplicar_excepciones(
            calendario_base,
            excepciones
        )