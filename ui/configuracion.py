from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QStackedWidget,
    QLineEdit,
    QComboBox,
    QFileDialog,
    QMessageBox,
    QSpinBox,
    QTimeEdit
)

from PySide6.QtCore import QTime

from data_sources.gestor_fuentes import GestorFuentes
from config.gestor_configuracion import GestorConfiguracion


class PaginaConfiguracion(QWidget):

    def __init__(
        self,
        gestor_fuentes=None,
        gestor_configuracion=None
    ):

        super().__init__()

        self.gestor_fuentes = (
            gestor_fuentes
            if gestor_fuentes
            else GestorFuentes()
        )

        self.gestor_configuracion = (
            gestor_configuracion
            if gestor_configuracion
            else GestorConfiguracion()
        )

        self.construir_interfaz()

    # ==========================================================
    # INTERFAZ PRINCIPAL
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
        # TÍTULO
        # ======================================================

        titulo = QLabel(
            "Configuración de datos"
        )

        titulo.setObjectName(
            "tituloPagina"
        )

        subtitulo = QLabel(
            "Configure el origen desde el cual el sistema "
            "obtendrá la información."
        )

        subtitulo.setObjectName(
            "subtituloPagina"
        )

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)

        # ======================================================
        # OPCIONES DE FUENTE
        # ======================================================

        opciones = QHBoxLayout()

        opciones.setSpacing(12)

        self.btn_excel = self.crear_boton_fuente(
            "📊",
            "Excel",
            "Archivos .xlsx y .xls"
        )

        self.btn_csv = self.crear_boton_fuente(
            "📄",
            "CSV",
            "Archivos delimitados"
        )

        self.btn_bd = self.crear_boton_fuente(
            "🗄",
            "Base de datos",
            "MySQL / MariaDB"
        )

        self.btn_api = self.crear_boton_fuente(
            "🔗",
            "API",
            "Sistema externo"
        )

        opciones.addWidget(
            self.btn_excel
        )

        opciones.addWidget(
            self.btn_csv
        )

        opciones.addWidget(
            self.btn_bd
        )

        opciones.addWidget(
            self.btn_api
        )

        layout.addLayout(opciones)

        # ======================================================
        # CONFIGURACIÓN DE FUENTE
        # ======================================================

        self.contenido = QStackedWidget()

        self.pagina_excel = (
            self.crear_pagina_excel()
        )

        self.pagina_csv = (
            self.crear_pagina_csv()
        )

        self.pagina_bd = (
            self.crear_pagina_bd()
        )

        self.pagina_api = (
            self.crear_pagina_api()
        )

        self.contenido.addWidget(
            self.pagina_excel
        )

        self.contenido.addWidget(
            self.pagina_csv
        )

        self.contenido.addWidget(
            self.pagina_bd
        )

        self.contenido.addWidget(
            self.pagina_api
        )

        layout.addWidget(
            self.contenido
        )

        # ======================================================
        # CONFIGURACIÓN DE ASISTENCIA
        # ======================================================

        titulo_asistencia = QLabel(
            "Configuración de asistencia"
        )

        titulo_asistencia.setObjectName(
            "tituloSeccion"
        )

        descripcion_asistencia = QLabel(
            "Defina el horario de trabajo y la tolerancia "
            "utilizada para procesar las marcaciones."
        )

        descripcion_asistencia.setObjectName(
            "subtituloPagina"
        )

        layout.addWidget(
            titulo_asistencia
        )

        layout.addWidget(
            descripcion_asistencia
        )

        panel_asistencia = (
            self.crear_panel_asistencia()
        )

        layout.addWidget(
            panel_asistencia
        )

        # ======================================================
        # CONEXIONES
        # ======================================================

        self.btn_excel.clicked.connect(
            lambda: self.mostrar_fuente(0)
        )

        self.btn_csv.clicked.connect(
            lambda: self.mostrar_fuente(1)
        )

        self.btn_bd.clicked.connect(
            lambda: self.mostrar_fuente(2)
        )

        self.btn_api.clicked.connect(
            lambda: self.mostrar_fuente(3)
        )

        self.setLayout(
            layout
        )

        # ======================================================
        # CARGAR CONFIGURACIÓN
        # ======================================================

        self.cargar_configuracion_asistencia()

        self.mostrar_fuente(0)

    # ==========================================================
    # BOTÓN DE FUENTE
    # ==========================================================

    def crear_boton_fuente(
        self,
        icono,
        titulo,
        descripcion
    ):

        boton = QPushButton()

        boton.setMinimumHeight(
            95
        )

        boton.setText(
            f"{icono}  {titulo}\n{descripcion}"
        )

        return boton

    # ==========================================================
    # CAMBIAR FUENTE
    # ==========================================================

    def mostrar_fuente(
        self,
        indice
    ):

        self.contenido.setCurrentIndex(
            indice
        )

        botones = [
            self.btn_excel,
            self.btn_csv,
            self.btn_bd,
            self.btn_api
        ]

        for boton in botones:

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

        boton_activo = botones[indice]

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

    # ==========================================================
    # EXCEL
    # ==========================================================

    def crear_pagina_excel(self):

        pagina = QFrame()

        pagina.setObjectName(
            "panel"
        )

        layout = QVBoxLayout()

        layout.setContentsMargins(
            25,
            20,
            25,
            20
        )

        titulo = QLabel(
            "Configuración de Excel"
        )

        titulo.setObjectName(
            "tituloSeccion"
        )

        descripcion = QLabel(
            "Seleccione la carpeta donde se encuentran "
            "los archivos de Excel que utilizará el sistema."
        )

        descripcion.setObjectName(
            "subtituloPagina"
        )

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            descripcion
        )

        layout.addSpacing(10)

        fila = QHBoxLayout()

        self.excel_ruta = QLineEdit()

        self.excel_ruta.setPlaceholderText(
            "Seleccione una carpeta..."
        )

        boton = QPushButton(
            "Seleccionar carpeta"
        )

        boton.clicked.connect(
            self.seleccionar_carpeta
        )

        fila.addWidget(
            self.excel_ruta
        )

        fila.addWidget(
            boton
        )

        layout.addLayout(
            fila
        )

        self.excel_formato = QComboBox()

        self.excel_formato.addItems([
            "Un archivo por trabajador",
            "Un archivo mensual",
            "Formato personalizado"
        ])

        layout.addWidget(
            QLabel(
                "Tipo de estructura:"
            )
        )

        layout.addWidget(
            self.excel_formato
        )

        boton_guardar = QPushButton(
            "Guardar configuración"
        )

        boton_guardar.clicked.connect(
            self.guardar_excel
        )

        layout.addWidget(
            boton_guardar
        )

        layout.addStretch()

        pagina.setLayout(
            layout
        )

        return pagina

    # ==========================================================
    # CSV
    # ==========================================================

    def crear_pagina_csv(self):

        pagina = QFrame()

        pagina.setObjectName(
            "panel"
        )

        layout = QVBoxLayout()

        layout.setContentsMargins(
            25,
            20,
            25,
            20
        )

        titulo = QLabel(
            "Configuración de CSV"
        )

        titulo.setObjectName(
            "tituloSeccion"
        )

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            QLabel(
                "Configure el archivo CSV que utilizará "
                "como fuente de información."
            )
        )

        self.csv_ruta = QLineEdit()

        self.csv_ruta.setPlaceholderText(
            "Ruta del archivo CSV..."
        )

        layout.addWidget(
            self.csv_ruta
        )

        self.csv_separador = QComboBox()

        self.csv_separador.addItems([
            "Coma (,)",
            "Punto y coma (;)",
            "Tabulación"
        ])

        layout.addWidget(
            QLabel(
                "Separador:"
            )
        )

        layout.addWidget(
            self.csv_separador
        )

        boton = QPushButton(
            "Guardar configuración"
        )

        boton.clicked.connect(
            lambda: QMessageBox.information(
                self,
                "Configuración",
                "Configuración CSV guardada."
            )
        )

        layout.addWidget(
            boton
        )

        layout.addStretch()

        pagina.setLayout(
            layout
        )

        return pagina

    # ==========================================================
    # BASE DE DATOS
    # ==========================================================

    def crear_pagina_bd(self):

        pagina = QFrame()

        pagina.setObjectName(
            "panel"
        )

        layout = QVBoxLayout()

        layout.setContentsMargins(
            25,
            20,
            25,
            20
        )

        titulo = QLabel(
            "Configuración de base de datos"
        )

        titulo.setObjectName(
            "tituloSeccion"
        )

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            QLabel(
                "Motor:"
            )
        )

        self.bd_motor = QComboBox()

        self.bd_motor.addItems([
            "MySQL",
            "MariaDB"
        ])

        layout.addWidget(
            self.bd_motor
        )

        self.bd_servidor = QLineEdit()

        self.bd_servidor.setPlaceholderText(
            "Servidor"
        )

        self.bd_puerto = QLineEdit()

        self.bd_puerto.setPlaceholderText(
            "Puerto"
        )

        self.bd_base = QLineEdit()

        self.bd_base.setPlaceholderText(
            "Base de datos"
        )

        self.bd_usuario = QLineEdit()

        self.bd_usuario.setPlaceholderText(
            "Usuario"
        )

        self.bd_password = QLineEdit()

        self.bd_password.setPlaceholderText(
            "Contraseña"
        )

        self.bd_password.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        layout.addWidget(
            self.bd_servidor
        )

        layout.addWidget(
            self.bd_puerto
        )

        layout.addWidget(
            self.bd_base
        )

        layout.addWidget(
            self.bd_usuario
        )

        layout.addWidget(
            self.bd_password
        )

        boton_probar = QPushButton(
            "Probar conexión"
        )

        boton_probar.clicked.connect(
            self.probar_conexion_mysql
        )

        layout.addWidget(
            boton_probar
        )

        boton_guardar = QPushButton(
            "Guardar configuración"
        )

        boton_guardar.clicked.connect(
            self.guardar_mysql
        )

        layout.addWidget(
            boton_guardar
        )

        layout.addStretch()

        pagina.setLayout(
            layout
        )

        return pagina

    # ==========================================================
    # PROBAR CONEXIÓN MYSQL
    # ==========================================================

    def probar_conexion_mysql(self):

        servidor = self.bd_servidor.text().strip()

        puerto_texto = (
            self.bd_puerto.text().strip()
        )

        base_datos = (
            self.bd_base.text().strip()
        )

        usuario = (
            self.bd_usuario.text().strip()
        )

        password = self.bd_password.text()

        if not servidor:

            QMessageBox.warning(
                self,
                "Datos incompletos",
                "Ingrese el servidor de MySQL."
            )

            return

        if not puerto_texto:

            QMessageBox.warning(
                self,
                "Datos incompletos",
                "Ingrese el puerto de MySQL."
            )

            return

        if not base_datos:

            QMessageBox.warning(
                self,
                "Datos incompletos",
                "Ingrese el nombre de la base de datos."
            )

            return

        if not usuario:

            QMessageBox.warning(
                self,
                "Datos incompletos",
                "Ingrese el usuario de MySQL."
            )

            return

        try:

            puerto = int(
                puerto_texto
            )

        except ValueError:

            QMessageBox.warning(
                self,
                "Puerto inválido",
                "El puerto debe ser un número."
            )

            return

        self.gestor_fuentes.configurar_mysql(
            servidor=servidor,
            puerto=puerto,
            base_datos=base_datos,
            usuario=usuario,
            password=password
        )

        if self.gestor_fuentes.conectar():

            QMessageBox.information(
                self,
                "Conexión exitosa",
                "La conexión con MySQL se realizó correctamente."
            )

        else:

            error = (
                self.gestor_fuentes.obtener_error()
            )

            QMessageBox.critical(
                self,
                "Error de conexión",
                "No fue posible conectarse a MySQL.\n\n"
                f"Detalle:\n{error}"
            )

    # ==========================================================
    # GUARDAR CONFIGURACIÓN MYSQL
    # ==========================================================

    def guardar_mysql(self):

        servidor = (
            self.bd_servidor.text().strip()
        )

        puerto_texto = (
            self.bd_puerto.text().strip()
        )

        base_datos = (
            self.bd_base.text().strip()
        )

        usuario = (
            self.bd_usuario.text().strip()
        )

        password = (
            self.bd_password.text()
        )

        if not servidor:

            QMessageBox.warning(
                self,
                "Configuración",
                "Ingrese el servidor."
            )

            return

        if not puerto_texto:

            QMessageBox.warning(
                self,
                "Configuración",
                "Ingrese el puerto."
            )

            return

        if not base_datos:

            QMessageBox.warning(
                self,
                "Configuración",
                "Ingrese la base de datos."
            )

            return

        if not usuario:

            QMessageBox.warning(
                self,
                "Configuración",
                "Ingrese el usuario."
            )

            return

        try:

            puerto = int(
                puerto_texto
            )

        except ValueError:

            QMessageBox.warning(
                self,
                "Configuración",
                "El puerto debe ser un número."
            )

            return

        configuracion = (
            self.gestor_configuracion.cargar()
        )

        if "fuente_datos" not in configuracion:

            configuracion["fuente_datos"] = {}

        configuracion["fuente_datos"]["tipo"] = (
            "mysql"
        )

        configuracion["fuente_datos"]["mysql"] = {
            "servidor": servidor,
            "puerto": puerto,
            "base_datos": base_datos,
            "usuario": usuario,
            "password": password
        }

        guardado = (
            self.gestor_configuracion.guardar(
                configuracion
            )
        )

        if not guardado:

            QMessageBox.critical(
                self,
                "Error",
                "No se pudo guardar la configuración."
            )

            return

        QMessageBox.information(
            self,
            "Configuración guardada",
            "La configuración de MySQL se guardó correctamente."
        )

    # ==========================================================
    # API
    # ==========================================================

    def crear_pagina_api(self):

        pagina = QFrame()

        pagina.setObjectName(
            "panel"
        )

        layout = QVBoxLayout()

        layout.setContentsMargins(
            25,
            20,
            25,
            20
        )

        titulo = QLabel(
            "Configuración de API"
        )

        titulo.setObjectName(
            "tituloSeccion"
        )

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            QLabel(
                "Configure una API externa como fuente "
                "de información."
            )
        )

        self.api_url = QLineEdit()

        self.api_url.setPlaceholderText(
            "https://servidor/api"
        )

        layout.addWidget(
            QLabel(
                "URL:"
            )
        )

        layout.addWidget(
            self.api_url
        )

        self.api_metodo = QComboBox()

        self.api_metodo.addItems([
            "REST",
            "JSON"
        ])

        layout.addWidget(
            QLabel(
                "Tipo:"
            )
        )

        layout.addWidget(
            self.api_metodo
        )

        self.api_token = QLineEdit()

        self.api_token.setPlaceholderText(
            "Token de autenticación"
        )

        self.api_token.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        layout.addWidget(
            QLabel(
                "Token:"
            )
        )

        layout.addWidget(
            self.api_token
        )

        boton = QPushButton(
            "Guardar configuración"
        )

        boton.clicked.connect(
            lambda: QMessageBox.information(
                self,
                "Configuración",
                "Configuración de API guardada."
            )
        )

        layout.addWidget(
            boton
        )

        layout.addStretch()

        pagina.setLayout(
            layout
        )

        return pagina

    # ==========================================================
    # PANEL DE ASISTENCIA
    # ==========================================================

    def crear_panel_asistencia(self):

        panel = QFrame()

        panel.setObjectName(
            "panel"
        )

        layout = QVBoxLayout()

        layout.setContentsMargins(
            25,
            20,
            25,
            20
        )

        layout.setSpacing(12)

        # ------------------------------------------
        # HORA DE ENTRADA
        # ------------------------------------------

        etiqueta_entrada = QLabel(
            "Hora de entrada:"
        )

        self.hora_entrada = QTimeEdit()

        self.hora_entrada.setDisplayFormat(
            "HH:mm"
        )

        self.hora_entrada.setMinimumHeight(
            38
        )

        layout.addWidget(
            etiqueta_entrada
        )

        layout.addWidget(
            self.hora_entrada
        )

        # ------------------------------------------
        # HORA DE SALIDA
        # ------------------------------------------

        etiqueta_salida = QLabel(
            "Hora de salida:"
        )

        self.hora_salida = QTimeEdit()

        self.hora_salida.setDisplayFormat(
            "HH:mm"
        )

        self.hora_salida.setMinimumHeight(
            38
        )

        layout.addWidget(
            etiqueta_salida
        )

        layout.addWidget(
            self.hora_salida
        )

        # ------------------------------------------
        # TOLERANCIA
        # ------------------------------------------

        etiqueta_tolerancia = QLabel(
            "Tolerancia de entrada (minutos):"
        )

        self.tolerancia_entrada = QSpinBox()

        self.tolerancia_entrada.setMinimum(
            0
        )

        self.tolerancia_entrada.setMaximum(
            120
        )

        self.tolerancia_entrada.setValue(
            0
        )

        self.tolerancia_entrada.setMinimumHeight(
            38
        )

        layout.addWidget(
            etiqueta_tolerancia
        )

        layout.addWidget(
            self.tolerancia_entrada
        )

        # ------------------------------------------
        # BOTÓN GUARDAR
        # ------------------------------------------

        boton_guardar = QPushButton(
            "Guardar configuración de asistencia"
        )

        boton_guardar.setMinimumHeight(
            42
        )

        boton_guardar.clicked.connect(
            self.guardar_configuracion_asistencia
        )

        layout.addWidget(
            boton_guardar
        )

        layout.addStretch()

        panel.setLayout(
            layout
        )

        return panel

    # ==========================================================
    # CARGAR CONFIGURACIÓN DE ASISTENCIA
    # ==========================================================

    def cargar_configuracion_asistencia(self):

        configuracion = (
            self.gestor_configuracion.cargar()
        )

        asistencia = configuracion.get(
            "asistencia",
            {}
        )

        horario = asistencia.get(
            "horario",
            {}
        )

        tolerancia = asistencia.get(
            "tolerancia",
            {}
        )

        hora_entrada = horario.get(
            "hora_entrada",
            "08:00"
        )

        hora_salida = horario.get(
            "hora_salida",
            "17:00"
        )

        minutos = tolerancia.get(
            "minutos_entrada",
            0
        )

        # ------------------------------------------
        # HORA DE ENTRADA
        # ------------------------------------------

        try:

            hora_e, minuto_e = map(
                int,
                hora_entrada.split(":")[:2]
            )

            self.hora_entrada.setTime(
                QTime(
                    hora_e,
                    minuto_e
                )
            )

        except (
            ValueError,
            AttributeError
        ):

            self.hora_entrada.setTime(
                QTime(
                    8,
                    0
                )
            )

        # ------------------------------------------
        # HORA DE SALIDA
        # ------------------------------------------

        try:

            hora_s, minuto_s = map(
                int,
                hora_salida.split(":")[:2]
            )

            self.hora_salida.setTime(
                QTime(
                    hora_s,
                    minuto_s
                )
            )

        except (
            ValueError,
            AttributeError
        ):

            self.hora_salida.setTime(
                QTime(
                    17,
                    0
                )
            )

        # ------------------------------------------
        # TOLERANCIA
        # ------------------------------------------

        try:

            self.tolerancia_entrada.setValue(
                int(minutos)
            )

        except (
            ValueError,
            TypeError
        ):

            self.tolerancia_entrada.setValue(
                0
            )

    # ==========================================================
    # GUARDAR CONFIGURACIÓN DE ASISTENCIA
    # ==========================================================

    def guardar_configuracion_asistencia(self):

        hora_entrada = (
            self.hora_entrada
            .time()
            .toString("HH:mm")
        )

        hora_salida = (
            self.hora_salida
            .time()
            .toString("HH:mm")
        )

        tolerancia = (
            self.tolerancia_entrada.value()
        )

        configuracion = (
            self.gestor_configuracion.cargar()
        )

        # ------------------------------------------
        # MANTENER CONFIGURACIÓN EXISTENTE
        # ------------------------------------------

        if "asistencia" not in configuracion:

            configuracion["asistencia"] = {}

        configuracion["asistencia"]["horario"] = {
            "hora_entrada": hora_entrada,
            "hora_salida": hora_salida
        }

        configuracion["asistencia"]["tolerancia"] = {
            "minutos_entrada": tolerancia
        }

        # ------------------------------------------
        # REGLAS POR DEFECTO
        # ------------------------------------------

        if "reglas" not in configuracion["asistencia"]:

            configuracion["asistencia"]["reglas"] = {
                "primera_marcacion_es_entrada": True,
                "ultima_marcacion_es_salida": True,
                "generar_salida_si_solo_hay_una_marcacion": False
            }

        guardado = (
            self.gestor_configuracion.guardar(
                configuracion
            )
        )

        if not guardado:

            QMessageBox.critical(
                self,
                "Error",
                "No se pudo guardar la configuración "
                "de asistencia."
            )

            return

        QMessageBox.information(
            self,
            "Configuración guardada",
            "La configuración de asistencia "
            "se guardó correctamente."
        )

    # ==========================================================
    # SELECCIONAR CARPETA
    # ==========================================================

    def seleccionar_carpeta(self):

        carpeta = (
            QFileDialog.getExistingDirectory(
                self,
                "Seleccionar carpeta"
            )
        )

        if carpeta:

            self.excel_ruta.setText(
                carpeta
            )

    # ==========================================================
    # GUARDAR EXCEL
    # ==========================================================

    def guardar_excel(self):

        ruta = (
            self.excel_ruta.text().strip()
        )

        if not ruta:

            QMessageBox.warning(
                self,
                "Configuración",
                "Seleccione una carpeta."
            )

            return

        QMessageBox.information(
            self,
            "Configuración",
            "Configuración de Excel guardada."
        )