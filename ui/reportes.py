from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox
)
from PySide6.QtCore import Qt


class PaginaReportes(QWidget):

    def __init__(self):

        super().__init__()

        self.construir_interfaz()

        self.cargar_historial()

    # ==========================================================
    # INTERFAZ
    # ==========================================================

    def construir_interfaz(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            30,
            25,
            30,
            25
        )

        layout.setSpacing(18)

        # ======================================================
        # ENCABEZADO
        # ======================================================

        titulo = QLabel(
            "Reportes"
        )

        titulo.setObjectName(
            "tituloPagina"
        )

        subtitulo = QLabel(
            "Generación y consulta de reportes del sistema"
        )

        subtitulo.setObjectName(
            "subtituloPagina"
        )

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)

        # ======================================================
        # PANEL DE GENERACIÓN
        # ======================================================

        panel = QFrame()

        panel.setObjectName(
            "panel"
        )

        formulario = QVBoxLayout()

        formulario.setContentsMargins(
            20,
            20,
            20,
            20
        )

        formulario.setSpacing(15)

        titulo_panel = QLabel(
            "Generar reporte"
        )

        titulo_panel.setObjectName(
            "tituloSeccion"
        )

        formulario.addWidget(
            titulo_panel
        )

        # -------------------------
        # FILA 1
        # -------------------------

        fila1 = QHBoxLayout()

        etiqueta_tipo = QLabel(
            "Tipo de reporte:"
        )

        self.tipo_reporte = QComboBox()

        self.tipo_reporte.addItems([
            "Reporte de asistencia",
            "Reporte de incidencias",
            "Reporte de permisos",
            "Reporte de remuneraciones",
            "Reporte de personal",
            "Resumen mensual"
        ])

        etiqueta_periodo = QLabel(
            "Periodo:"
        )

        self.periodo = QComboBox()

        self.periodo.addItems([
            "Septiembre 2026",
            "Agosto 2026",
            "Julio 2026",
            "Junio 2026"
        ])

        fila1.addWidget(
            etiqueta_tipo
        )

        fila1.addWidget(
            self.tipo_reporte
        )

        fila1.addSpacing(15)

        fila1.addWidget(
            etiqueta_periodo
        )

        fila1.addWidget(
            self.periodo
        )

        fila1.addStretch()

        formulario.addLayout(
            fila1
        )

        # -------------------------
        # FILA 2
        # -------------------------

        fila2 = QHBoxLayout()

        etiqueta_formato = QLabel(
            "Formato:"
        )

        self.formato = QComboBox()

        self.formato.addItems([
            "PDF",
            "Excel"
        ])

        boton_previsualizar = QPushButton(
            "Previsualizar"
        )

        boton_generar = QPushButton(
            "Generar reporte"
        )

        boton_previsualizar.clicked.connect(
            self.previsualizar
        )

        boton_generar.clicked.connect(
            self.generar_reporte
        )

        fila2.addWidget(
            etiqueta_formato
        )

        fila2.addWidget(
            self.formato
        )

        fila2.addStretch()

        fila2.addWidget(
            boton_previsualizar
        )

        fila2.addWidget(
            boton_generar
        )

        formulario.addLayout(
            fila2
        )

        panel.setLayout(
            formulario
        )

        layout.addWidget(
            panel
        )

        # ======================================================
        # HISTORIAL
        # ======================================================

        titulo_historial = QLabel(
            "Historial de reportes"
        )

        titulo_historial.setObjectName(
            "tituloSeccion"
        )

        layout.addWidget(
            titulo_historial
        )

        # ======================================================
        # TABLA
        # ======================================================

        self.tabla = QTableWidget()

        self.tabla.setColumnCount(6)

        self.tabla.setHorizontalHeaderLabels([
            "Reporte",
            "Periodo",
            "Formato",
            "Fecha de generación",
            "Usuario",
            "Acción"
        ])

        self.tabla.setAlternatingRowColors(
            True
        )

        self.tabla.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.tabla.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        encabezado = (
            self.tabla.horizontalHeader()
        )

        encabezado.setSectionResizeMode(
            0,
            QHeaderView.Stretch
        )

        encabezado.setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents
        )

        encabezado.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )

        encabezado.setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents
        )

        encabezado.setSectionResizeMode(
            4,
            QHeaderView.ResizeToContents
        )

        encabezado.setSectionResizeMode(
            5,
            QHeaderView.ResizeToContents
        )

        layout.addWidget(
            self.tabla
        )

        self.setLayout(
            layout
        )

    # ==========================================================
    # HISTORIAL
    # ==========================================================

    def cargar_historial(self):

        historial = [

            (
                "Reporte de asistencia",
                "Septiembre 2026",
                "PDF",
                "23/09/2026 10:25",
                "Administrador"
            ),

            (
                "Reporte de remuneraciones",
                "Septiembre 2026",
                "Excel",
                "22/09/2026 16:40",
                "Administrador"
            ),

            (
                "Reporte de incidencias",
                "Septiembre 2026",
                "PDF",
                "20/09/2026 11:15",
                "Administrador"
            ),

            (
                "Reporte de personal",
                "Septiembre 2026",
                "Excel",
                "18/09/2026 09:30",
                "Administrador"
            )
        ]

        self.tabla.setRowCount(
            len(historial)
        )

        for fila, reporte in enumerate(
            historial
        ):

            for columna in range(5):

                item = QTableWidgetItem(
                    str(reporte[columna])
                )

                item.setTextAlignment(
                    Qt.AlignVCenter
                )

                self.tabla.setItem(
                    fila,
                    columna,
                    item
                )

            boton = QPushButton(
                "Abrir"
            )

            boton.clicked.connect(
                lambda _, datos=reporte:
                self.abrir_reporte(datos)
            )

            self.tabla.setCellWidget(
                fila,
                5,
                boton
            )

    # ==========================================================
    # PREVISUALIZAR
    # ==========================================================

    def previsualizar(self):

        tipo = self.tipo_reporte.currentText()
        periodo = self.periodo.currentText()

        QMessageBox.information(
            self,
            "Previsualización",
            f"Reporte:\n{tipo}\n\n"
            f"Periodo:\n{periodo}\n\n"
            "La previsualización será conectada "
            "al generador de reportes posteriormente."
        )

    # ==========================================================
    # GENERAR
    # ==========================================================

    def generar_reporte(self):

        tipo = self.tipo_reporte.currentText()
        periodo = self.periodo.currentText()
        formato = self.formato.currentText()

        QMessageBox.information(
            self,
            "Generar reporte",
            f"Reporte: {tipo}\n"
            f"Periodo: {periodo}\n"
            f"Formato: {formato}\n\n"
            "El generador de PDF/Excel "
            "se implementará posteriormente."
        )

    # ==========================================================
    # ABRIR
    # ==========================================================

    def abrir_reporte(self, reporte):

        QMessageBox.information(
            self,
            "Reporte",
            f"Reporte seleccionado:\n\n"
            f"{reporte[0]}\n"
            f"{reporte[1]}\n"
            f"Formato: {reporte[2]}"
        )