import json
from pathlib import Path


CONFIGURACION_POR_DEFECTO = {
    "asistencia": {
        "horario": {
            "hora_entrada": "08:00",
            "hora_salida": "17:00"
        },
        "tolerancia": {
            "minutos_entrada": 0
        },
        "reglas": {
            "primera_marcacion_es_entrada": True,
            "ultima_marcacion_es_salida": True,
            "generar_salida_si_solo_hay_una_marcacion": False
        }
    }
}


class GestorConfiguracion:

    def __init__(self):
        self.archivo = (
            Path(__file__).resolve().parent
            / "configuracion.json"
        )

    # ==========================================
    # CARGAR
    # ==========================================

    def cargar(self):

        if not self.archivo.exists():
            return self._configuracion_por_defecto()

        try:

            with open(
                self.archivo,
                "r",
                encoding="utf-8"
            ) as archivo:

                configuracion = json.load(
                    archivo
                )

            return self._completar_configuracion(
                configuracion
            )

        except (
            json.JSONDecodeError,
            OSError
        ):

            return self._configuracion_por_defecto()

    # ==========================================
    # GUARDAR
    # ==========================================

    def guardar(self, configuracion):

        try:

            configuracion = (
                self._completar_configuracion(
                    configuracion
                )
            )

            with open(
                self.archivo,
                "w",
                encoding="utf-8"
            ) as archivo:

                json.dump(
                    configuracion,
                    archivo,
                    indent=4,
                    ensure_ascii=False
                )

            return True

        except OSError:

            return False

    # ==========================================
    # COMPLETAR CONFIGURACIÓN
    # ==========================================

    def _completar_configuracion(
        self,
        configuracion
    ):

        if not isinstance(
            configuracion,
            dict
        ):
            configuracion = {}

        asistencia = configuracion.setdefault(
            "asistencia",
            {}
        )

        horario = asistencia.setdefault(
            "horario",
            {}
        )

        horario.setdefault(
            "hora_entrada",
            "08:00"
        )

        horario.setdefault(
            "hora_salida",
            "17:00"
        )

        tolerancia = asistencia.setdefault(
            "tolerancia",
            {}
        )

        tolerancia.setdefault(
            "minutos_entrada",
            0
        )

        reglas = asistencia.setdefault(
            "reglas",
            {}
        )

        reglas.setdefault(
            "primera_marcacion_es_entrada",
            True
        )

        reglas.setdefault(
            "ultima_marcacion_es_salida",
            True
        )

        reglas.setdefault(
            "generar_salida_si_solo_hay_una_marcacion",
            False
        )

        return configuracion

    # ==========================================
    # CONFIGURACIÓN POR DEFECTO
    # ==========================================

    def _configuracion_por_defecto(self):

        return {
            "asistencia": {
                "horario": {
                    "hora_entrada": "08:00",
                    "hora_salida": "17:00"
                },
                "tolerancia": {
                    "minutos_entrada": 0
                },
                "reglas": {
                    "primera_marcacion_es_entrada": True,
                    "ultima_marcacion_es_salida": True,
                    "generar_salida_si_solo_hay_una_marcacion": False
                }
            }
        }