from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame
)

from config.configuracion import CONFIGURACION


class PaginaInicio(QWidget):

    def __init__(
        self,
        cambiar_pagina=None
    ):

        super().__init__()

        self.cambiar_pagina = cambiar_pagina

        layout = QVBoxLayout()

        layout.setContentsMargins(
            30,
            25,
            30,
            25
        )

        layout.setSpacing(20)

        # ==========================================================
        # ENCABEZADO
        # ==========================================================

        titulo = QLabel(
            "Panel principal"
        )

        titulo.setObjectName(
            "tituloPagina"
        )

        subtitulo = QLabel(
            f"{CONFIGURACION['sistema']['descripcion']} - "
            f"{CONFIGURACION['empresa']['nombre']}"
        )

        subtitulo.setObjectName(
            "subtituloPagina"
        )

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)

        # ==========================================================
        # TARJETAS
        # ==========================================================

        tarjetas = QHBoxLayout()
        tarjetas.setSpacing(15)

        tarjetas.addWidget(
            self.crear_tarjeta(
                "Personal",
                "200",
                "Trabajadores registrados"
            )
        )

        tarjetas.addWidget(
            self.crear_tarjeta(
                "Asistencia",
                "185",
                "Registros procesados"
            )
        )

        tarjetas.addWidget(
            self.crear_tarjeta(
                "Permisos",
                "8",
                "Pendientes de revisión"
            )
        )

        tarjetas.addWidget(
            self.crear_tarjeta(
                "Remuneraciones",
                "Septiembre",
                "Periodo actual"
            )
        )

        layout.addLayout(tarjetas)

        # ==========================================================
        # ACTIVIDAD
        # ==========================================================

        titulo_actividad = QLabel(
            "Actividad reciente"
        )

        titulo_actividad.setObjectName(
            "tituloSeccion"
        )

        layout.addWidget(
            titulo_actividad
        )

        panel_actividad = QFrame()

        panel_actividad.setObjectName(
            "panel"
        )

        actividad = QVBoxLayout()

        actividad.setContentsMargins(
            20,
            15,
            20,
            15
        )

        actividad.setSpacing(12)

        actividad.addWidget(
            self.crear_actividad(
                "Importación de asistencia",
                "Se procesaron archivos de asistencia"
            )
        )

        actividad.addWidget(
            self.crear_actividad(
                "Procesamiento de asistencia",
                "Se generaron los registros diarios"
            )
        )

        actividad.addWidget(
            self.crear_actividad(
                "Permisos",
                "Solicitudes pendientes de revisión"
            )
        )

        panel_actividad.setLayout(
            actividad
        )

        layout.addWidget(
            panel_actividad
        )

        # ==========================================================
        # ACCIONES RÁPIDAS
        # ==========================================================

        titulo_acciones = QLabel(
            "Acciones rápidas"
        )

        titulo_acciones.setObjectName(
            "tituloSeccion"
        )

        layout.addWidget(
            titulo_acciones
        )

        acciones = QHBoxLayout()
        acciones.setSpacing(10)

        boton_importar = QPushButton(
            "Importar asistencia"
        )

        boton_personal = QPushButton(
            "Gestionar personal"
        )

        boton_reportes = QPushButton(
            "Generar reporte"
        )

        if self.cambiar_pagina:

            boton_importar.clicked.connect(
                lambda: self.cambiar_pagina(1)
            )

            boton_personal.clicked.connect(
                lambda: self.cambiar_pagina(2)
            )

            boton_reportes.clicked.connect(
                lambda: self.cambiar_pagina(6)
            )

        acciones.addWidget(
            boton_importar
        )

        acciones.addWidget(
            boton_personal
        )

        acciones.addWidget(
            boton_reportes
        )

        acciones.addStretch()

        layout.addLayout(
            acciones
        )

        layout.addStretch()

        # ==========================================================
        # PIE
        # ==========================================================

        informacion = QLabel(
            f"{CONFIGURACION['sistema']['nombre']} · "
            f"Versión {CONFIGURACION['sistema']['version']}"
        )

        informacion.setObjectName(
            "subtituloPagina"
        )

        layout.addWidget(
            informacion
        )

        self.setLayout(layout)

    # ==============================================================
    # CREAR TARJETA
    # ==============================================================

    def crear_tarjeta(
        self,
        titulo,
        valor,
        descripcion
    ):

        tarjeta = QFrame()

        tarjeta.setObjectName(
            "tarjeta"
        )

        layout = QVBoxLayout()

        layout.setContentsMargins(
            18,
            15,
            18,
            15
        )

        etiqueta_titulo = QLabel(
            titulo
        )

        etiqueta_titulo.setObjectName(
            "tarjetaTitulo"
        )

        etiqueta_valor = QLabel(
            valor
        )

        etiqueta_valor.setObjectName(
            "tarjetaValor"
        )

        etiqueta_descripcion = QLabel(
            descripcion
        )

        etiqueta_descripcion.setObjectName(
            "tarjetaDescripcion"
        )

        layout.addWidget(
            etiqueta_titulo
        )

        layout.addWidget(
            etiqueta_valor
        )

        layout.addWidget(
            etiqueta_descripcion
        )

        tarjeta.setLayout(
            layout
        )

        return tarjeta

    # ==============================================================
    # CREAR ACTIVIDAD
    # ==============================================================

    def crear_actividad(
        self,
        titulo,
        descripcion
    ):

        contenedor = QFrame()

        layout = QVBoxLayout()

        layout.setContentsMargins(
            5,
            3,
            5,
            3
        )

        titulo_label = QLabel(
            titulo
        )

        titulo_label.setObjectName(
            "tituloSeccion"
        )

        descripcion_label = QLabel(
            descripcion
        )

        descripcion_label.setObjectName(
            "subtituloPagina"
        )

        layout.addWidget(
            titulo_label
        )

        layout.addWidget(
            descripcion_label
        )

        contenedor.setLayout(
            layout
        )

        return contenedor