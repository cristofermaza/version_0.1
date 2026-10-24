import unittest
from unittest.mock import patch

import pandas as pd

from importacion.database_importer import importar_dataframe
from importacion.excel_reader import COLUMNAS_REQUERIDAS


def crear_dataframe_valido():
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


class TestImportadorSinMySQL(unittest.TestCase):

    @patch("importacion.database_importer.obtener_conexion")
    def test_rechaza_id_vacio_sin_conectarse(self, obtener_conexion):
        df = crear_dataframe_valido()
        df.loc[0, "ID usuario"] = ""

        resultado = importar_dataframe(df)

        self.assertFalse(resultado["ok"])
        self.assertIn("ID usuario", resultado["error"])
        obtener_conexion.assert_not_called()

    @patch("importacion.database_importer.obtener_conexion")
    def test_rechaza_fecha_invalida_sin_conectarse(self, obtener_conexion):
        df = crear_dataframe_valido()
        df.loc[0, "Fecha y tiempo"] = "fecha incorrecta"

        resultado = importar_dataframe(df)

        self.assertFalse(resultado["ok"])
        self.assertIn("fecha(s) inválida(s)", resultado["error"])
        obtener_conexion.assert_not_called()

    @patch("importacion.database_importer.obtener_conexion")
    def test_rechaza_dataframe_vacio_sin_conectarse(self, obtener_conexion):
        df = pd.DataFrame(columns=COLUMNAS_REQUERIDAS)

        resultado = importar_dataframe(df)

        self.assertFalse(resultado["ok"])
        self.assertIn("no contiene marcaciones", resultado["error"])
        obtener_conexion.assert_not_called()

    @patch("importacion.database_importer.obtener_conexion")
    def test_rechaza_columnas_faltantes_sin_conectarse(self, obtener_conexion):
        df = crear_dataframe_valido().drop(columns=["ID usuario"])

        resultado = importar_dataframe(df)

        self.assertFalse(resultado["ok"])
        self.assertIn("ID usuario", resultado["error"])
        obtener_conexion.assert_not_called()


if __name__ == "__main__":
    unittest.main()
