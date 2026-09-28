import mysql.connector


def obtener_conexion():

    conexion = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="sistema_draj"
    )

    return conexion