import sys

from PySide6.QtWidgets import QApplication

from ui.ventana_principal import VentanaPrincipal
from ui.estilos import ESTILO_APLICACION

from config.gestor_configuracion import GestorConfiguracion
from data_sources.gestor_fuentes import GestorFuentes


app = QApplication(sys.argv)

app.setStyleSheet(ESTILO_APLICACION)

gestor_configuracion = GestorConfiguracion()
configuracion = gestor_configuracion.cargar()

gestor_fuentes = GestorFuentes()
gestor_fuentes.cargar_desde_configuracion(configuracion)


if gestor_fuentes.fuente_actual:

    if gestor_fuentes.conectar():

        print("CONEXION EXITOSA")
        print("PASO 1: conexión lista")

    else:

        print("NO SE PUDO CONECTAR A LA FUENTE DE DATOS")
        print(gestor_fuentes.obtener_error())

else:

    print("NO HAY FUENTE DE DATOS CONFIGURADA")


print("PASO 2: intentando crear VentanaPrincipal")

try:

    ventana = VentanaPrincipal(
        gestor_fuentes,
        gestor_configuracion
    )

    print("PASO 3: VentanaPrincipal creada")

except Exception as error:

    print("ERROR AL CREAR VENTANAPRINCIPAL")
    print(type(error).__name__)
    print(str(error))

    import traceback
    traceback.print_exc()

    input("\nPresiona ENTER para cerrar...")
    sys.exit(1)


print("PASO 4: intentando mostrar ventana")

try:

    ventana.show()

    print("PASO 5: ventana mostrada")

except Exception as error:

    print("ERROR AL MOSTRAR LA VENTANA")
    print(type(error).__name__)
    print(str(error))

    import traceback
    traceback.print_exc()

    input("\nPresiona ENTER para cerrar...")
    sys.exit(1)


print("PASO 6: iniciando QApplication")

sys.exit(app.exec())