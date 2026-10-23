import tempfile
import unittest
from pathlib import Path

import pandas as pd

from importacion.excel_reader import (
    COLUMNAS_REQUERIDAS,
    leer_excel,
    validar_columnas,
)


class TestValidacionColumnas(unittest.TestCase):

    def test_acepta_todas_las_columnas_requeridas(self):
        df = pd.DataFrame(columns=COLUMNAS_REQUERIDAS)

        resultado = validar_columnas(df)

        self.assertTrue(resultado["ok"])
        self.assertEqual(resultado["faltantes"], [])

    def test_detecta_columnas_faltantes(self):
        columnas = [
            columna
            for columna in COLUMNAS_REQUERIDAS
            if columna != "Notas"
        ]
        df = pd.DataFrame(columns=columnas)

        resultado = validar_columnas(df)

        self.assertFalse(resultado["ok"])
        self.assertEqual(resultado["faltantes"], ["Notas"])

    def test_detecta_varias_columnas_faltantes(self):
        columnas = ["Nombre", "Apellido"]
        df = pd.DataFrame(columns=columnas)

        resultado = validar_columnas(df)

        self.assertFalse(resultado["ok"])
        self.assertEqual(
            resultado["faltantes"],
            [
                columna
                for columna in COLUMNAS_REQUERIDAS
                if columna not in columnas
            ],
        )
        
    def test_detecta_nombres_de_columnas_con_espacios(self):
        columnas = [
            columna if columna != "Nombre" else " Nombre "
            for columna in COLUMNAS_REQUERIDAS
        ]
        df = pd.DataFrame(columns=columnas)

        resultado = validar_columnas(df)

        self.assertFalse(resultado["ok"])
        self.assertIn("Nombre", resultado["faltantes"])

    def test_no_falla_con_dataframe_vacio(self):
        df = pd.DataFrame(columns=COLUMNAS_REQUERIDAS)

        resultado = validar_columnas(df)

        self.assertTrue(resultado["ok"])
        self.assertEqual(resultado["faltantes"], [])


class TestLecturaExcel(unittest.TestCase):

    def test_lee_excel_valido(self):
        datos = pd.DataFrame({
            "ID usuario": ["001"],
            "Nombre": ["Juan"],
            "Apellido": ["Pérez"],
        })

        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "prueba.xlsx"
            datos.to_excel(ruta, index=False)

            resultado = leer_excel(ruta)

        self.assertTrue(resultado["ok"])
        self.assertIsNone(resultado["error"])
        self.assertEqual(len(resultado["datos"]), 1)
        self.assertEqual(
            resultado["datos"].iloc[0]["Nombre"],
            "Juan",
        )

    def test_informa_error_si_el_archivo_no_existe(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "no_existe.xlsx"

            resultado = leer_excel(ruta)

        self.assertFalse(resultado["ok"])
        self.assertIsNone(resultado["datos"])
        self.assertTrue(resultado["error"])

    def test_informa_error_si_el_archivo_es_invalido(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "invalido.xlsx"
            ruta.write_text(
                "Esto no es un archivo Excel",
                encoding="utf-8",
            )

            resultado = leer_excel(ruta)

        self.assertFalse(resultado["ok"])
        self.assertIsNone(resultado["datos"])
        self.assertTrue(resultado["error"])


if __name__ == "__main__":
    unittest.main()
