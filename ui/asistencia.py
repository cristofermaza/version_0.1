from datetime import date

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QComboBox,
    QSpinBox
)

from PySide6.QtCore import Qt

from asistencia.servicio_asistencia import ServicioAsistencia


class PaginaAsistencia(QWidget):

    def __init__(
        self,
        gestor_fuentes=None,
        gestor_configuracion=None
    ):
        super().__init__()

        self.gestor_fuentes = gestor_fuentes
        self.gestor_configuracion = gestor_configuracion

        self.datos_asistencia = []

        # --------------------------------------
        # SERVICIO DE ASISTENCIA
        # --------------------------------------

        configuracion = self.gestor_configuracion.cargar()

        self.servicio_asistencia = ServicioAsistencia(
            self.gestor_fuentes,
            configuracion
        )

        self.construir_interfaz()
        self.cargar_asistencia()

    # ==========================================
    # INTERFAZ
    # ==========================================

    def construir_interfaz(self):

        layout_principal = QVBoxLayout()

        layout_principal.setContentsMargins(
            30, 25, 30, 30
        )

        layout_principal.setSpacing(15)

        self.setLayout(layout_principal)

        # --------------------------------------
        # TÍTULO
        # --------------------------------------

        titulo = QLabel(
            "Gestión de Asistencia"
        )

        titulo.setObjectName(
            "titulo_pagina"
        )

        descripcion = QLabel(
            "Consulta y procesamiento de la "
            "asistencia diaria del personal."
        )

        descripcion.setObjectName(
            "descripcion_pagina"
        )

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(descripcion)

        # --------------------------------------
        # BARRA DE HERRAMIENTAS
        # --------------------------------------

        barra = QHBoxLayout()

        barra.setSpacing(10)

        # --------------------------------------
        # BUSCAR
        # --------------------------------------

        self.buscar = QLineEdit()

        self.buscar.setPlaceholderText(
            "Buscar por trabajador o ID..."
        )

        self.buscar.setMinimumHeight(40)

        self.buscar.textChanged.connect(
            self.filtrar_asistencia
        )

        barra.addWidget(self.buscar)

        # --------------------------------------
        # MES
        # --------------------------------------

        self.selector_mes = QComboBox()

        self.selector_mes.setMinimumHeight(40)

        meses = [
            ("Enero", 1),
            ("Febrero", 2),
            ("Marzo", 3),
            ("Abril", 4),
            ("Mayo", 5),
            ("Junio", 6),
            ("Julio", 7),
            ("Agosto", 8),
            ("Septiembre", 9),
            ("Octubre", 10),
            ("Noviembre", 11),
            ("Diciembre", 12)
        ]

        for nombre, numero in meses:

            self.selector_mes.addItem(
                nombre,
                numero
            )

        self.selector_mes.setCurrentIndex(8)

        self.selector_mes.currentIndexChanged.connect(
            self.cargar_asistencia
        )

        barra.addWidget(
            self.selector_mes
        )

        # --------------------------------------
        # AÑO
        # --------------------------------------

        self.selector_anio = QSpinBox()

        self.selector_anio.setMinimumHeight(40)

        self.selector_anio.setRange(
            2020,
            2100
        )

        self.selector_anio.setValue(
            2026
        )

        self.selector_anio.valueChanged.connect(
            self.cargar_asistencia
        )

        barra.addWidget(
            self.selector_anio
        )

        # --------------------------------------
        # PROCESAR
        # --------------------------------------

        boton_procesar = QPushButton(
            "Procesar asistencia"
        )

        boton_procesar.setMinimumHeight(40)

        boton_procesar.clicked.connect(
            self.procesar_asistencia
        )

        barra.addWidget(
            boton_procesar
        )

        # --------------------------------------
        # ACTUALIZAR
        # --------------------------------------

        boton_actualizar = QPushButton(
            "Actualizar"
        )

        boton_actualizar.setMinimumHeight(40)

        boton_actualizar.clicked.connect(
            self.cargar_asistencia
        )

        barra.addWidget(
            boton_actualizar
        )

        layout_principal.addLayout(
            barra
        )

        # --------------------------------------
        # ESTADO
        # --------------------------------------

        self.estado = QLabel(
            "Cargando..."
        )

        self.estado.setObjectName(
            "estado_asistencia"
        )

        layout_principal.addWidget(
            self.estado
        )

        # --------------------------------------
        # TABLA
        # --------------------------------------

        self.tabla = QTableWidget()

        self.tabla.setColumnCount(8)

        self.tabla.setHorizontalHeaderLabels([
            "Fecha",
            "ID Usuario",
            "Nombre",
            "Apellido",
            "Entrada",
            "Salida",
            "Estado",
            "Observaciones"
        ])

        self.tabla.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.tabla.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.tabla.setAlternatingRowColors(
            True
        )

        self.tabla.verticalHeader().setVisible(
            False
        )

        encabezado = (
            self.tabla.horizontalHeader()
        )

        encabezado.setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.tabla.setMinimumHeight(
            400
        )

        layout_principal.addWidget(
            self.tabla
        )

    # ==========================================
    # OBTENER PERIODO
    # ==========================================

    def obtener_periodo_seleccionado(self):

        mes = self.selector_mes.currentData()

        anio = self.selector_anio.value()

        fecha_inicio = date(
            anio,
            mes,
            1
        )

        if mes == 12:

            fecha_fin = date(
                anio + 1,
                1,
                1
            )

        else:

            fecha_fin = date(
                anio,
                mes + 1,
                1
            )

        return fecha_inicio, fecha_fin

    # ==========================================
    # CARGAR ASISTENCIA
    # ==========================================

    def cargar_asistencia(self):

        self.tabla.setRowCount(0)

        self.datos_asistencia = []

        if not self.gestor_fuentes:

            self.estado.setText(
                "Fuente de datos no disponible."
            )

            return

        if not self.gestor_fuentes.esta_disponible():

            self.estado.setText(
                "No hay conexión con la "
                "fuente de datos."
            )

            return

        try:

            self.estado.setText(
                "Consultando asistencia..."
            )

            fecha_inicio, fecha_fin = (
                self.obtener_periodo_seleccionado()
            )

            # ----------------------------------
            # NUEVO FLUJO DE EVALUACIÓN
            # ----------------------------------

            datos = (
                self.servicio_asistencia
                .obtener_evaluacion_periodo(
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin
                )
            )

            self.datos_asistencia = datos

            self.mostrar_datos(
                datos
            )

        except Exception as error:

            self.estado.setText(
                "Error al cargar la asistencia."
            )

            QMessageBox.critical(
                self,
                "Error",
                "No se pudo cargar la asistencia:\n\n"
                f"{error}"
            )

    # ==========================================
    # PROCESAR ASISTENCIA
    # ==========================================

    def procesar_asistencia(self):

        if not self.gestor_fuentes:

            QMessageBox.warning(
                self,
                "Fuente de datos",
                "No hay una fuente de datos configurada."
            )

            return

        if not self.gestor_fuentes.esta_disponible():

            QMessageBox.warning(
                self,
                "Conexión",
                "No existe una conexión disponible "
                "con la fuente de datos."
            )

            return

        if not self.gestor_configuracion:

            QMessageBox.warning(
                self,
                "Configuración",
                "No se encontró el gestor de configuración."
            )

            return

        # --------------------------------------
        # OBTENER PERIODO
        # --------------------------------------

        fecha_inicio, fecha_fin = (
            self.obtener_periodo_seleccionado()
        )

        mes = self.selector_mes.currentText()

        anio = self.selector_anio.value()

        # --------------------------------------
        # CONFIRMACIÓN
        # --------------------------------------

        respuesta = QMessageBox.question(
            self,
            "Procesar asistencia",
            "¿Desea procesar las marcaciones "
            "del periodo seleccionado?\n\n"
            f"Periodo: {mes} {anio}",
            QMessageBox.Yes |
            QMessageBox.No
        )

        if respuesta != QMessageBox.Yes:

            return

        # --------------------------------------
        # PROCESAMIENTO
        # --------------------------------------

        try:

            self.estado.setText(
                "Procesando asistencia..."
            )

            cantidad = (
                self.servicio_asistencia
                .procesar_asistencia(
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin
                )
            )

            # ----------------------------------
            # VOLVER A CONSULTAR
            # ----------------------------------

            self.cargar_asistencia()

            QMessageBox.information(
                self,
                "Proceso completado",
                "El procesamiento de asistencia "
                "finalizó correctamente.\n\n"
                f"Periodo: {mes} {anio}\n"
                f"Registros procesados: {cantidad}"
            )

        except Exception as error:

            self.estado.setText(
                "Error durante el procesamiento."
            )

            QMessageBox.critical(
                self,
                "Error",
                "No se pudo procesar la asistencia:\n\n"
                f"{error}"
            )

    # ==========================================
    # MOSTRAR DATOS
    # ==========================================

    def mostrar_datos(self, datos):

        self.tabla.setRowCount(0)

        for registro in datos:

            fila = self.tabla.rowCount()

            self.tabla.insertRow(
                fila
            )

            # ----------------------------------
            # FECHA
            # ----------------------------------

            fecha = registro.get(
                "fecha"
            )

            if fecha is not None:

                if hasattr(fecha, "strftime"):

                    texto_fecha = fecha.strftime(
                        "%d/%m/%Y"
                    )

                else:

                    texto_fecha = str(fecha)

            else:

                texto_fecha = ""

            # ----------------------------------
            # ENTRADA
            # ----------------------------------

            hora_entrada = registro.get(
                "hora_entrada"
            )

            if hora_entrada is not None:

                if hasattr(hora_entrada, "strftime"):

                    texto_entrada = (
                        hora_entrada.strftime("%H:%M")
                    )

                else:

                    texto_entrada = str(
                        hora_entrada
                    )

            else:

                texto_entrada = "-"

            # ----------------------------------
            # SALIDA
            # ----------------------------------

            hora_salida = registro.get(
                "hora_salida"
            )

            if hora_salida is not None:

                if hasattr(hora_salida, "strftime"):

                    texto_salida = (
                        hora_salida.strftime("%H:%M")
                    )

                else:

                    texto_salida = str(
                        hora_salida
                    )

            else:

                texto_salida = "-"

            valores = [
                texto_fecha,
                registro.get(
                    "id_usuario",
                    ""
                ),
                registro.get(
                    "nombre",
                    ""
                ),
                registro.get(
                    "apellido",
                    ""
                ),
                texto_entrada,
                texto_salida,
                registro.get(
                    "estado",
                    ""
                ),
                registro.get(
                    "observaciones",
                    ""
                )
            ]

            for columna, valor in enumerate(
                valores
            ):

                if valor is None:

                    texto = ""

                else:

                    texto = str(valor)

                item = QTableWidgetItem(
                    texto
                )

                if columna in (0, 1, 4, 5, 6):

                    item.setTextAlignment(
                        Qt.AlignCenter
                    )

                self.tabla.setItem(
                    fila,
                    columna,
                    item
                )

        self.estado.setText(
            f"Registros encontrados: {len(datos)}"
        )

    # ==========================================
    # BUSCAR
    # ==========================================

    def filtrar_asistencia(
        self,
        texto
    ):

        texto = (
            texto
            .strip()
            .lower()
        )

        if not texto:

            self.mostrar_datos(
                self.datos_asistencia
            )

            return

        resultados = []

        for registro in (
            self.datos_asistencia
        ):

            id_usuario = str(
                registro.get(
                    "id_usuario",
                    ""
                )
            ).lower()

            nombre = str(
                registro.get(
                    "nombre",
                    ""
                )
            ).lower()

            apellido = str(
                registro.get(
                    "apellido",
                    ""
                )
            ).lower()

            if (
                texto in id_usuario
                or texto in nombre
                or texto in apellido
            ):

                resultados.append(
                    registro
                )

        self.mostrar_datos(
            resultados
        )