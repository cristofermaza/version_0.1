
import mysql.connector

from config.gestor_configuracion import GestorConfiguracion


def obtener_conexion():
    gestor_configuracion = GestorConfiguracion()
    configuracion = gestor_configuracion.cargar()

    if not isinstance(configuracion, dict):
        raise ValueError(
            "La configuración de SIGEP no tiene un formato válido."
        )

    fuente_datos = configuracion.get("fuente_datos", {})

    if not isinstance(fuente_datos, dict):
        raise ValueError(
            "La configuración de la fuente de datos no es válida."
        )

    tipo = fuente_datos.get("tipo", "mysql")

    if tipo != "mysql":
        raise ValueError(
            f"La importación requiere MySQL. Fuente configurada: {tipo}"
        )

    config_mysql = fuente_datos.get("mysql", {})

    if not isinstance(config_mysql, dict):
        raise ValueError(
            "La configuración de MySQL no es válida."
        )

    servidor = config_mysql.get("servidor", "")
    base_datos = config_mysql.get("base_datos", "")
    usuario = config_mysql.get("usuario", "")

    if not all(
        isinstance(valor, str) and valor.strip()
        for valor in (servidor, base_datos, usuario)
    ):
        raise ValueError(
            "Configura un servidor, una base de datos y un usuario "
            "válidos en SIGEP antes de importar."
        )

    puerto = config_mysql.get("puerto", 3306)

    try:
        puerto = int(puerto)
    except (TypeError, ValueError):
        raise ValueError(
            "El puerto de MySQL debe ser un número entero."
        ) from None

    if not 1 <= puerto <= 65535:
        raise ValueError(
            "El puerto de MySQL debe estar entre 1 y 65535."
        )

    password = config_mysql.get("password", "")

    if not isinstance(password, str):
        raise ValueError(
            "La contraseña de MySQL debe ser texto."
        )

    return mysql.connector.connect(
        host=servidor.strip(),
        port=puerto,
        user=usuario.strip(),
        password=password,
        database=base_datos.strip()
    )
