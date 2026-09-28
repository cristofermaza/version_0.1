CONFIGURACION = {

    "sistema": {
        "nombre": "SIGEP",
        "descripcion": "Sistema de Gestión de Personal",
        "version": "1.0"
    },

    "empresa": {
        "nombre": "Dirección Regional de Agricultura",
        "nombre_corto": "DRAJ",
        "ruc": "",
        "logo": ""
    },

    "fuente_datos": {
        "tipo": "excel",

        "excel": {
            "carpeta": "",
            "estructura": "Un archivo por trabajador"
        },

        "csv": {
            "archivo": "",
            "separador": ","
        },

        "base_datos": {
            "motor": "MySQL",
            "servidor": "",
            "puerto": "3306",
            "base": "",
            "usuario": "",
            "password": ""
        },

        "api": {
            "url": "",
            "tipo": "REST",
            "token": ""
        }
    },

    "modulos": {
        "personal": True,
        "asistencia": True,
        "permisos": True,
        "incidencias": True,
        "remuneraciones": True,
        "reportes": True
    }
}