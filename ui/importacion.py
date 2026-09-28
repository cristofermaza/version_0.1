import os

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QListWidget,
    QFileDialog,
    QProgressBar
)

from importacion.excel_reader import (
    leer_excel,
    validar_columnas
)

from importacion.database_importer import (
    importar_dataframe
)


class PaginaImportacion(QWidget):

    def __init__(self):
        super().__init__()

        self.carpeta_seleccionada = ""

        # ==========================================
        # LAYOUT PRINCIPAL
        # ==========================================

        layout = QVBoxLayout()
        self.setLayout(layout)

        # ==========================================
        # TÍTULO
        # ==========================================

        titulo = QLabel("Importación de asistencia")

        titulo.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            padding: 10px;
        """)

        layout.addWidget(titulo)

        descripcion = QLabel(
            "Seleccione la carpeta que contiene los archivos "
            "Excel exportados por el sistema biométrico."
        )

        descripcion.setStyleSheet("""
            color: #555555;
            padding: 5px 10px;
        """)

        layout.addWidget(descripcion)

        # ==========================================
        # BOTÓN SELECCIONAR CARPETA
        # ==========================================

        fila_boton = QHBoxLayout()

        self.btn_carpeta = QPushButton(
            "Seleccionar carpeta"
        )

        self.btn_carpeta.setMinimumHeight(40)

        self.btn_carpeta.clicked.connect(
            self.seleccionar_carpeta
        )

        self.lbl_carpeta = QLabel(
            "Ninguna carpeta seleccionada"
        )

        fila_boton.addWidget(self.btn_carpeta)
        fila_boton.addWidget(self.lbl_carpeta)

        layout.addLayout(fila_boton)

        # ==========================================
        # INFORMACIÓN
        # ==========================================

        self.lbl_total = QLabel(
            "Archivos encontrados: 0"
        )

        self.lbl_total.setStyleSheet("""
            font-weight: bold;
            padding: 10px;
        """)

        layout.addWidget(self.lbl_total)

        self.lbl_procesados = QLabel(
            "Procesados correctamente: 0"
        )

        self.lbl_errores = QLabel(
            "Con errores: 0"
        )

        layout.addWidget(self.lbl_procesados)
        layout.addWidget(self.lbl_errores)

        # ==========================================
        # LISTA DE ARCHIVOS
        # ==========================================

        self.lista_archivos = QListWidget()

        layout.addWidget(self.lista_archivos)

        # ==========================================
        # PROGRESO
        # ==========================================

        self.barra_progreso = QProgressBar()

        self.barra_progreso.setValue(0)

        layout.addWidget(self.barra_progreso)

        # ==========================================
        # BOTÓN PROCESAR
        # ==========================================

        self.btn_procesar = QPushButton(
            "Procesar archivos"
        )

        self.btn_procesar.setMinimumHeight(45)

        self.btn_procesar.setEnabled(False)

        self.btn_procesar.clicked.connect(
            self.procesar_archivos
        )

        layout.addWidget(self.btn_procesar)

    # ==============================================
    # SELECCIONAR CARPETA
    # ==============================================

    def seleccionar_carpeta(self):

        carpeta = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar carpeta con archivos Excel"
        )

        if not carpeta:
            return

        self.carpeta_seleccionada = carpeta

        self.lbl_carpeta.setText(carpeta)

        self.buscar_archivos()

    # ==============================================
    # BUSCAR ARCHIVOS EXCEL
    # ==============================================

    def buscar_archivos(self):

        self.lista_archivos.clear()

        archivos = []

        for archivo in os.listdir(
            self.carpeta_seleccionada
        ):

            if archivo.lower().endswith(".xlsx"):

                archivos.append(archivo)

        archivos.sort()

        for archivo in archivos:

            self.lista_archivos.addItem(archivo)

        self.lbl_total.setText(
            f"Archivos encontrados: {len(archivos)}"
        )

        self.barra_progreso.setValue(0)

        self.lbl_procesados.setText(
            "Procesados correctamente: 0"
        )

        self.lbl_errores.setText(
            "Con errores: 0"
        )

        if archivos:

            self.btn_procesar.setEnabled(True)

        else:

            self.btn_procesar.setEnabled(False)

    # ==============================================
    # PROCESAR ARCHIVOS
    # ==============================================

    def procesar_archivos(self):

        archivos = []

        for i in range(
            self.lista_archivos.count()
        ):

            texto = self.lista_archivos.item(i).text()

            # Ignorar archivos que ya fueron procesados
            # o que tuvieron error
            if texto.startswith("✔") or texto.startswith("✖"):
                continue

            ruta = os.path.join(
                self.carpeta_seleccionada,
                texto
            )

            archivos.append(ruta)

        total = len(archivos)

        if total == 0:
            return

        procesados = 0
        errores = 0
        marcaciones_nuevas = 0
        marcaciones_duplicadas = 0

        self.barra_progreso.setValue(0)

        self.lbl_procesados.setText(
            "Procesados correctamente: 0"
        )

        self.lbl_errores.setText(
            "Con errores: 0"
        )

        # ==========================================
        # PROCESAR CADA ARCHIVO
        # ==========================================

        for numero, ruta in enumerate(
            archivos,
            start=1
        ):

            nombre_archivo = os.path.basename(ruta)

            # ======================================
            # LEER EXCEL
            # ======================================

            resultado = leer_excel(ruta)

            if not resultado["ok"]:

                errores += 1

                self.lista_archivos.item(
                    numero - 1
                ).setText(
                    f"✖ {nombre_archivo} - "
                    f"Error al leer Excel"
                )

                print(
                    f"ERROR leyendo {ruta}: "
                    f"{resultado['error']}"
                )

            else:

                df = resultado["datos"]

                # ==================================
                # VALIDAR COLUMNAS
                # ==================================

                validacion = validar_columnas(df)

                if not validacion["ok"]:

                    errores += 1

                    faltantes = ", ".join(
                        validacion["faltantes"]
                    )

                    self.lista_archivos.item(
                        numero - 1
                    ).setText(
                        f"✖ {nombre_archivo} - "
                        f"Faltan: {faltantes}"
                    )

                    print(
                        f"ERROR en {ruta}: "
                        f"faltan columnas "
                        f"{validacion['faltantes']}"
                    )

                else:

                    # ==================================
                    # GUARDAR EN MYSQL
                    # ==================================

                    resultado_bd = importar_dataframe(df)

                    if not resultado_bd["ok"]:

                        errores += 1

                        self.lista_archivos.item(
                            numero - 1
                        ).setText(
                            f"✖ {nombre_archivo} - "
                            f"Error MySQL"
                        )

                        print(
                            f"ERROR MySQL en "
                            f"{nombre_archivo}: "
                            f"{resultado_bd['error']}"
                        )

                    else:

                        procesados += 1

                        marcaciones_nuevas += (
                            resultado_bd["marcaciones"]
                        )

                        marcaciones_duplicadas += (
                            resultado_bd["duplicadas"]
                        )

                        self.lista_archivos.item(
                            numero - 1
                        ).setText(
                            f"✔ {nombre_archivo} - "
                            f"{resultado_bd['marcaciones']} "
                            f"nuevas"
                        )

                        print(
                            f"OK: {nombre_archivo} "
                            f"→ "
                            f"{resultado_bd['marcaciones']} "
                            f"marcaciones nuevas"
                        )

            # ======================================
            # ACTUALIZAR INTERFAZ
            # ======================================

            self.lbl_procesados.setText(
                f"Procesados correctamente: "
                f"{procesados}"
            )

            self.lbl_errores.setText(
                f"Con errores: {errores}"
            )

            porcentaje = int(
                (numero / total) * 100
            )

            self.barra_progreso.setValue(
                porcentaje
            )

        # ==========================================
        # RESUMEN FINAL
        # ==========================================

        print("")
        print("===================================")
        print("       IMPORTACIÓN TERMINADA")
        print("===================================")
        print(f"Archivos:               {total}")
        print(f"Correctos:              {procesados}")
        print(f"Errores:                {errores}")
        print(f"Marcaciones nuevas:     {marcaciones_nuevas}")
        print(
            f"Marcaciones duplicadas: "
            f"{marcaciones_duplicadas}"
        )
        print("===================================")