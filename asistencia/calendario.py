from datetime import timedelta


class CalendarioLaboral:

    def es_fin_de_semana(self, fecha):
        return fecha.weekday() >= 5

    def obtener_tipo_dia(self, fecha):
        if self.es_fin_de_semana(fecha):
            return "Fin de semana"

        return "Laborable"

    def es_laborable(self, fecha):
        return not self.es_fin_de_semana(fecha)

    def generar_periodo(self, fecha_inicio, fecha_fin):
        fechas = []

        fecha_actual = fecha_inicio

        while fecha_actual < fecha_fin:

            fechas.append({
                "fecha": fecha_actual,
                "tipo_dia": self.obtener_tipo_dia(
                    fecha_actual
                ),
                "descripcion": None,
                "es_laborable": self.es_laborable(
                    fecha_actual
                )
            })

            fecha_actual += timedelta(days=1)

        return fechas

    def aplicar_excepciones(
        self,
        fechas,
        excepciones
    ):
        indice = {
            registro["fecha"]: registro
            for registro in fechas
        }

        for excepcion in excepciones:

            fecha = excepcion.get("fecha")

            if fecha not in indice:
                continue

            indice[fecha]["tipo_dia"] = excepcion.get(
                "tipo_dia",
                indice[fecha]["tipo_dia"]
            )

            indice[fecha]["descripcion"] = excepcion.get(
                "descripcion"
            )

            indice[fecha]["es_laborable"] = bool(
                excepcion.get(
                    "es_laborable",
                    indice[fecha]["es_laborable"]
                )
            )

        return list(indice.values())