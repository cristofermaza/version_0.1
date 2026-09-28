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


class FormularioPermiso(QDialog):

    def __init__(self, parent=None, datos=None):
        super().__init__(parent)

        self.datos = None

        if datos:
            self.setWindowTitle("Editar permiso")
        else:
            self.setWindowTitle("Nuevo permiso")

        self.setMinimumWidth(500)

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(18)

        titulo = QLabel(
            "Editar permiso" if datos else "Registrar permiso"
        )
        titulo.setObjectName("tituloPagina")

        subtitulo = QLabel(
            "Modifique los datos del permiso"
            if datos
            else "Ingrese los datos del permiso"
        )
        subtitulo.setObjectName("subtituloPagina")

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)

        formulario = QFormLayout()
        formulario.setSpacing(12)

        self.trabajador = QLineEdit()
        self.trabajador.setPlaceholderText("Nombre del trabajador")

        self.fecha = QDateEdit()
        self.fecha.setCalendarPopup(True)
        self.fecha.setDate(QDate.currentDate())
        self.fecha.setDisplayFormat("dd/MM/yyyy")

        self.tipo = QComboBox()
        self.tipo.addItems([
            "Personal",
            "Salud",
            "Comisión de servicio",
            "Capacitación",
            "Otro"
        ])

        self.desde = QDateEdit()
        self.desde.setCalendarPopup(True)
        self.desde.setDate(QDate.currentDate())
        self.desde.setDisplayFormat("dd/MM/yyyy")

        self.hasta = QDateEdit()
        self.hasta.setCalendarPopup(True)
        self.hasta.setDate(QDate.currentDate())
        self.hasta.setDisplayFormat("dd/MM/yyyy")

        self.estado = QComboBox()
        self.estado.addItems([
            "Pendiente",
            "Aprobado",
            "Observado"
        ])

        self.observacion = QTextEdit()
        self.observacion.setPlaceholderText(
            "Ingrese una observación..."
        )
        self.observacion.setMaximumHeight(100)

        formulario.addRow("Trabajador:", self.trabajador)
        formulario.addRow("Fecha solicitud:", self.fecha)
        formulario.addRow("Tipo:", self.tipo)
        formulario.addRow("Desde:", self.desde)
        formulario.addRow("Hasta:", self.hasta)
        formulario.addRow("Estado:", self.estado)
        formulario.addRow("Observación:", self.observacion)

        layout.addLayout(formulario)

        botones = QHBoxLayout()

        boton_cancelar = QPushButton("Cancelar")
        boton_guardar = QPushButton(
            "Guardar cambios" if datos else "Guardar"
        )

        boton_cancelar.setMinimumHeight(40)
        boton_guardar.setMinimumHeight(40)

        boton_cancelar.clicked.connect(self.reject)
        boton_guardar.clicked.connect(self.guardar)

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

        indice = self.tipo.findText(datos[2])

        if indice >= 0:
            self.tipo.setCurrentIndex(indice)

        desde = QDate.fromString(
            datos[3],
            "dd/MM/yyyy"
        )

        hasta = QDate.fromString(
            datos[4],
            "dd/MM/yyyy"
        )

        if desde.isValid():
            self.desde.setDate(desde)

        if hasta.isValid():
            self.hasta.setDate(hasta)

        indice = self.estado.findText(datos[5])

        if indice >= 0:
            self.estado.setCurrentIndex(indice)

        self.observacion.setPlainText(datos[6])

    def guardar(self):

        trabajador = self.trabajador.text().strip()

        if not trabajador:
            self.trabajador.setFocus()
            return

        fecha = self.fecha.date().toString("dd/MM/yyyy")
        tipo = self.tipo.currentText()
        desde = self.desde.date().toString("dd/MM/yyyy")
        hasta = self.hasta.date().toString("dd/MM/yyyy")
        estado = self.estado.currentText()
        observacion = self.observacion.toPlainText().strip()

        self.datos = (
            trabajador,
            fecha,
            tipo,
            desde,
            hasta,
            estado,
            observacion
        )

        self.accept()


class PaginaPermisos(QWidget):

    def __init__(self):

        super().__init__()

        self.permisos = [
            (
                "Juan Pérez",
                "23/09/2026",
                "Personal",
                "24/09/2026",
                "24/09/2026",
                "Pendiente",
                ""
            ),
            (
                "María García",
                "22/09/2026",
                "Salud",
                "23/09/2026",
                "23/09/2026",
                "Pendiente",
                "Cita médica"
            ),
            (
                "Carlos Ramos",
                "20/09/2026",
                "Capacitación",
                "21/09/2026",
                "22/09/2026",
                "Aprobado",
                ""
            ),
            (
                "Ana Torres",
                "19/09/2026",
                "Personal",
                "20/09/2026",
                "20/09/2026",
                "Observado",
                "Falta documento"
            ),
            (
                "Luis Mendoza",
                "18/09/2026",
                "Comisión de servicio",
                "19/09/2026",
                "19/09/2026",
                "Aprobado",
                ""
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

        titulo = QLabel("Gestión de Permisos")
        titulo.setObjectName("tituloPagina")

        subtitulo = QLabel(
            "Registro y seguimiento de permisos del personal"
        )
        subtitulo.setObjectName("subtituloPagina")

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)

        # =========================
        # TARJETAS
        # =========================

        tarjetas = QHBoxLayout()
        tarjetas.setSpacing(15)

        self.tarjeta_pendientes = self.crear_tarjeta(
            "Pendientes",
            "0",
            "Por revisar"
        )

        self.tarjeta_aprobados = self.crear_tarjeta(
            "Aprobados",
            "0",
            "Permisos aprobados"
        )

        self.tarjeta_observados = self.crear_tarjeta(
            "Observados",
            "0",
            "Requieren corrección"
        )

        tarjetas.addWidget(self.tarjeta_pendientes)
        tarjetas.addWidget(self.tarjeta_aprobados)
        tarjetas.addWidget(self.tarjeta_observados)

        layout.addLayout(tarjetas)

        # =========================
        # FILTROS
        # =========================

        panel_filtros = QFrame()
        panel_filtros.setObjectName("panel")

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

        self.combo_estado = QComboBox()

        self.combo_estado.addItems([
            "Todos",
            "Pendiente",
            "Aprobado",
            "Observado"
        ])

        boton_nuevo = QPushButton(
            "+ Nuevo permiso"
        )

        boton_nuevo.clicked.connect(
            self.nuevo_permiso
        )

        self.buscar.textChanged.connect(
            self.actualizar_tabla
        )

        self.combo_estado.currentTextChanged.connect(
            self.actualizar_tabla
        )

        filtros.addWidget(self.buscar)
        filtros.addWidget(self.combo_estado)
        filtros.addStretch()
        filtros.addWidget(boton_nuevo)

        panel_filtros.setLayout(filtros)

        layout.addWidget(panel_filtros)

        # =========================
        # TABLA
        # =========================

        self.tabla = QTableWidget()

        self.tabla.setColumnCount(9)

        self.tabla.setHorizontalHeaderLabels([
            "Trabajador",
            "Fecha",
            "Tipo",
            "Desde",
            "Hasta",
            "Estado",
            "Observación",
            "Editar",
            "Eliminar"
        ])

        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.tabla.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        encabezado = self.tabla.horizontalHeader()

        encabezado.setSectionResizeMode(
            0,
            QHeaderView.Stretch
        )

        for columna in range(1, 9):
            encabezado.setSectionResizeMode(
                columna,
                QHeaderView.ResizeToContents
            )

        layout.addWidget(self.tabla)

        self.setLayout(layout)

    # =========================
    # TARJETA
    # =========================

    def crear_tarjeta(
        self,
        titulo,
        valor,
        descripcion
    ):

        tarjeta = QFrame()
        tarjeta.setObjectName("tarjeta")

        layout = QVBoxLayout()

        layout.setContentsMargins(
            18,
            15,
            18,
            15
        )

        etiqueta_titulo = QLabel(titulo)
        etiqueta_titulo.setObjectName(
            "tarjetaTitulo"
        )

        etiqueta_valor = QLabel(valor)
        etiqueta_valor.setObjectName(
            "tarjetaValor"
        )

        etiqueta_descripcion = QLabel(
            descripcion
        )

        etiqueta_descripcion.setObjectName(
            "tarjetaDescripcion"
        )

        layout.addWidget(etiqueta_titulo)
        layout.addWidget(etiqueta_valor)
        layout.addWidget(
            etiqueta_descripcion
        )

        tarjeta.setLayout(layout)

        return tarjeta

    # =========================
    # ACTUALIZAR TABLA
    # =========================

    def actualizar_tabla(self):

        texto = self.buscar.text().lower().strip()

        estado_filtro = (
            self.combo_estado.currentText()
        )

        filtrados = []

        for permiso in self.permisos:

            trabajador = permiso[0].lower()
            estado = permiso[5]

            coincide_trabajador = (
                texto in trabajador
            )

            coincide_estado = (
                estado_filtro == "Todos"
                or estado == estado_filtro
            )

            if (
                coincide_trabajador
                and coincide_estado
            ):
                filtrados.append(permiso)

        self.tabla.setRowCount(
            len(filtrados)
        )

        for fila, permiso in enumerate(
            filtrados
        ):

            for columna in range(7):

                item = QTableWidgetItem(
                    str(permiso[columna])
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
                lambda _, datos=permiso:
                self.editar_permiso(datos)
            )

            boton_eliminar.clicked.connect(
                lambda _, datos=permiso:
                self.eliminar_permiso(datos)
            )

            self.tabla.setCellWidget(
                fila,
                7,
                boton_editar
            )

            self.tabla.setCellWidget(
                fila,
                8,
                boton_eliminar
            )

        self.actualizar_resumen()

    # =========================
    # RESUMEN
    # =========================

    def actualizar_resumen(self):

        pendientes = 0
        aprobados = 0
        observados = 0

        for permiso in self.permisos:

            if permiso[5] == "Pendiente":
                pendientes += 1

            elif permiso[5] == "Aprobado":
                aprobados += 1

            elif permiso[5] == "Observado":
                observados += 1

        self.tarjeta_pendientes.findChild(
            QLabel,
            "tarjetaValor"
        ).setText(str(pendientes))

        self.tarjeta_aprobados.findChild(
            QLabel,
            "tarjetaValor"
        ).setText(str(aprobados))

        self.tarjeta_observados.findChild(
            QLabel,
            "tarjetaValor"
        ).setText(str(observados))

    # =========================
    # NUEVO
    # =========================

    def nuevo_permiso(self):

        formulario = FormularioPermiso(
            self
        )

        resultado = formulario.exec()

        if resultado and formulario.datos:

            self.permisos.append(
                formulario.datos
            )

            self.actualizar_tabla()

    # =========================
    # EDITAR
    # =========================

    def editar_permiso(self, permiso):

        formulario = FormularioPermiso(
            self,
            permiso
        )

        resultado = formulario.exec()

        if resultado and formulario.datos:

            indice = self.permisos.index(
                permiso
            )

            self.permisos[indice] = (
                formulario.datos
            )

            self.actualizar_tabla()

    # =========================
    # ELIMINAR
    # =========================

    def eliminar_permiso(self, permiso):

        respuesta = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Desea eliminar este permiso?",
            QMessageBox.Yes
            | QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:

            self.permisos.remove(
                permiso
            )

            self.actualizar_tabla()