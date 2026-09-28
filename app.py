import sys

from PySide6.QtWidgets import QApplication

from ui.ventana_principal import VentanaPrincipal
from ui.estilos import ESTILO_APLICACION

from config.gestor_configuracion import GestorConfiguracion
from data_sources.gestor_fuentes import GestorFuentes


app = QApplication(sys.argv)

app.setStyleSheet(ESTILO_APLICACION)


# ==========================================
# CARGAR CONFIGURACIÓN GUARDADA
# ==========================================

gestor_configuracion = GestorConfiguracion()

configuracion = gestor_configuracion.cargar()


# ==========================================
# CONFIGURAR FUENTE DE DATOS
# ==========================================

gestor_fuentes = GestorFuentes()

gestor_fuentes.cargar_desde_configuracion(configuracion)


# ==========================================
# CONECTAR AUTOMÁTICAMENTE
# ==========================================

if gestor_fuentes.fuente_actual:

    if gestor_fuentes.conectar():

        print("CONEXION EXITOSA")

    else:

        print("NO SE PUDO CONECTAR A LA FUENTE DE DATOS")
        print(gestor_fuentes.obtener_error())

else:

    print("NO HAY FUENTE DE DATOS CONFIGURADA")


# ==========================================
# ABRIR VENTANA PRINCIPAL
# ==========================================

ventana = VentanaPrincipal(
    gestor_fuentes,
    gestor_configuracion
)

ventana.show()


# ==========================================
# INICIAR APLICACIÓN
# ==========================================

sys.exit(app.exec())