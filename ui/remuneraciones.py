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
    QDoubleSpinBox
)
from PySide6.QtCore import Qt


class FormularioRemuneracion(QDialog):

    def __init__(self, parent=None, datos=None):
        super().__init__(parent)

        self.datos = None

        if datos:
            self.setWindowTitle("Editar remuneración")
        else:
            self.setWindowTitle("Nueva remuneración")

        self.setMinimumWidth(500)

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(18)

        titulo = QLabel(
            "Editar remuneración"
            if datos
            else "Registrar remuneración"
        )

        titulo.setObjectName("tituloPagina")

        subtitulo = QLabel(
            "Modifique los datos de la remuneración"
            if datos
            else "Ingrese los datos de la remuneración"
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

        self.sueldo = self.crear_campo_dinero()
        self.bonificaciones = self.crear_campo_dinero()
        self.descuentos = self.crear_campo_dinero()

        formulario.addRow(
            "Trabajador:",
            self.trabajador
        )

        formulario.addRow(
            "Sueldo base:",
            self.sueldo
        )

        formulario.addRow(
            "Bonificaciones:",
            self.bonificaciones
        )

        formulario.addRow(
            "Descuentos:",
            self.descuentos
        )

        layout.addLayout(formulario)

        botones = QHBoxLayout()

        boton_cancelar = QPushButton(
            "Cancelar"
        )

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

    def crear_campo_dinero(self):

        campo = QDoubleSpinBox()

        campo.setRange(
            0,
            9999999.99
        )

        campo.setDecimals(2)
        campo.setSingleStep(50)

        campo.setPrefix("S/ ")

        return campo

    def cargar_datos(self, datos):

        self.trabajador.setText(
            datos[0]
        )

        self.sueldo.setValue(
            float(datos[2])
        )

        self.bonificaciones.setValue(
            float(datos[3])
        )

        self.descuentos.setValue(
            float(datos[4])
        )

    def guardar(self):

        trabajador = (
            self.trabajador
            .text()
            .strip()
        )

        if not trabajador:
            self.trabajador.setFocus()
            return

        sueldo = self.sueldo.value()
        bonificaciones = (
            self.bonificaciones.value()
        )
        descuentos = self.descuentos.value()

        bruto = (
            sueldo +
            bonificaciones
        )

        neto = (
            bruto -
            descuentos
        )

        self.datos = (
            trabajador,
            "Septiembre 2026",
            sueldo,
            bonificaciones,
            descuentos,
            bruto,
            neto
        )

        self.accept()


class PaginaRemuneraciones(QWidget):

    def __init__(self):

        super().__init__()

        self.remuneraciones = [

            (
                "Juan Pérez",
                "Septiembre 2026",
                2500.00,
                250.00,
                180.00,
                2750.00,
                2570.00
            ),

            (
                "María García",
                "Septiembre 2026",
                3200.00,
                300.00,
                250.00,
                3500.00,
                3250.00
            ),

            (
                "Carlos Ramos",
                "Septiembre 2026",
                2800.00,
                150.00,
                200.00,
                2950.00,
                2750.00
            ),

            (
                "Ana Torres",
                "Septiembre 2026",
                2100.00,
                100.00,
                120.00,
                2200.00,
                2080.00
            ),

            (
                "Luis Mendoza",
                "Septiembre 2026",
                3500.00,
                400.00,
                300.00,
                3900.00,
                3600.00
            )
        ]

        self.construir_interfaz()
        self.actualizar_tabla()

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

        titulo = QLabel(
            "Remuneraciones"
        )

        titulo.setObjectName(
            "tituloPagina"
        )

        subtitulo = QLabel(
            "Gestión y cálculo de remuneraciones del personal"
        )

        subtitulo.setObjectName(
            "subtituloPagina"
        )

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)

        # ======================================================
        # BARRA SUPERIOR
        # ======================================================

        barra = QHBoxLayout()

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

        boton_procesar = QPushButton(
            "Procesar remuneraciones"
        )

        boton_procesar.clicked.connect(
            self.procesar
        )

        boton_nuevo = QPushButton(
            "+ Nueva remuneración"
        )

        boton_nuevo.clicked.connect(
            self.nueva_remuneracion
        )

        barra.addWidget(
            etiqueta_periodo
        )

        barra.addWidget(
            self.periodo
        )

        barra.addStretch()

        barra.addWidget(
            boton_procesar
        )

        barra.addWidget(
            boton_nuevo
        )

        layout.addLayout(barra)

        # ======================================================
        # TARJETAS
        # ======================================================

        tarjetas = QHBoxLayout()

        tarjetas.setSpacing(15)

        self.tarjeta_personal = (
            self.crear_tarjeta(
                "Personal procesado",
                "0",
                "Trabajadores"
            )
        )

        self.tarjeta_bruto = (
            self.crear_tarjeta(
                "Total bruto",
                "S/ 0.00",
                "Antes de descuentos"
            )
        )

        self.tarjeta_descuentos = (
            self.crear_tarjeta(
                "Descuentos",
                "S/ 0.00",
                "Total descontado"
            )
        )

        self.tarjeta_neto = (
            self.crear_tarjeta(
                "Total neto",
                "S/ 0.00",
                "Total a pagar"
            )
        )

        tarjetas.addWidget(
            self.tarjeta_personal
        )

        tarjetas.addWidget(
            self.tarjeta_bruto
        )

        tarjetas.addWidget(
            self.tarjeta_descuentos
        )

        tarjetas.addWidget(
            self.tarjeta_neto
        )

        layout.addLayout(tarjetas)

        # ======================================================
        # BÚSQUEDA
        # ======================================================

        panel_busqueda = QFrame()

        panel_busqueda.setObjectName(
            "panel"
        )

        busqueda = QHBoxLayout()

        busqueda.setContentsMargins(
            15,
            15,
            15,
            15
        )

        self.buscar = QLineEdit()

        self.buscar.setPlaceholderText(
            "Buscar trabajador..."
        )

        self.buscar.textChanged.connect(
            self.actualizar_tabla
        )

        busqueda.addWidget(
            self.buscar
        )

        busqueda.addStretch()

        boton_exportar = QPushButton(
            "Exportar"
        )

        boton_exportar.clicked.connect(
            self.exportar
        )

        busqueda.addWidget(
            boton_exportar
        )

        panel_busqueda.setLayout(
            busqueda
        )

        layout.addWidget(
            panel_busqueda
        )

        # ======================================================
        # TABLA
        # ======================================================

        self.tabla = QTableWidget()

        self.tabla.setColumnCount(9)

        self.tabla.setHorizontalHeaderLabels([
            "Trabajador",
            "Periodo",
            "Sueldo base",
            "Bonificaciones",
            "Descuentos",
            "Bruto",
            "Neto",
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

        for columna in range(1, 9):

            encabezado.setSectionResizeMode(
                columna,
                QHeaderView.ResizeToContents
            )

        layout.addWidget(
            self.tabla
        )

        self.setLayout(layout)

    # ==========================================================
    # TARJETA
    # ==========================================================

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

    # ==========================================================
    # ACTUALIZAR TABLA
    # ==========================================================

    def actualizar_tabla(self):

        texto = (
            self.buscar
            .text()
            .lower()
            .strip()
        )

        filtrados = []

        for remuneracion in self.remuneraciones:

            trabajador = (
                remuneracion[0]
                .lower()
            )

            if texto in trabajador:

                filtrados.append(
                    remuneracion
                )

        self.tabla.setRowCount(
            len(filtrados)
        )

        for fila, datos in enumerate(
            filtrados
        ):

            # Trabajador
            self.tabla.setItem(
                fila,
                0,
                QTableWidgetItem(
                    datos[0]
                )
            )

            # Periodo
            self.tabla.setItem(
                fila,
                1,
                QTableWidgetItem(
                    datos[1]
                )
            )

            # Sueldo
            self.tabla.setItem(
                fila,
                2,
                self.crear_item_dinero(
                    datos[2]
                )
            )

            # Bonificaciones
            self.tabla.setItem(
                fila,
                3,
                self.crear_item_dinero(
                    datos[3]
                )
            )

            # Descuentos
            self.tabla.setItem(
                fila,
                4,
                self.crear_item_dinero(
                    datos[4]
                )
            )

            # Bruto
            self.tabla.setItem(
                fila,
                5,
                self.crear_item_dinero(
                    datos[5]
                )
            )

            # Neto
            self.tabla.setItem(
                fila,
                6,
                self.crear_item_dinero(
                    datos[6]
                )
            )

            boton_editar = QPushButton(
                "Editar"
            )

            boton_eliminar = QPushButton(
                "Eliminar"
            )

            boton_editar.clicked.connect(
                lambda _, datos=datos:
                self.editar_remuneracion(
                    datos
                )
            )

            boton_eliminar.clicked.connect(
                lambda _, datos=datos:
                self.eliminar_remuneracion(
                    datos
                )
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

    # ==========================================================
    # ITEM DINERO
    # ==========================================================

    def crear_item_dinero(
        self,
        valor
    ):

        item = QTableWidgetItem(
            f"S/ {valor:,.2f}"
        )

        item.setTextAlignment(
            Qt.AlignRight |
            Qt.AlignVCenter
        )

        return item

    # ==========================================================
    # RESUMEN
    # ==========================================================

    def actualizar_resumen(self):

        cantidad = len(
            self.remuneraciones
        )

        total_bruto = sum(
            datos[5]
            for datos in self.remuneraciones
        )

        total_descuentos = sum(
            datos[4]
            for datos in self.remuneraciones
        )

        total_neto = sum(
            datos[6]
            for datos in self.remuneraciones
        )

        self.tarjeta_personal.findChild(
            QLabel,
            "tarjetaValor"
        ).setText(
            str(cantidad)
        )

        self.tarjeta_bruto.findChild(
            QLabel,
            "tarjetaValor"
        ).setText(
            f"S/ {total_bruto:,.2f}"
        )

        self.tarjeta_descuentos.findChild(
            QLabel,
            "tarjetaValor"
        ).setText(
            f"S/ {total_descuentos:,.2f}"
        )

        self.tarjeta_neto.findChild(
            QLabel,
            "tarjetaValor"
        ).setText(
            f"S/ {total_neto:,.2f}"
        )

    # ==========================================================
    # NUEVA REMUNERACIÓN
    # ==========================================================

    def nueva_remuneracion(self):

        formulario = FormularioRemuneracion(
            self
        )

        resultado = formulario.exec()

        if resultado and formulario.datos:

            self.remuneraciones.append(
                formulario.datos
            )

            self.actualizar_tabla()

    # ==========================================================
    # EDITAR
    # ==========================================================

    def editar_remuneracion(
        self,
        remuneracion
    ):

        formulario = FormularioRemuneracion(
            self,
            remuneracion
        )

        resultado = formulario.exec()

        if resultado and formulario.datos:

            indice = (
                self.remuneraciones
                .index(remuneracion)
            )

            self.remuneraciones[indice] = (
                formulario.datos
            )

            self.actualizar_tabla()

    # ==========================================================
    # ELIMINAR
    # ==========================================================

    def eliminar_remuneracion(
        self,
        remuneracion
    ):

        respuesta = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Desea eliminar esta remuneración?",
            QMessageBox.Yes |
            QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:

            self.remuneraciones.remove(
                remuneracion
            )

            self.actualizar_tabla()

    # ==========================================================
    # PROCESAR
    # ==========================================================

    def procesar(self):

        QMessageBox.information(
            self,
            "Procesamiento",
            "El procesamiento automático de "
            "remuneraciones se conectará posteriormente "
            "con asistencia, incidencias y la base de datos."
        )

    # ==========================================================
    # EXPORTAR
    # ==========================================================

    def exportar(self):

        QMessageBox.information(
            self,
            "Exportar",
            "La exportación de remuneraciones "
            "se implementará posteriormente."
        )