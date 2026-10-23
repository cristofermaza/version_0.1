from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QFrame,
    QMessageBox,
    QHeaderView
)

from ui.formulario_personal import FormularioPersonal


class PaginaPersonal(QWidget):

    def __init__(self, gestor_fuentes=None):

        super().__init__()

        self.gestor_fuentes = gestor_fuentes

        self.construir_interfaz()
        self.cargar_trabajadores()

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

        layout.setSpacing(16)

        # ======================================================
        # ENCABEZADO
        # ======================================================

        titulo = QLabel(
            "Gestión de Personal"
        )

        titulo.setObjectName(
            "tituloPagina"
        )

        subtitulo = QLabel(
            "Administración de trabajadores registrados"
        )

        subtitulo.setObjectName(
            "subtituloPagina"
        )

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)

        # ======================================================
        # TARJETAS
        # ======================================================

        tarjetas = QHBoxLayout()

        tarjetas.setSpacing(12)

        self.tarjeta_total = self.crear_tarjeta(
            "Total de trabajadores",
            "0"
        )

        self.tarjeta_activos = self.crear_tarjeta(
            "Trabajadores activos",
            "0"
        )

        self.tarjeta_inactivos = self.crear_tarjeta(
            "Trabajadores inactivos",
            "0"
        )

        tarjetas.addWidget(
            self.tarjeta_total
        )

        tarjetas.addWidget(
            self.tarjeta_activos
        )

        tarjetas.addWidget(
            self.tarjeta_inactivos
        )

        tarjetas.addStretch()

        layout.addLayout(tarjetas)

        # ======================================================
        # BARRA DE HERRAMIENTAS
        # ======================================================

        barra = QHBoxLayout()

        self.buscar = QLineEdit()

        self.buscar.setPlaceholderText(
            "Buscar por ID, nombre o apellido..."
        )

        self.buscar.setMinimumHeight(
            40
        )

        self.btn_nuevo = QPushButton(
            "+ Nuevo trabajador"
        )

        self.btn_nuevo.setMinimumHeight(
            40
        )

        self.buscar.textChanged.connect(
            self.filtrar
        )

        self.btn_nuevo.clicked.connect(
            self.nuevo_trabajador
        )

        barra.addWidget(
            self.buscar
        )

        barra.addWidget(
            self.btn_nuevo
        )

        layout.addLayout(
            barra
        )

        # ======================================================
        # TABLA
        # ======================================================

        self.tabla = QTableWidget()

        self.tabla.setColumnCount(
            7
        )

        self.tabla.setHorizontalHeaderLabels([
            "ID Usuario",
            "Nombre",
            "Apellido",
            "N.º Tarjeta",
            "Estado",
            "Editar",
            "Eliminar"
        ])

        self.tabla.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.tabla.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.tabla.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.tabla.setAlternatingRowColors(
            True
        )

        header = self.tabla.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeMode.Stretch
        )

        layout.addWidget(
            self.tabla
        )

        # ======================================================
        # INFORMACIÓN
        # ======================================================

        self.lbl_info = QLabel(
            "Trabajadores registrados: 0"
        )

        self.lbl_info.setObjectName(
            "subtituloPagina"
        )

        layout.addWidget(
            self.lbl_info
        )

        self.setLayout(
            layout
        )

    # ==========================================================
    # TARJETA
    # ==========================================================

    def crear_tarjeta(
        self,
        titulo,
        valor
    ):

        tarjeta = QFrame()

        tarjeta.setObjectName(
            "tarjeta"
        )

        layout = QVBoxLayout()

        layout.setContentsMargins(
            15,
            12,
            15,
            12
        )

        lbl_titulo = QLabel(
            titulo
        )

        lbl_titulo.setObjectName(
            "tarjetaTitulo"
        )

        lbl_valor = QLabel(
            valor
        )

        lbl_valor.setObjectName(
            "tarjetaValor"
        )

        layout.addWidget(
            lbl_titulo
        )

        layout.addWidget(
            lbl_valor
        )

        tarjeta.setLayout(
            layout
        )

        return tarjeta

    # ==========================================================
    # CARGAR TRABAJADORES
    # ==========================================================

    def cargar_trabajadores(self):

        print("========================================")
        print("PERSONAL: iniciando carga de trabajadores")
        print("========================================")

        try:

            self.tabla.setRowCount(0)

            # ------------------------------------------
            # COMPROBAR GESTOR
            # ------------------------------------------

            if not self.gestor_fuentes:

                print(
                    "PERSONAL: gestor_fuentes = None"
                )

                self.lbl_info.setText(
                    "Fuente de datos no configurada."
                )

                self.actualizar_resumen()

                return

            print(
                "PERSONAL: gestor_fuentes recibido correctamente"
            )

            # ------------------------------------------
            # COMPROBAR CONEXIÓN
            # ------------------------------------------

            disponible = (
                self.gestor_fuentes.esta_disponible()
            )

            print(
                f"PERSONAL: fuente disponible = {disponible}"
            )

            if not disponible:

                print(
                    "PERSONAL: NO existe conexión con la fuente"
                )

                self.lbl_info.setText(
                    "Fuente de datos no disponible."
                )

                self.actualizar_resumen()

                return

            # ------------------------------------------
            # OBTENER TRABAJADORES
            # ------------------------------------------

            print(
                "PERSONAL: consultando empleados..."
            )

            trabajadores = (
                self.gestor_fuentes
                .obtener_empleados()
            )

            print(
                "PERSONAL: trabajadores encontrados = "
                f"{len(trabajadores)}"
            )

            # ------------------------------------------
            # MOSTRAR TRABAJADORES
            # ------------------------------------------

            for trabajador in trabajadores:

                print(
                    "PERSONAL: cargando trabajador:",
                    trabajador
                )

                id_usuario = str(
                    trabajador.get(
                        "id_usuario",
                        ""
                    )
                )

                nombre = str(
                    trabajador.get(
                        "nombre",
                        ""
                    )
                )

                apellido = str(
                    trabajador.get(
                        "apellido",
                        ""
                    )
                )

                tarjeta = (
                    ""
                    if trabajador.get(
                        "numero_tarjeta"
                    ) is None
                    else str(
                        trabajador.get(
                            "numero_tarjeta"
                        )
                    )
                )

                estado = (
                    "Activo"
                    if trabajador.get(
                        "estado"
                    )
                    else "Inactivo"
                )

                datos = (
                    id_usuario,
                    nombre,
                    apellido,
                    tarjeta,
                    estado
                )

                self.agregar_fila(
                    datos
                )

            # ------------------------------------------
            # ACTUALIZAR RESUMEN
            # ------------------------------------------

            self.actualizar_resumen()

            cantidad = (
                self.tabla.rowCount()
            )

            self.lbl_info.setText(
                f"Trabajadores registrados: {cantidad}"
            )

            print(
                f"PERSONAL: tabla cargada con {cantidad} registros"
            )

            print(
                "========================================"
            )

        except Exception as error:

            print(
                "PERSONAL: ERROR AL CARGAR TRABAJADORES"
            )

            print(
                type(error).__name__
            )

            print(
                str(error)
            )

            import traceback

            traceback.print_exc()

            QMessageBox.critical(
                self,
                "Error de base de datos",
                "No se pudieron cargar los trabajadores.\n\n"
                f"{error}"
            )

    # ==========================================================
    # AGREGAR FILA
    # ==========================================================

    def agregar_fila(
        self,
        datos
    ):

        fila = self.tabla.rowCount()

        self.tabla.insertRow(
            fila
        )

        for columna, valor in enumerate(
            datos
        ):

            item = QTableWidgetItem(
                str(valor)
            )

            self.tabla.setItem(
                fila,
                columna,
                item
            )

        # ------------------------------------------------------
        # EDITAR
        # ------------------------------------------------------

        boton_editar = QPushButton(
            "Editar"
        )

        boton_editar.clicked.connect(
            lambda _, f=fila:
            self.editar_trabajador(f)
        )

        self.tabla.setCellWidget(
            fila,
            5,
            boton_editar
        )

        # ------------------------------------------------------
        # DAR DE BAJA
        # ------------------------------------------------------

        boton_eliminar = QPushButton(
            "Dar de baja"
        )

        boton_eliminar.clicked.connect(
            lambda _, f=fila:
            self.eliminar_trabajador(f)
        )

        self.tabla.setCellWidget(
            fila,
            6,
            boton_eliminar
        )

    # ==========================================================
    # NUEVO TRABAJADOR
    # ==========================================================

    def nuevo_trabajador(self):

        formulario = FormularioPersonal(
            self
        )

        resultado = formulario.exec()

        if not resultado:
            return

        if not formulario.datos:
            return

        datos = formulario.datos

        id_usuario = datos[0]
        nombre = datos[1]
        apellido = datos[2]
        tarjeta = datos[3]
        estado = datos[4]

        estado_bd = (
            True
            if estado == "Activo"
            else False
        )

        try:

            if not self.gestor_fuentes:

                raise RuntimeError(
                    "No hay una fuente de datos configurada."
                )

            if not self.gestor_fuentes.esta_disponible():

                raise RuntimeError(
                    "La fuente de datos no está disponible."
                )

            self.gestor_fuentes.crear_empleado(
                id_usuario,
                nombre,
                apellido,
                tarjeta,
                estado_bd
            )

            self.cargar_trabajadores()

            self.lbl_info.setText(
                "Trabajador registrado correctamente."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                "No se pudo registrar el trabajador.\n\n"
                f"{e}"
            )

    # ==========================================================
    # EDITAR
    # ==========================================================

    def editar_trabajador(
        self,
        fila
    ):

        datos_actuales = []

        for columna in range(5):

            item = self.tabla.item(
                fila,
                columna
            )

            if item:

                datos_actuales.append(
                    item.text()
                )

            else:

                datos_actuales.append(
                    ""
                )

        id_usuario_original = datos_actuales[0]

        formulario = FormularioPersonal(
            self,
            datos_actuales
        )

        resultado = formulario.exec()

        if not resultado:
            return

        if not formulario.datos:
            return

        nuevos_datos = formulario.datos

        id_usuario = nuevos_datos[0]
        nombre = nuevos_datos[1]
        apellido = nuevos_datos[2]
        tarjeta = nuevos_datos[3]
        estado = nuevos_datos[4]

        estado_bd = (
            True
            if estado == "Activo"
            else False
        )

        try:

            if not self.gestor_fuentes:

                raise RuntimeError(
                    "No hay una fuente de datos configurada."
                )

            if not self.gestor_fuentes.esta_disponible():

                raise RuntimeError(
                    "La fuente de datos no está disponible."
                )

            self.gestor_fuentes.actualizar_empleado(
                id_usuario_original,
                id_usuario,
                nombre,
                apellido,
                tarjeta,
                estado_bd
            )

            self.cargar_trabajadores()

            self.lbl_info.setText(
                "Trabajador actualizado correctamente."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                "No se pudo actualizar el trabajador.\n\n"
                f"{e}"
            )

    # ==========================================================
    # DAR DE BAJA
    # ==========================================================

    def eliminar_trabajador(
        self,
        fila
    ):

        id_usuario = self.tabla.item(
            fila,
            0
        ).text()

        nombre = (
            self.tabla.item(
                fila,
                1
            ).text()
            + " "
            + self.tabla.item(
                fila,
                2
            ).text()
        )

        respuesta = QMessageBox.question(
            self,
            "Confirmar baja",
            f"¿Desea dar de baja al trabajador "
            f"{nombre}?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No
        )

        if respuesta != QMessageBox.StandardButton.Yes:
            return

        try:

            if not self.gestor_fuentes:

                raise RuntimeError(
                    "No hay una fuente de datos configurada."
                )

            if not self.gestor_fuentes.esta_disponible():

                raise RuntimeError(
                    "La fuente de datos no está disponible."
                )

            self.gestor_fuentes.desactivar_empleado(
                id_usuario
            )

            self.cargar_trabajadores()

            self.lbl_info.setText(
                "Trabajador dado de baja correctamente."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                "No se pudo dar de baja al trabajador.\n\n"
                f"{e}"
            )

    # ==========================================================
    # BUSCAR
    # ==========================================================

    def filtrar(self):

        texto = (
            self.buscar.text()
            .lower()
            .strip()
        )

        visibles = 0

        for fila in range(
            self.tabla.rowCount()
        ):

            id_usuario = self.tabla.item(
                fila,
                0
            ).text().lower()

            nombre = self.tabla.item(
                fila,
                1
            ).text().lower()

            apellido = self.tabla.item(
                fila,
                2
            ).text().lower()

            coincide = (
                texto in id_usuario
                or texto in nombre
                or texto in apellido
            )

            self.tabla.setRowHidden(
                fila,
                not coincide
            )

            if coincide:
                visibles += 1

        self.lbl_info.setText(
            f"Trabajadores mostrados: {visibles}"
        )

    # ==========================================================
    # RESUMEN
    # ==========================================================

    def actualizar_resumen(self):

        total = self.tabla.rowCount()

        activos = 0
        inactivos = 0

        for fila in range(total):

            item_estado = self.tabla.item(
                fila,
                4
            )

            if not item_estado:
                continue

            estado = item_estado.text()

            if estado == "Activo":
                activos += 1
            else:
                inactivos += 1

        self.tarjeta_total.findChild(
            QLabel,
            "tarjetaValor"
        ).setText(
            str(total)
        )

        self.tarjeta_activos.findChild(
            QLabel,
            "tarjetaValor"
        ).setText(
            str(activos)
        )

        self.tarjeta_inactivos.findChild(
            QLabel,
            "tarjetaValor"
        ).setText(
            str(inactivos)
        )

        self.lbl_info.setText(
            f"Trabajadores registrados: {total}"
        )