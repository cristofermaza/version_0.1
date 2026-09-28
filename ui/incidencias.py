from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QLineEdit,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QDialog,
    QFormLayout,
    QDateEdit,
    QTextEdit
)
from PySide6.QtCore import Qt, QDate


class FormularioIncidencia(QDialog):

    def __init__(self, parent=None, datos=None):
        super().__init__(parent)

        self.datos = None

        if datos:
            self.setWindowTitle("Editar incidencia")
        else:
            self.setWindowTitle("Nueva incidencia")

        self.setMinimumWidth(500)

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(18)

        titulo = QLabel(
            "Editar incidencia" if datos
            else "Registrar incidencia"
        )
        titulo.setObjectName("tituloPagina")

        subtitulo = QLabel(
            "Modifique los datos de la incidencia"
            if datos
            else "Ingrese los datos de la incidencia"
        )
        subtitulo.setObjectName("subtituloPagina")

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)

        formulario = QFormLayout()
        formulario.setSpacing(12)

        self.trabajador = QLineEdit()
        self.trabajador.setPlaceholderText(
            "Nombre del trabajador"
        )

        self.fecha = QDateEdit()
        self.fecha.setCalendarPopup(True)
        self.fecha.setDate(QDate.currentDate())
        self.fecha.setDisplayFormat("dd/MM/yyyy")

        self.tipo = QComboBox()
        self.tipo.addItems([
            "Falta",
            "Tardanza",
            "Salida anticipada",
            "Inasistencia justificada",
            "Inasistencia no justificada",
            "Otro"
        ])

        self.estado = QComboBox()
        self.estado.addItems([
            "Pendiente",
            "Justificada",
            "No justificada",
            "Observada"
        ])

        self.observacion = QTextEdit()
        self.observacion.setPlaceholderText(
            "Detalle u observación..."
        )
        self.observacion.setMaximumHeight(100)

        formulario.addRow(
            "Trabajador:",
            self.trabajador
        )

        formulario.addRow(
            "Fecha:",
            self.fecha
        )

        formulario.addRow(
            "Tipo:",
            self.tipo
        )

        formulario.addRow(
            "Estado:",
            self.estado
        )

        formulario.addRow(
            "Observación:",
            self.observacion
        )

        layout.addLayout(formulario)

        botones = QHBoxLayout()

        boton_cancelar = QPushButton("Cancelar")

        boton_guardar = QPushButton(
            "Guardar cambios"
            if datos
            else "Guardar"
        )

        boton_cancelar.setMinimumHeight(40)
        boton_guardar.setMinimumHeight(40)

        boton_cancelar.clicked.connect(
            self.reject
        )

        boton_guardar.clicked.connect(
            self.guardar
        )

        botones.addStretch()
        botones.addWidget(boton_cancelar)
        botones.addWidget(boton_guardar)

        layout.addLayout(botones)

        self.setLayout(layout)

        if datos:
            self.cargar_datos(datos)

    def cargar_datos(self, datos):

        self.trabajador.setText(datos[0])

        fecha = QDate.fromString(
            datos[1],
            "dd/MM/yyyy"
        )

        if fecha.isValid():
            self.fecha.setDate(fecha)

        indice = self.tipo.findText(
            datos[2]
        )

        if indice >= 0:
            self.tipo.setCurrentIndex(indice)

        indice = self.estado.findText(
            datos[3]
        )

        if indice >= 0:
            self.estado.setCurrentIndex(indice)

        self.observacion.setPlainText(
            datos[4]
        )

    def guardar(self):

        trabajador = self.trabajador.text().strip()

        if not trabajador:
            self.trabajador.setFocus()
            return

        fecha = self.fecha.date().toString(
            "dd/MM/yyyy"
        )

        tipo = self.tipo.currentText()
        estado = self.estado.currentText()

        observacion = (
            self.observacion
            .toPlainText()
            .strip()
        )

        self.datos = (
            trabajador,
            fecha,
            tipo,
            estado,
            observacion
        )

        self.accept()


class PaginaIncidencias(QWidget):

    def __init__(self):

        super().__init__()

        self.incidencias = [

            (
                "Juan Pérez",
                "23/09/2026",
                "Tardanza",
                "Pendiente",
                "Llegada después de la hora referencial"
            ),

            (
                "María García",
                "22/09/2026",
                "Inasistencia justificada",
                "Justificada",
                "Presentó documento médico"
            ),

            (
                "Carlos Ramos",
                "21/09/2026",
                "Salida anticipada",
                "Observada",
                "Pendiente de sustento"
            ),

            (
                "Ana Torres",
                "20/09/2026",
                "Falta",
                "No justificada",
                ""
            ),

            (
                "Luis Mendoza",
                "19/09/2026",
                "Tardanza",
                "Justificada",
                "Comisión autorizada"
            )
        ]

        self.construir_interfaz()
        self.actualizar_tabla()

    def construir_interfaz(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            30,
            25,
            30,
            25
        )

        layout.setSpacing(18)

        # =========================
        # ENCABEZADO
        # =========================

        titulo = QLabel(
            "Gestión de Incidencias"
        )

        titulo.setObjectName(
            "tituloPagina"
        )

        subtitulo = QLabel(
            "Registro y seguimiento de incidencias del personal"
        )

        subtitulo.setObjectName(
            "subtituloPagina"
        )

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)

        # =========================
        # TARJETAS
        # =========================

        tarjetas = QHBoxLayout()
        tarjetas.setSpacing(15)

        self.tarjeta_pendientes = (
            self.crear_tarjeta(
                "Pendientes",
                "0",
                "Por revisar"
            )
        )

        self.tarjeta_justificadas = (
            self.crear_tarjeta(
                "Justificadas",
                "0",
                "Incidencias justificadas"
            )
        )

        self.tarjeta_no_justificadas = (
            self.crear_tarjeta(
                "No justificadas",
                "0",
                "Requieren atención"
            )
        )

        self.tarjeta_observadas = (
            self.crear_tarjeta(
                "Observadas",
                "0",
                "Requieren sustento"
            )
        )

        tarjetas.addWidget(
            self.tarjeta_pendientes
        )

        tarjetas.addWidget(
            self.tarjeta_justificadas
        )

        tarjetas.addWidget(
            self.tarjeta_no_justificadas
        )

        tarjetas.addWidget(
            self.tarjeta_observadas
        )

        layout.addLayout(tarjetas)

        # =========================
        # FILTROS
        # =========================

        panel_filtros = QFrame()
        panel_filtros.setObjectName(
            "panel"
        )

        filtros = QHBoxLayout()

        filtros.setContentsMargins(
            15,
            15,
            15,
            15
        )

        self.buscar = QLineEdit()

        self.buscar.setPlaceholderText(
            "Buscar trabajador..."
        )

        self.combo_tipo = QComboBox()

        self.combo_tipo.addItems([
            "Todos",
            "Falta",
            "Tardanza",
            "Salida anticipada",
            "Inasistencia justificada",
            "Inasistencia no justificada",
            "Otro"
        ])

        self.combo_estado = QComboBox()

        self.combo_estado.addItems([
            "Todos",
            "Pendiente",
            "Justificada",
            "No justificada",
            "Observada"
        ])

        boton_nuevo = QPushButton(
            "+ Nueva incidencia"
        )

        self.buscar.textChanged.connect(
            self.actualizar_tabla
        )

        self.combo_tipo.currentTextChanged.connect(
            self.actualizar_tabla
        )

        self.combo_estado.currentTextChanged.connect(
            self.actualizar_tabla
        )

        boton_nuevo.clicked.connect(
            self.nueva_incidencia
        )

        filtros.addWidget(self.buscar)
        filtros.addWidget(self.combo_tipo)
        filtros.addWidget(self.combo_estado)

        filtros.addStretch()

        filtros.addWidget(boton_nuevo)

        panel_filtros.setLayout(
            filtros
        )

        layout.addWidget(
            panel_filtros
        )

        # =========================
        # TABLA
        # =========================

        self.tabla = QTableWidget()

        self.tabla.setColumnCount(7)

        self.tabla.setHorizontalHeaderLabels([
            "Trabajador",
            "Fecha",
            "Tipo",
            "Estado",
            "Observación",
            "Editar",
            "Eliminar"
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
            4,
            QHeaderView.Stretch
        )

        for columna in [1, 2, 3, 5, 6]:

            encabezado.setSectionResizeMode(
                columna,
                QHeaderView.ResizeToContents
            )

        layout.addWidget(
            self.tabla
        )

        self.setLayout(layout)

    # =========================
    # TARJETAS
    # =========================

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

    # =========================
    # TABLA
    # =========================

    def actualizar_tabla(self):

        texto = (
            self.buscar
            .text()
            .lower()
            .strip()
        )

        tipo_filtro = (
            self.combo_tipo
            .currentText()
        )

        estado_filtro = (
            self.combo_estado
            .currentText()
        )

        filtrados = []

        for incidencia in self.incidencias:

            trabajador = (
                incidencia[0]
                .lower()
            )

            tipo = incidencia[2]
            estado = incidencia[3]

            coincide_trabajador = (
                texto in trabajador
            )

            coincide_tipo = (
                tipo_filtro == "Todos"
                or tipo == tipo_filtro
            )

            coincide_estado = (
                estado_filtro == "Todos"
                or estado == estado_filtro
            )

            if (
                coincide_trabajador
                and coincide_tipo
                and coincide_estado
            ):
                filtrados.append(
                    incidencia
                )

        self.tabla.setRowCount(
            len(filtrados)
        )

        for fila, incidencia in enumerate(
            filtrados
        ):

            for columna in range(5):

                item = QTableWidgetItem(
                    str(incidencia[columna])
                )

                item.setTextAlignment(
                    Qt.AlignVCenter
                )

                self.tabla.setItem(
                    fila,
                    columna,
                    item
                )

            boton_editar = QPushButton(
                "Editar"
            )

            boton_eliminar = QPushButton(
                "Eliminar"
            )

            boton_editar.clicked.connect(
                lambda _, datos=incidencia:
                self.editar_incidencia(datos)
            )

            boton_eliminar.clicked.connect(
                lambda _, datos=incidencia:
                self.eliminar_incidencia(datos)
            )

            self.tabla.setCellWidget(
                fila,
                5,
                boton_editar
            )

            self.tabla.setCellWidget(
                fila,
                6,
                boton_eliminar
            )

        self.actualizar_resumen()

    # =========================
    # RESUMEN
    # =========================

    def actualizar_resumen(self):

        pendientes = 0
        justificadas = 0
        no_justificadas = 0
        observadas = 0

        for incidencia in self.incidencias:

            estado = incidencia[3]

            if estado == "Pendiente":
                pendientes += 1

            elif estado == "Justificada":
                justificadas += 1

            elif estado == "No justificada":
                no_justificadas += 1

            elif estado == "Observada":
                observadas += 1

        self.tarjeta_pendientes.findChild(
            QLabel,
            "tarjetaValor"
        ).setText(
            str(pendientes)
        )

        self.tarjeta_justificadas.findChild(
            QLabel,
            "tarjetaValor"
        ).setText(
            str(justificadas)
        )

        self.tarjeta_no_justificadas.findChild(
            QLabel,
            "tarjetaValor"
        ).setText(
            str(no_justificadas)
        )

        self.tarjeta_observadas.findChild(
            QLabel,
            "tarjetaValor"
        ).setText(
            str(observadas)
        )

    # =========================
    # NUEVA INCIDENCIA
    # =========================

    def nueva_incidencia(self):

        formulario = FormularioIncidencia(
            self
        )

        resultado = formulario.exec()

        if resultado and formulario.datos:

            self.incidencias.append(
                formulario.datos
            )

            self.actualizar_tabla()

    # =========================
    # EDITAR
    # =========================

    def editar_incidencia(
        self,
        incidencia
    ):

        formulario = FormularioIncidencia(
            self,
            incidencia
        )

        resultado = formulario.exec()

        if resultado and formulario.datos:

            indice = self.incidencias.index(
                incidencia
            )

            self.incidencias[indice] = (
                formulario.datos
            )

            self.actualizar_tabla()

    # =========================
    # ELIMINAR
    # =========================

    def eliminar_incidencia(
        self,
        incidencia
    ):

        respuesta = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Desea eliminar esta incidencia?",
            QMessageBox.Yes
            | QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:

            self.incidencias.remove(
                incidencia
            )

            self.actualizar_tabla()