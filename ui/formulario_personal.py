from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QLabel
)


class FormularioPersonal(QDialog):

    def __init__(self, parent=None, datos_iniciales=None):
        super().__init__(parent)

        self.datos = None

        # -----------------------------
        # TÍTULO DE LA VENTANA
        # -----------------------------

        if datos_iniciales:
            self.setWindowTitle("Editar trabajador")
        else:
            self.setWindowTitle("Nuevo trabajador")

        self.setMinimumWidth(450)

        # -----------------------------
        # LAYOUT PRINCIPAL
        # -----------------------------

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(18)

        # -----------------------------
        # TÍTULO
        # -----------------------------

        if datos_iniciales:
            titulo = QLabel("Editar trabajador")
            subtitulo = QLabel(
                "Modifique los datos del trabajador"
            )
        else:
            titulo = QLabel("Registrar trabajador")
            subtitulo = QLabel(
                "Ingrese los datos del trabajador"
            )

        titulo.setObjectName("tituloPagina")
        subtitulo.setObjectName("subtituloPagina")

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)

        # -----------------------------
        # FORMULARIO
        # -----------------------------

        formulario = QFormLayout()
        formulario.setSpacing(12)

        self.id_usuario = QLineEdit()
        self.id_usuario.setPlaceholderText("Ejemplo: 1006")

        self.nombre = QLineEdit()
        self.nombre.setPlaceholderText("Nombre")

        self.apellido = QLineEdit()
        self.apellido.setPlaceholderText("Apellido")

        self.tarjeta = QLineEdit()
        self.tarjeta.setPlaceholderText("Número de tarjeta")

        self.estado = QComboBox()
        self.estado.addItems([
            "Activo",
            "Inactivo"
        ])

        formulario.addRow(
            "ID Usuario:",
            self.id_usuario
        )

        formulario.addRow(
            "Nombre:",
            self.nombre
        )

        formulario.addRow(
            "Apellido:",
            self.apellido
        )

        formulario.addRow(
            "N.º Tarjeta:",
            self.tarjeta
        )

        formulario.addRow(
            "Estado:",
            self.estado
        )

        layout.addLayout(formulario)

        # -----------------------------
        # CARGAR DATOS SI ES EDICIÓN
        # -----------------------------

        if datos_iniciales:

            self.id_usuario.setText(
                datos_iniciales[0]
            )

            self.nombre.setText(
                datos_iniciales[1]
            )

            self.apellido.setText(
                datos_iniciales[2]
            )

            self.tarjeta.setText(
                datos_iniciales[3]
            )

            indice_estado = self.estado.findText(
                datos_iniciales[4]
            )

            if indice_estado >= 0:
                self.estado.setCurrentIndex(
                    indice_estado
                )

        # -----------------------------
        # BOTONES
        # -----------------------------

        botones = QHBoxLayout()

        boton_cancelar = QPushButton("Cancelar")
        boton_guardar = QPushButton(
            "Guardar cambios"
            if datos_iniciales
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

    # -----------------------------
    # GUARDAR
    # -----------------------------

    def guardar(self):

        id_usuario = self.id_usuario.text().strip()
        nombre = self.nombre.text().strip()
        apellido = self.apellido.text().strip()
        tarjeta = self.tarjeta.text().strip()
        estado = self.estado.currentText()

        # -----------------------------
        # VALIDACIONES
        # -----------------------------

        if not id_usuario:
            self.id_usuario.setFocus()
            return

        if not nombre:
            self.nombre.setFocus()
            return

        if not apellido:
            self.apellido.setFocus()
            return

        # -----------------------------
        # VALIDAR ID
        # -----------------------------

        if not id_usuario.isdigit():
            self.id_usuario.setFocus()
            return

        # -----------------------------
        # GUARDAR DATOS
        # -----------------------------

        self.datos = (
            id_usuario,
            nombre,
            apellido,
            tarjeta,
            estado
        )

        self.accept()