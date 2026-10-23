from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QSpinBox,
    QCheckBox,
    QGroupBox,
    QMessageBox,
    QTabWidget,
    QScrollArea
)

from PySide6.QtCore import Qt


class PaginaConfiguracion(QWidget):

    def __init__(
        self,
        gestor_fuentes=None,
        gestor_configuracion=None
    ):
        super().__init__()

        self.gestor_fuentes = gestor_fuentes
        self.gestor_configuracion = gestor_configuracion

        self.configuracion = (
            self.gestor_configuracion.cargar()
            if self.gestor_configuracion
            else {}
        )

        self.construir_interfaz()
        self.cargar_configuracion()

    # ==================================================
    # INTERFAZ PRINCIPAL
    # ==================================================

    def construir_interfaz(self):

        layout_principal = QVBoxLayout()

        layout_principal.setContentsMargins(
            30,
            25,
            30,
            30
        )

        layout_principal.setSpacing(15)

        self.setLayout(layout_principal)

        # ----------------------------------------------
        # TITULO
        # ----------------------------------------------

        titulo = QLabel(
            "Configuración"
        )

        titulo.setObjectName(
            "titulo_pagina"
        )

        descripcion = QLabel(
            "Configure los parámetros generales y "
            "las fuentes de información del sistema."
        )

        descripcion.setObjectName(
            "descripcion_pagina"
        )

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(descripcion)

        # ----------------------------------------------
        # PESTAÑAS
        # ----------------------------------------------

        self.pestanas = QTabWidget()

        self.pestanas.addTab(
            self.crear_pagina_organizacion(),
            "Organización"
        )

        self.pestanas.addTab(
            self.crear_pagina_fuente_datos(),
            "Fuente de datos"
        )

        self.pestanas.addTab(
            self.crear_pagina_importacion(),
            "Importación"
        )

        self.pestanas.addTab(
            self.crear_pagina_asistencia(),
            "Asistencia"
        )

        self.pestanas.addTab(
            self.crear_pagina_modulos(),
            "Módulos"
        )

        layout_principal.addWidget(
            self.pestanas
        )

        # ----------------------------------------------
        # BOTONES
        # ----------------------------------------------

        barra_botones = QHBoxLayout()

        barra_botones.addStretch()

        self.boton_guardar = QPushButton(
            "Guardar configuración"
        )

        self.boton_guardar.setMinimumHeight(40)

        self.boton_guardar.clicked.connect(
            self.guardar_configuracion
        )

        barra_botones.addWidget(
            self.boton_guardar
        )

        layout_principal.addLayout(
            barra_botones
        )

    # ==================================================
    # ORGANIZACIÓN
    # ==================================================

    def crear_pagina_organizacion(self):

        pagina = QWidget()

        layout = QVBoxLayout(
            pagina
        )

        layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        grupo = QGroupBox(
            "Información de la organización"
        )

        formulario = QFormLayout()

        self.organizacion_nombre = QLineEdit()

        self.organizacion_codigo = QLineEdit()

        self.organizacion_direccion = QLineEdit()

        self.organizacion_telefono = QLineEdit()

        formulario.addRow(
            "Nombre:",
            self.organizacion_nombre
        )

        formulario.addRow(
            "Código:",
            self.organizacion_codigo
        )

        formulario.addRow(
            "Dirección:",
            self.organizacion_direccion
        )

        formulario.addRow(
            "Teléfono:",
            self.organizacion_telefono
        )

        grupo.setLayout(
            formulario
        )

        layout.addWidget(
            grupo
        )

        layout.addStretch()

        return pagina

    # ==================================================
    # FUENTE DE DATOS
    # ==================================================

    def crear_pagina_fuente_datos(self):

        pagina = QWidget()

        layout = QVBoxLayout(
            pagina
        )

        layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        grupo = QGroupBox(
            "Fuente de datos"
        )

        formulario = QFormLayout()

        self.fuente_tipo = QComboBox()

        self.fuente_tipo.addItem(
            "MySQL",
            "mysql"
        )

        self.fuente_tipo.addItem(
            "Base de datos",
            "bd"
        )

        self.fuente_tipo.addItem(
            "Excel",
            "excel"
        )

        self.fuente_tipo.addItem(
            "CSV",
            "csv"
        )

        self.fuente_tipo.addItem(
            "API",
            "api"
        )

        self.fuente_tipo.currentIndexChanged.connect(
            self.actualizar_campos_fuente
        )

        self.bd_servidor = QLineEdit()

        self.bd_puerto = QSpinBox()

        self.bd_puerto.setRange(
            1,
            65535
        )

        self.bd_base = QLineEdit()

        self.bd_usuario = QLineEdit()

        self.bd_password = QLineEdit()

        self.bd_password.setEchoMode(
            QLineEdit.Password
        )

        formulario.addRow(
            "Tipo:",
            self.fuente_tipo
        )

        formulario.addRow(
            "Servidor:",
            self.bd_servidor
        )

        formulario.addRow(
            "Puerto:",
            self.bd_puerto
        )

        formulario.addRow(
            "Base de datos:",
            self.bd_base
        )

        formulario.addRow(
            "Usuario:",
            self.bd_usuario
        )

        formulario.addRow(
            "Contraseña:",
            self.bd_password
        )

        grupo.setLayout(
            formulario
        )

        layout.addWidget(
            grupo
        )

        # ----------------------------------------------
        # ESTADO
        # ----------------------------------------------

        self.estado_fuente = QLabel(
            "Sin comprobar"
        )

        layout.addWidget(
            self.estado_fuente
        )

        # ----------------------------------------------
        # BOTON PROBAR
        # ----------------------------------------------

        self.boton_probar = QPushButton(
            "Probar conexión"
        )

        self.boton_probar.setMinimumHeight(
            40
        )

        self.boton_probar.clicked.connect(
            self.probar_conexion
        )

        layout.addWidget(
            self.boton_probar
        )

        layout.addStretch()

        return pagina

    # ==================================================
    # IMPORTACION
    # ==================================================

    def crear_pagina_importacion(self):

        pagina = QWidget()

        layout = QVBoxLayout(
            pagina
        )

        layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        grupo = QGroupBox(
            "Configuración de importación"
        )

        formulario = QFormLayout()

        self.importacion_tipo = QComboBox()

        self.importacion_tipo.addItem(
            "Excel",
            "excel"
        )

        self.importacion_tipo.addItem(
            "CSV",
            "csv"
        )

        self.importacion_modo = QComboBox()

        self.importacion_modo.addItem(
            "Carpeta",
            "carpeta"
        )

        self.importacion_modo.addItem(
            "Archivo único",
            "archivo"
        )

        self.importacion_modo.addItem(
            "Múltiples archivos",
            "multiples"
        )

        formulario.addRow(
            "Tipo:",
            self.importacion_tipo
        )

        formulario.addRow(
            "Modo:",
            self.importacion_modo
        )

        grupo.setLayout(
            formulario
        )

        layout.addWidget(
            grupo
        )

        # ----------------------------------------------
        # EXTENSIONES
        # ----------------------------------------------

        grupo_extensiones = QGroupBox(
            "Extensiones permitidas"
        )

        layout_extensiones = QVBoxLayout()

        self.extension_xlsx = QCheckBox(
            ".xlsx"
        )

        self.extension_xls = QCheckBox(
            ".xls"
        )

        self.extension_csv = QCheckBox(
            ".csv"
        )

        layout_extensiones.addWidget(
            self.extension_xlsx
        )

        layout_extensiones.addWidget(
            self.extension_xls
        )

        layout_extensiones.addWidget(
            self.extension_csv
        )

        grupo_extensiones.setLayout(
            layout_extensiones
        )

        layout.addWidget(
            grupo_extensiones
        )

        layout.addStretch()

        return pagina

    # ==================================================
    # ASISTENCIA
    # ==================================================

    def crear_pagina_asistencia(self):

        pagina = QWidget()

        layout = QVBoxLayout(
            pagina
        )

        layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        # ----------------------------------------------
        # HORARIO
        # ----------------------------------------------

        grupo_horario = QGroupBox(
            "Horario laboral"
        )

        formulario_horario = QFormLayout()

        self.hora_entrada = QLineEdit()

        self.hora_entrada.setPlaceholderText(
            "HH:MM"
        )

        self.hora_salida = QLineEdit()

        self.hora_salida.setPlaceholderText(
            "HH:MM"
        )

        formulario_horario.addRow(
            "Hora de entrada:",
            self.hora_entrada
        )

        formulario_horario.addRow(
            "Hora de salida:",
            self.hora_salida
        )

        grupo_horario.setLayout(
            formulario_horario
        )

        layout.addWidget(
            grupo_horario
        )

        # ----------------------------------------------
        # TOLERANCIA
        # ----------------------------------------------

        grupo_tolerancia = QGroupBox(
            "Tolerancia"
        )

        formulario_tolerancia = QFormLayout()

        self.tolerancia_entrada = QSpinBox()

        self.tolerancia_entrada.setRange(
            0,
            180
        )

        self.tolerancia_entrada.setSuffix(
            " minutos"
        )

        formulario_tolerancia.addRow(
            "Tolerancia de entrada:",
            self.tolerancia_entrada
        )

        grupo_tolerancia.setLayout(
            formulario_tolerancia
        )

        layout.addWidget(
            grupo_tolerancia
        )

        # ----------------------------------------------
        # REGLAS
        # ----------------------------------------------

        grupo_reglas = QGroupBox(
            "Reglas de procesamiento"
        )

        layout_reglas = QVBoxLayout()

        self.regla_primera = QCheckBox(
            "La primera marcación corresponde a la entrada"
        )

        self.regla_ultima = QCheckBox(
            "La última marcación corresponde a la salida"
        )

        self.regla_generar_salida = QCheckBox(
            "Generar salida cuando exista una sola marcación"
        )

        layout_reglas.addWidget(
            self.regla_primera
        )

        layout_reglas.addWidget(
            self.regla_ultima
        )

        layout_reglas.addWidget(
            self.regla_generar_salida
        )

        grupo_reglas.setLayout(
            layout_reglas
        )

        layout.addWidget(
            grupo_reglas
        )

        layout.addStretch()

        return pagina

    # ==================================================
    # MODULOS
    # ==================================================

    def crear_pagina_modulos(self):

        pagina = QWidget()

        layout = QVBoxLayout(
            pagina
        )

        layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        grupo = QGroupBox(
            "Módulos disponibles"
        )

        layout_modulos = QVBoxLayout()

        self.modulo_permisos = QCheckBox(
            "Permisos"
        )

        self.modulo_remuneraciones = QCheckBox(
            "Remuneraciones"
        )

        layout_modulos.addWidget(
            self.modulo_permisos
        )

        layout_modulos.addWidget(
            self.modulo_remuneraciones
        )

        grupo.setLayout(
            layout_modulos
        )

        layout.addWidget(
            grupo
        )

        aviso = QLabel(
            "Las reglas institucionales de cada módulo "
            "se configurarán posteriormente. "
            "No están fijadas en el código."
        )

        aviso.setWordWrap(
            True
        )

        layout.addWidget(
            aviso
        )

        layout.addStretch()

        return pagina

    # ==================================================
    # CARGAR CONFIGURACION
    # ==================================================

    def cargar_configuracion(self):

        organizacion = self.configuracion.get(
            "organizacion",
            {}
        )

        self.organizacion_nombre.setText(
            organizacion.get(
                "nombre",
                ""
            )
        )

        self.organizacion_codigo.setText(
            organizacion.get(
                "codigo",
                ""
            )
        )

        self.organizacion_direccion.setText(
            organizacion.get(
                "direccion",
                ""
            )
        )

        self.organizacion_telefono.setText(
            organizacion.get(
                "telefono",
                ""
            )
        )

        # ----------------------------------------------
        # FUENTE DE DATOS
        # ----------------------------------------------

        fuente = self.configuracion.get(
            "fuente_datos",
            {}
        )

        tipo = fuente.get(
            "tipo",
            "mysql"
        )

        indice = self.fuente_tipo.findData(
            tipo
        )

        if indice >= 0:
            self.fuente_tipo.setCurrentIndex(
                indice
            )

        mysql = fuente.get(
            "mysql",
            {}
        )

        self.bd_servidor.setText(
            str(
                mysql.get(
                    "servidor",
                    ""
                )
            )
        )

        self.bd_puerto.setValue(
            int(
                mysql.get(
                    "puerto",
                    3306
                )
            )
        )

        self.bd_base.setText(
            str(
                mysql.get(
                    "base_datos",
                    ""
                )
            )
        )

        self.bd_usuario.setText(
            str(
                mysql.get(
                    "usuario",
                    ""
                )
            )
        )

        self.bd_password.setText(
            str(
                mysql.get(
                    "password",
                    ""
                )
            )
        )

        # ----------------------------------------------
        # IMPORTACION
        # ----------------------------------------------

        importacion = self.configuracion.get(
            "importacion",
            {}
        )

        tipo_importacion = importacion.get(
            "tipo",
            "excel"
        )

        indice = self.importacion_tipo.findData(
            tipo_importacion
        )

        if indice >= 0:
            self.importacion_tipo.setCurrentIndex(
                indice
            )

        modo = importacion.get(
            "modo",
            "carpeta"
        )

        indice = self.importacion_modo.findData(
            modo
        )

        if indice >= 0:
            self.importacion_modo.setCurrentIndex(
                indice
            )

        extensiones = importacion.get(
            "extensiones",
            []
        )

        self.extension_xlsx.setChecked(
            ".xlsx" in extensiones
        )

        self.extension_xls.setChecked(
            ".xls" in extensiones
        )

        self.extension_csv.setChecked(
            ".csv" in extensiones
        )

        # ----------------------------------------------
        # ASISTENCIA
        # ----------------------------------------------

        asistencia = self.configuracion.get(
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

        reglas = asistencia.get(
            "reglas",
            {}
        )

        self.hora_entrada.setText(
            horario.get(
                "hora_entrada",
                "08:00"
            )
        )

        self.hora_salida.setText(
            horario.get(
                "hora_salida",
                "17:00"
            )
        )

        self.tolerancia_entrada.setValue(
            int(
                tolerancia.get(
                    "minutos_entrada",
                    0
                )
            )
        )

        self.regla_primera.setChecked(
            reglas.get(
                "primera_marcacion_es_entrada",
                True
            )
        )

        self.regla_ultima.setChecked(
            reglas.get(
                "ultima_marcacion_es_salida",
                True
            )
        )

        self.regla_generar_salida.setChecked(
            reglas.get(
                "generar_salida_si_solo_hay_una_marcacion",
                False
            )
        )

        # ----------------------------------------------
        # MODULOS
        # ----------------------------------------------

        permisos = self.configuracion.get(
            "permisos",
            {}
        )

        remuneraciones = self.configuracion.get(
            "remuneraciones",
            {}
        )

        self.modulo_permisos.setChecked(
            permisos.get(
                "habilitado",
                True
            )
        )

        self.modulo_remuneraciones.setChecked(
            remuneraciones.get(
                "habilitado",
                True
            )
        )

    # ==================================================
    # CAMBIAR CAMPOS DE FUENTE
    # ==================================================

    def actualizar_campos_fuente(self):

        tipo = self.fuente_tipo.currentData()

        es_bd = tipo in (
            "mysql",
            "bd"
        )

        self.bd_servidor.setEnabled(
            es_bd
        )

        self.bd_puerto.setEnabled(
            es_bd
        )

        self.bd_base.setEnabled(
            es_bd
        )

        self.bd_usuario.setEnabled(
            es_bd
        )

        self.bd_password.setEnabled(
            es_bd
        )

        self.boton_probar.setEnabled(
            tipo == "mysql"
        )

        if not es_bd:

            self.estado_fuente.setText(
                "La configuración de esta fuente "
                "se implementará en la siguiente etapa."
            )

    # ==================================================
    # PROBAR CONEXION
    # ==================================================

    def probar_conexion(self):

        if not self.gestor_fuentes:

            QMessageBox.warning(
                self,
                "Fuente de datos",
                "No existe un gestor de fuentes."
            )

            return

        tipo = self.fuente_tipo.currentData()

        if tipo != "mysql":

            QMessageBox.information(
                self,
                "Fuente de datos",
                "La prueba de conexión está "
                "disponible actualmente para MySQL."
            )

            return

        try:

            self.gestor_fuentes.configurar_mysql(
                servidor=self.bd_servidor.text().strip(),
                puerto=self.bd_puerto.value(),
                base_datos=self.bd_base.text().strip(),
                usuario=self.bd_usuario.text().strip(),
                password=self.bd_password.text()
            )

            resultado = (
                self.gestor_fuentes.conectar()
            )

            if resultado:

                self.estado_fuente.setText(
                    "Conexión exitosa."
                )

                QMessageBox.information(
                    self,
                    "Conexión",
                    "La conexión con la fuente "
                    "de datos fue exitosa."
                )

            else:

                error = (
                    self.gestor_fuentes.obtener_error()
                    or "Error desconocido."
                )

                self.estado_fuente.setText(
                    "No se pudo establecer la conexión."
                )

                QMessageBox.critical(
                    self,
                    "Error de conexión",
                    f"No se pudo conectar:\n\n{error}"
                )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                f"Ocurrió un error:\n\n{error}"
            )

    # ==================================================
    # GUARDAR CONFIGURACION
    # ==================================================

    def guardar_configuracion(self):

        if not self.gestor_configuracion:

            QMessageBox.warning(
                self,
                "Configuración",
                "No existe un gestor de configuración."
            )

            return

        self.configuracion["organizacion"] = {
            "nombre": self.organizacion_nombre.text().strip(),
            "codigo": self.organizacion_codigo.text().strip(),
            "direccion": self.organizacion_direccion.text().strip(),
            "telefono": self.organizacion_telefono.text().strip()
        }

        # ----------------------------------------------
        # FUENTE DE DATOS
        # ----------------------------------------------

        tipo_fuente = (
            self.fuente_tipo.currentData()
        )

        self.configuracion["fuente_datos"] = {
            "tipo": tipo_fuente,
            "mysql": {
                "servidor": self.bd_servidor.text().strip(),
                "puerto": self.bd_puerto.value(),
                "base_datos": self.bd_base.text().strip(),
                "usuario": self.bd_usuario.text().strip(),
                "password": self.bd_password.text()
            }
        }

        # ----------------------------------------------
        # IMPORTACION
        # ----------------------------------------------

        extensiones = []

        if self.extension_xlsx.isChecked():
            extensiones.append(".xlsx")

        if self.extension_xls.isChecked():
            extensiones.append(".xls")

        if self.extension_csv.isChecked():
            extensiones.append(".csv")

        self.configuracion["importacion"] = {
            "tipo": self.importacion_tipo.currentData(),
            "modo": self.importacion_modo.currentData(),
            "extensiones": extensiones
        }

        # ----------------------------------------------
        # ASISTENCIA
        # ----------------------------------------------

        self.configuracion["asistencia"] = {
            "horario": {
                "hora_entrada": self.hora_entrada.text().strip(),
                "hora_salida": self.hora_salida.text().strip()
            },

            "tolerancia": {
                "minutos_entrada": (
                    self.tolerancia_entrada.value()
                )
            },

            "reglas": {
                "primera_marcacion_es_entrada": (
                    self.regla_primera.isChecked()
                ),

                "ultima_marcacion_es_salida": (
                    self.regla_ultima.isChecked()
                ),

                "generar_salida_si_solo_hay_una_marcacion": (
                    self.regla_generar_salida.isChecked()
                )
            }
        }

        # ----------------------------------------------
        # MODULOS
        # ----------------------------------------------

        self.configuracion["permisos"] = {
            "habilitado": (
                self.modulo_permisos.isChecked()
            )
        }

        self.configuracion["remuneraciones"] = {
            "habilitado": (
                self.modulo_remuneraciones.isChecked()
            )
        }

        # ----------------------------------------------
        # GUARDAR
        # ----------------------------------------------

        resultado = (
            self.gestor_configuracion.guardar(
                self.configuracion
            )
        )

        if resultado:

            QMessageBox.information(
                self,
                "Configuración",
                "La configuración fue guardada correctamente."
            )

        else:

            QMessageBox.critical(
                self,
                "Error",
                "No se pudo guardar la configuración."
            )