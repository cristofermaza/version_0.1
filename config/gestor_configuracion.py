import json
from pathlib import Path


CONFIGURACION_POR_DEFECTO = {
    "organizacion": {
        "nombre": "",
        "codigo": "",
        "direccion": "",
        "telefono": ""
    },

    "fuente_datos": {
        "tipo": "mysql",

        "mysql": {
            "servidor": "localhost",
            "puerto": 3306,
            "base_datos": "",
            "usuario": "",
            "password": ""
        }
    },

    "importacion": {
        "tipo": "excel",
        "modo": "carpeta",
        "extensiones": [
            ".xlsx",
            ".xls"
        ]
    },

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
    },

    "permisos": {
        "habilitado": True
    },

    "remuneraciones": {
        "habilitado": True
    },

    "reportes": {
        "formato_predeterminado": "PDF"
    },

    "seguridad": {
        "sesion_habilitada": False
    },

    "sistema": {
        "idioma": "es",
        "tema": "institucional"
    }
}


class GestorConfiguracion:

    def __init__(self):
        self.archivo = (
            Path(__file__).resolve().parent
            / "configuracion.json"
        )

    def cargar(self):

        if not self.archivo.exists():
            configuracion = self._configuracion_por_defecto()
            self.guardar(configuracion)
            return configuracion

        try:

            with open(
                self.archivo,
                "r",
                encoding="utf-8"
            ) as archivo:

                configuracion = json.load(archivo)

            return self._completar_configuracion(
                configuracion
            )

        except (
            json.JSONDecodeError,
            OSError
        ):

            return self._configuracion_por_defecto()

    def guardar(self, configuracion):

        try:

            configuracion = self._completar_configuracion(
                configuracion
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

    def _completar_configuracion(
        self,
        configuracion
    ):

        if not isinstance(
            configuracion,
            dict
        ):
            configuracion = {}

        return self._fusionar_configuracion(
            CONFIGURACION_POR_DEFECTO,
            configuracion
        )

    def _fusionar_configuracion(
        self,
        valores_por_defecto,
        valores_actuales
    ):

        resultado = {}

        for clave, valor_defecto in (
            valores_por_defecto.items()
        ):

            if clave not in valores_actuales:

                if isinstance(
                    valor_defecto,
                    dict
                ):

                    resultado[clave] = (
                        self._fusionar_configuracion(
                            valor_defecto,
                            {}
                        )
                    )

                elif isinstance(
                    valor_defecto,
                    list
                ):

                    resultado[clave] = list(
                        valor_defecto
                    )

                else:

                    resultado[clave] = valor_defecto

                continue

            valor_actual = valores_actuales[clave]

            if (
                isinstance(
                    valor_defecto,
                    dict
                )
                and isinstance(
                    valor_actual,
                    dict
                )
            ):

                resultado[clave] = (
                    self._fusionar_configuracion(
                        valor_defecto,
                        valor_actual
                    )
                )

            else:

                resultado[clave] = valor_actual

        # Conservamos configuraciones adicionales
        # que puedan existir.
        for clave, valor in valores_actuales.items():

            if clave not in resultado:

                resultado[clave] = valor

        return resultado

    def _configuracion_por_defecto(self):

        return self._fusionar_configuracion(
            CONFIGURACION_POR_DEFECTO,
            {}
        )