class ClasificadorAsistencia:

    def __init__(self, procesador=None):
        self.procesador = procesador

    def clasificar(self, registro):
        marcas = registro.get("marcaciones", [])

        if not marcas:
            return {
                **registro,
                "estado": "Sin marcación",
                "hora_entrada": None,
                "hora_salida": None,
                "observaciones": (
                    "No se encontraron marcaciones para este día."
                )
            }

        marcas = sorted(
            marcas,
            key=lambda marcacion: marcacion["fecha_hora"]
        )

        hora_entrada = marcas[0]["fecha_hora"]
        hora_salida = None

        if len(marcas) >= 2:
            hora_salida = marcas[-1]["fecha_hora"]

        # Si tenemos ProcesadorAsistencia,
        # utilizamos sus reglas reales.
        if self.procesador is not None:

            resultado_procesado = self.procesador.determinar_estado(
                hora_entrada,
                hora_salida
            )

            observaciones = self.procesador.generar_observaciones(
                hora_entrada,
                hora_salida
            )

            estado = resultado_procesado

        else:

            estado = "Normal"
            observaciones = ""

            if len(marcas) == 1:
                estado = "Entrada registrada"
                observaciones = (
                    "Solo existe una marcación para este día."
                )

        return {
            **registro,
            "estado": estado,
            "hora_entrada": hora_entrada,
            "hora_salida": hora_salida,
            "observaciones": observaciones
        }

    def clasificar_todos(self, registros):

        resultado = []

        for registro in registros:
            resultado.append(
                self.clasificar(registro)
            )

        return resultado