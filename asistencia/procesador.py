from datetime import datetime, time, timedelta


class ProcesadorAsistencia:

    def __init__(
        self,
        hora_entrada="08:00",
        hora_salida="17:00",
        tolerancia_entrada=0,
        primera_marcacion_es_entrada=True,
        ultima_marcacion_es_salida=True,
        generar_salida_si_solo_hay_una_marcacion=False
    ):
        self.hora_entrada = self._convertir_hora(hora_entrada)
        self.hora_salida = self._convertir_hora(hora_salida)

        self.tolerancia_entrada = int(tolerancia_entrada)

        self.primera_marcacion_es_entrada = bool(
            primera_marcacion_es_entrada
        )

        self.ultima_marcacion_es_salida = bool(
            ultima_marcacion_es_salida
        )

        self.generar_salida_si_solo_hay_una_marcacion = bool(
            generar_salida_si_solo_hay_una_marcacion
        )

    def _convertir_hora(self, valor):

        if isinstance(valor, time):
            return valor

        if isinstance(valor, str):

            partes = valor.strip().split(":")

            if len(partes) >= 2:

                hora = int(partes[0])
                minuto = int(partes[1])

                return time(hora, minuto)

        raise ValueError(f"Hora no válida: {valor}")

    def procesar(self, marcaciones):

        grupos = {}

        for marcacion in marcaciones:

            fecha_hora = marcacion.get("fecha_hora")
            empleado_id = marcacion.get("empleado_id")

            if not fecha_hora or not empleado_id:
                continue

            if isinstance(fecha_hora, str):

                try:
                    fecha_hora = datetime.fromisoformat(fecha_hora)

                except ValueError:
                    continue

            fecha = fecha_hora.date()

            clave = (empleado_id, fecha)

            grupos.setdefault(clave, []).append(fecha_hora)

        resultados = []

        for (empleado_id, fecha), marcas in grupos.items():

            marcas.sort()

            hora_entrada = None
            hora_salida = None

            # --------------------------------------------------
            # ENTRADA
            # --------------------------------------------------

            if self.primera_marcacion_es_entrada:

                hora_entrada = marcas[0]

            # --------------------------------------------------
            # SALIDA
            # --------------------------------------------------

            if len(marcas) >= 2:

                if self.ultima_marcacion_es_salida:
                    hora_salida = marcas[-1]

            elif len(marcas) == 1:

                if self.generar_salida_si_solo_hay_una_marcacion:

                    hora_salida = datetime.combine(
                        fecha,
                        self.hora_salida
                    )

            estado = self.determinar_estado(
                hora_entrada,
                hora_salida
            )

            observaciones = self.generar_observaciones(
                hora_entrada,
                hora_salida
            )

            resultados.append({
                "empleado_id": empleado_id,
                "fecha": fecha,
                "hora_entrada": hora_entrada,
                "hora_salida": hora_salida,
                "estado": estado,
                "observaciones": observaciones
            })

        resultados.sort(
            key=lambda registro: (
                registro["fecha"],
                registro["empleado_id"]
            )
        )

        return resultados

    def determinar_estado(
        self,
        hora_entrada,
        hora_salida
    ):

        if not hora_entrada:

            return "Sin entrada"

        limite_tardanza = (
            datetime.combine(
                hora_entrada.date(),
                self.hora_entrada
            )
            + timedelta(minutes=self.tolerancia_entrada)
        )

        entrada_tardia = hora_entrada > limite_tardanza

        salida_anticipada = False

        if hora_salida:

            hora_salida_esperada = datetime.combine(
                hora_salida.date(),
                self.hora_salida
            )

            salida_anticipada = (
                hora_salida < hora_salida_esperada
            )

        if entrada_tardia and salida_anticipada:
            return "Tardanza y salida anticipada"

        if entrada_tardia:
            return "Tardanza"

        if salida_anticipada:
            return "Salida anticipada"

        if not hora_salida:
            return "Entrada registrada"

        return "Normal"

    def generar_observaciones(
        self,
        hora_entrada,
        hora_salida
    ):

        observaciones = []

        if hora_entrada:

            limite_tardanza = (
                datetime.combine(
                    hora_entrada.date(),
                    self.hora_entrada
                )
                + timedelta(minutes=self.tolerancia_entrada)
            )

            if hora_entrada > limite_tardanza:

                minutos_tarde = int(
                    (
                        hora_entrada - limite_tardanza
                    ).total_seconds() / 60
                )

                observaciones.append(
                    f"Ingreso posterior al horario establecido "
                    f"({minutos_tarde} min.)"
                )

        if hora_salida:

            hora_salida_esperada = datetime.combine(
                hora_salida.date(),
                self.hora_salida
            )

            if hora_salida < hora_salida_esperada:

                minutos_antes = int(
                    (
                        hora_salida_esperada - hora_salida
                    ).total_seconds() / 60
                )

                observaciones.append(
                    f"Salida anticipada ({minutos_antes} min.)"
                )

        else:

            observaciones.append(
                "No se registró salida"
            )

        return "; ".join(observaciones)