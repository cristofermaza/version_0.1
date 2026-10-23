import unittest

import pandas as pd

from importacion.excel_reader import COLUMNAS_REQUERIDAS
from importacion.validacion_marcaciones import validar_dataframe


def crear_dataframe():
    return pd.DataFrame([{
        "Fecha y tiempo": "2026-09-01 08:00:00",
        "ID usuario": "001",
        "Nombre": "Juan",
        "Apellido": "Pérez",
        "Número de tarjeta": "123",
        "Dispositivo": "Biométrico 01",
        "Verificación": "Huella",
        "Estado": "Entrada",
        "Evento": "Marcación",
        "Notas": "",
    }], columns=COLUMNAS_REQUERIDAS)


class TestValidacionMarcaciones(unittest.TestCase):

    def test_acepta_marcacion_valida(self):
        resultado = validar_dataframe(crear_dataframe())

        self.assertTrue(resultado["ok"])
        self.assertEqual(resultado["errores"], [])

    def test_rechaza_dataframe_vacio(self):
        df = pd.DataFrame(columns=COLUMNAS_REQUERIDAS)

        resultado = validar_dataframe(df)

        self.assertFalse(resultado["ok"])
        self.assertTrue(resultado["errores"])

    def test_detecta_id_usuario_vacio(self):
        df = crear_dataframe()
        df.loc[0, "ID usuario"] = ""

        resultado = validar_dataframe(df)

        self.assertFalse(resultado["ok"])
        self.assertTrue(
            any("ID usuario" in error for error in resultado["errores"])
        )

    def test_detecta_fecha_invalida(self):
        df = crear_dataframe()
        df.loc[0, "Fecha y tiempo"] = "fecha incorrecta"

        resultado = validar_dataframe(df)

        self.assertFalse(resultado["ok"])
        self.assertTrue(
            any("fecha(s) inválida(s)" in error
                for error in resultado["errores"])
        )

    def test_ignora_filas_completamente_vacias(self):
        df = crear_dataframe()
        df.loc[1] = [None] * len(COLUMNAS_REQUERIDAS)

        resultado = validar_dataframe(df)

        self.assertTrue(resultado["ok"])
        self.assertEqual(resultado["errores"], [])


if __name__ == "__main__":
    unittest.main()
