ESTILO_APLICACION = """

QMainWindow {
    background-color: #f3f4f6;
}

QWidget {
    font-family: "Segoe UI";
    font-size: 14px;
    color: #1f2937;
}


/* =========================
   MENÚ LATERAL
   ========================= */

QWidget#menu {
    background-color: #1f2937;
}

QLabel#titulo {
    color: #ffffff;
    font-size: 28px;
    font-weight: bold;
    padding-top: 15px;
}

QLabel#subtitulo {
    color: #d1d5db;
    font-size: 13px;
}

QLabel#version {
    color: #9ca3af;
    font-size: 11px;
    padding-bottom: 10px;
}


/* =========================
   BOTONES DEL MENÚ
   ========================= */

QWidget#menu QPushButton {

    color: #e5e7eb;

    text-align: left;

    padding: 10px 14px;

    border: none;

    border-radius: 6px;

    background-color: transparent;

}

QWidget#menu QPushButton:hover {

    background-color: #374151;

    color: #ffffff;

}

QWidget#menu QPushButton[activo="true"] {

    background-color: #2563eb;

    color: #ffffff;

    font-weight: bold;

}

QWidget#menu QPushButton[activo="true"]:hover {

    background-color: #1d4ed8;

}

QWidget#menu QPushButton:pressed {

    background-color: #4b5563;

}

QWidget#menu QPushButton[activo="true"]:pressed {

    background-color: #1d4ed8;

}

/* =========================
   BOTONES GENERALES
   ========================= */

QPushButton {
    color: #1f2937;
    background-color: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 9px 16px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #f3f4f6;
    border-color: #9ca3af;
}

QPushButton:pressed {
    background-color: #e5e7eb;
}


/* =========================
   TABLAS
   ========================= */

QTableWidget {
    background-color: #ffffff;
    color: #1f2937;
    border: 1px solid #d1d5db;
    gridline-color: #e5e7eb;
    selection-background-color: #dbeafe;
    selection-color: #1e3a8a;
}

QHeaderView::section {
    background-color: #374151;
    color: #ffffff;
    padding: 9px;
    border: none;
    font-weight: bold;
}


/* =========================
   LISTAS
   ========================= */

QListWidget {
    background-color: #ffffff;
    color: #1f2937;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 5px;
}

QListWidget::item {
    padding: 7px;
}

QListWidget::item:selected {
    background-color: #dbeafe;
    color: #1e3a8a;
}


/* =========================
   CAMPOS DE TEXTO
   ========================= */

QLineEdit,
QTextEdit,
QPlainTextEdit {
    background-color: #ffffff;
    color: #1f2937;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 8px;
}

QLineEdit:focus,
QTextEdit:focus,
QPlainTextEdit:focus {
    border: 1px solid #2563eb;
}


/* =========================
   COMBOBOX
   ========================= */

QComboBox {
    background-color: #ffffff;
    color: #1f2937;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 8px;
}


/* =========================
   BARRA DE PROGRESO
   ========================= */

QProgressBar {
    background-color: #e5e7eb;
    color: #1f2937;
    border: none;
    border-radius: 5px;
    text-align: center;
    height: 18px;
}

QProgressBar::chunk {
    background-color: #2563eb;
    border-radius: 5px;
}


/* =========================
   ETIQUETAS GENERALES
   ========================= */

QLabel {
    color: #1f2937;
}

/* =========================
   PÁGINA PRINCIPAL
   ========================= */

QLabel#tituloPagina {
    color: #111827;
    font-size: 28px;
    font-weight: bold;
}

QLabel#subtituloPagina {
    color: #6b7280;
    font-size: 14px;
}

QLabel#tituloSeccion {
    color: #111827;
    font-size: 18px;
    font-weight: bold;
    margin-top: 10px;
}

QFrame#tarjeta {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
}

QLabel#tarjetaTitulo {
    color: #6b7280;
    font-size: 13px;
}

QLabel#tarjetaValor {
    color: #111827;
    font-size: 25px;
    font-weight: bold;
    padding-top: 5px;
}

QLabel#tarjetaDescripcion {
    color: #9ca3af;
    font-size: 12px;
}

QFrame#panel {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
}

QFrame#panel QLabel {
    color: #374151;
    padding: 4px;
}

"""