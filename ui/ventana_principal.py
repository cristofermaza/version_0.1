from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget
)

from config.configuracion import CONFIGURACION

from ui.inicio import PaginaInicio
from ui.importacion import PaginaImportacion
from ui.personal import PaginaPersonal
from ui.asistencia import PaginaAsistencia
from ui.incidencias import PaginaIncidencias
from ui.permisos import PaginaPermisos
from ui.remuneraciones import PaginaRemuneraciones
from ui.reportes import PaginaReportes
from ui.configuracion import PaginaConfiguracion


class VentanaPrincipal(QMainWindow):

    def __init__(self, gestor_fuentes, gestor_configuracion):

        print("VP 1: entrando a VentanaPrincipal")

        super().__init__()

        print("VP 2: super() terminado")

        self.gestor_fuentes = gestor_fuentes
        self.gestor_configuracion = gestor_configuracion

        print("VP 3: gestores asignados")

        self.construir_interfaz()

        print("VP 4: interfaz construida")

    # ==========================================================
    # CONSTRUIR INTERFAZ
    # ==========================================================

    def construir_interfaz(self):

        # ==========================================================
        # CONFIGURACIÓN DE LA VENTANA
        # ==========================================================

        self.setWindowTitle(
            f"{CONFIGURACION['sistema']['nombre']} - "
            f"{CONFIGURACION['empresa']['nombre']}"
        )

        self.resize(1200, 750)
        self.setMinimumSize(1000, 650)

        # ==========================================================
        # CONTENEDOR PRINCIPAL
        # ==========================================================

        contenedor = QWidget()

        self.setCentralWidget(
            contenedor
        )

        layout_principal = QHBoxLayout()

        layout_principal.setContentsMargins(
            0,
            0,
            0,
            0
        )

        contenedor.setLayout(
            layout_principal
        )

        # ==========================================================
        # MENÚ LATERAL
        # ==========================================================

        menu = QWidget()

        menu.setObjectName(
            "menu"
        )

        menu.setFixedWidth(
            230
        )

        layout_menu = QVBoxLayout()

        layout_menu.setContentsMargins(
            15,
            20,
            15,
            15
        )

        menu.setLayout(
            layout_menu
        )

        # ==========================================================
        # TÍTULO DEL MENÚ
        # ==========================================================

        titulo = QLabel(
            CONFIGURACION["empresa"]["nombre_corto"]
        )

        titulo.setObjectName(
            "titulo"
        )

        subtitulo = QLabel(
            CONFIGURACION["sistema"]["descripcion"]
        )

        subtitulo.setObjectName(
            "subtitulo"
        )

        layout_menu.addWidget(
            titulo
        )

        layout_menu.addWidget(
            subtitulo
        )

        layout_menu.addSpacing(
            30
        )

        # ==========================================================
        # BOTONES DEL MENÚ
        # ==========================================================

        self.btn_inicio = QPushButton(
            "Inicio"
        )

        self.btn_importar = QPushButton(
            "Importar asistencia"
        )

        self.btn_personal = QPushButton(
            "Personal"
        )

        self.btn_asistencia = QPushButton(
            "Asistencia"
        )

        self.btn_incidencias = QPushButton(
            "Incidencias"
        )

        self.btn_permisos = QPushButton(
            "Permisos"
        )

        self.btn_remuneraciones = QPushButton(
            "Remuneraciones"
        )

        self.btn_reportes = QPushButton(
            "Reportes"
        )

        self.btn_configuracion = QPushButton(
            "Configuración"
        )

        self.botones_menu = [
            self.btn_inicio,
            self.btn_importar,
            self.btn_personal,
            self.btn_asistencia,
            self.btn_incidencias,
            self.btn_permisos,
            self.btn_remuneraciones,
            self.btn_reportes,
            self.btn_configuracion
        ]

        for boton in self.botones_menu:

            boton.setMinimumHeight(
                45
            )

            layout_menu.addWidget(
                boton
            )

        layout_menu.addStretch()

        # ==========================================================
        # VERSIÓN
        # ==========================================================

        version = QLabel(
            f"{CONFIGURACION['sistema']['nombre']}\n"
            f"Versión {CONFIGURACION['sistema']['version']}"
        )

        version.setObjectName(
            "version"
        )

        layout_menu.addWidget(
            version
        )

        # ==========================================================
        # CONTENIDO
        # ==========================================================

        self.contenido = QStackedWidget()

        # ==========================================================
        # PÁGINAS
        # ==========================================================

        # ----------------------------------------------------------
        # INICIO
        # ----------------------------------------------------------

        self.pagina_inicio = PaginaInicio(
            self.ir_a_pagina
        )

        # ----------------------------------------------------------
        # IMPORTACIÓN
        # ----------------------------------------------------------

        self.pagina_importar = PaginaImportacion()

        # ----------------------------------------------------------
        # PERSONAL
        # ----------------------------------------------------------

        self.pagina_personal = PaginaPersonal(
            self.gestor_fuentes
        )

        # ----------------------------------------------------------
        # ASISTENCIA
        # ----------------------------------------------------------

        self.pagina_asistencia = PaginaAsistencia(
            self.gestor_fuentes,
            self.gestor_configuracion
        )

        # ----------------------------------------------------------
        # INCIDENCIAS
        # ----------------------------------------------------------

        self.pagina_incidencias = PaginaIncidencias()

        # ----------------------------------------------------------
        # PERMISOS
        # ----------------------------------------------------------

        self.pagina_permisos = PaginaPermisos()

        # ----------------------------------------------------------
        # REMUNERACIONES
        # ----------------------------------------------------------

        self.pagina_remuneraciones = (
            PaginaRemuneraciones()
        )

        # ----------------------------------------------------------
        # REPORTES
        # ----------------------------------------------------------

        self.pagina_reportes = (
            PaginaReportes()
        )

        # ----------------------------------------------------------
        # CONFIGURACIÓN
        # ----------------------------------------------------------

        self.pagina_configuracion = PaginaConfiguracion(
            self.gestor_fuentes,
            self.gestor_configuracion
        )

        # ==========================================================
        # TODAS LAS PÁGINAS
        # ==========================================================

        paginas = [
            self.pagina_inicio,
            self.pagina_importar,
            self.pagina_personal,
            self.pagina_asistencia,
            self.pagina_incidencias,
            self.pagina_permisos,
            self.pagina_remuneraciones,
            self.pagina_reportes,
            self.pagina_configuracion
        ]

        for pagina in paginas:

            self.contenido.addWidget(
                pagina
            )

        # ==========================================================
        # CONEXIONES DEL MENÚ
        # ==========================================================

        self.btn_inicio.clicked.connect(
            lambda: self.cambiar_pagina(
                0,
                self.btn_inicio
            )
        )

        self.btn_importar.clicked.connect(
            lambda: self.cambiar_pagina(
                1,
                self.btn_importar
            )
        )

        self.btn_personal.clicked.connect(
            lambda: self.cambiar_pagina(
                2,
                self.btn_personal
            )
        )

        self.btn_asistencia.clicked.connect(
            lambda: self.cambiar_pagina(
                3,
                self.btn_asistencia
            )
        )

        self.btn_incidencias.clicked.connect(
            lambda: self.cambiar_pagina(
                4,
                self.btn_incidencias
            )
        )

        self.btn_permisos.clicked.connect(
            lambda: self.cambiar_pagina(
                5,
                self.btn_permisos
            )
        )

        self.btn_remuneraciones.clicked.connect(
            lambda: self.cambiar_pagina(
                6,
                self.btn_remuneraciones
            )
        )

        self.btn_reportes.clicked.connect(
            lambda: self.cambiar_pagina(
                7,
                self.btn_reportes
            )
        )

        self.btn_configuracion.clicked.connect(
            lambda: self.cambiar_pagina(
                8,
                self.btn_configuracion
            )
        )

        # ==========================================================
        # AGREGAR AL LAYOUT PRINCIPAL
        # ==========================================================

        layout_principal.addWidget(
            menu
        )

        layout_principal.addWidget(
            self.contenido
        )

        # ==========================================================
        # PÁGINA INICIAL
        # ==========================================================

        self.cambiar_pagina(
            0,
            self.btn_inicio
        )

    # ==============================================================
    # CAMBIAR DE PÁGINA
    # ==============================================================

    def cambiar_pagina(
        self,
        indice,
        boton_activo
    ):

        self.contenido.setCurrentIndex(
            indice
        )

        for boton in self.botones_menu:

            boton.setProperty(
                "activo",
                False
            )

            boton.style().unpolish(
                boton
            )

            boton.style().polish(
                boton
            )

        boton_activo.setProperty(
            "activo",
            True
        )

        boton_activo.style().unpolish(
            boton_activo
        )

        boton_activo.style().polish(
            boton_activo
        )

    # ==============================================================
    # NAVEGACIÓN DESDE INICIO
    # ==============================================================

    def ir_a_pagina(
        self,
        indice
    ):

        if 0 <= indice < len(
            self.botones_menu
        ):

            self.cambiar_pagina(
                indice,
                self.botones_menu[indice]
            )