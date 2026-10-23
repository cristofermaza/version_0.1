ESTILO_APLICACION = """
/* =========================================================
   CONFIGURACIÓN GENERAL
   ========================================================= */

QMainWindow {
    background-color: #f4f6f8;
    color: #1f2937;
}

QWidget {
    font-family: "Segoe UI";
    font-size: 14px;
    color: #1f2937;
}


/* =========================================================
   TITULOS
   ========================================================= */

QLabel#titulo_pagina {
    color: #111827;
    font-size: 26px;
    font-weight: 700;
}

QLabel#descripcion_pagina {
    color: #4b5563;
    font-size: 14px;
}


/* =========================================================
   MENU LATERAL
   ========================================================= */

QFrame#menu_lateral {
    background-color: #1f2937;
}

QPushButton#boton_menu {
    background-color: transparent;
    color: #f9fafb;
    border: none;
    border-radius: 6px;
    padding: 12px 16px;
    text-align: left;
    font-size: 14px;
}

QPushButton#boton_menu:hover {
    background-color: #374151;
    color: #ffffff;
}

QPushButton#boton_menu:checked {
    background-color: #2563eb;
    color: #ffffff;
    font-weight: 600;
}


/* =========================================================
   BOTONES
   ========================================================= */

QPushButton {
    background-color: #2563eb;
    color: #ffffff;
    border: 1px solid #1d4ed8;
    border-radius: 6px;
    padding: 9px 16px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #1d4ed8;
}

QPushButton:pressed {
    background-color: #1e40af;
}

QPushButton:disabled {
    background-color: #d1d5db;
    color: #6b7280;
    border-color: #d1d5db;
}


/* =========================================================
   CAMPOS DE TEXTO
   ========================================================= */

QLineEdit {
    background-color: #ffffff;
    color: #111827;
    border: 1px solid #9ca3af;
    border-radius: 6px;
    padding: 9px 10px;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
}

QLineEdit:focus {
    border: 2px solid #2563eb;
    padding: 8px 9px;
}

QLineEdit:disabled {
    background-color: #e5e7eb;
    color: #6b7280;
}


/* =========================================================
   COMBOBOX
   ========================================================= */

QComboBox {
    background-color: #ffffff;
    color: #111827;
    border: 1px solid #9ca3af;
    border-radius: 6px;
    padding: 9px 10px;
    min-height: 20px;
}

QComboBox:hover {
    border-color: #6b7280;
}

QComboBox:focus {
    border: 2px solid #2563eb;
}

QComboBox:disabled {
    background-color: #e5e7eb;
    color: #6b7280;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #111827;
    border: 1px solid #9ca3af;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
}


/* =========================================================
   SPINBOX
   ========================================================= */

QSpinBox {
    background-color: #ffffff;
    color: #111827;
    border: 1px solid #9ca3af;
    border-radius: 6px;
    padding: 8px 10px;
}

QSpinBox:focus {
    border: 2px solid #2563eb;
}

QSpinBox:disabled {
    background-color: #e5e7eb;
    color: #6b7280;
}


/* =========================================================
   CHECKBOX
   ========================================================= */

QCheckBox {
    color: #1f2937;
    spacing: 8px;
    padding: 5px;
}

QCheckBox:disabled {
    color: #6b7280;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
}

QCheckBox::indicator:unchecked {
    background-color: #ffffff;
    border: 1px solid #6b7280;
    border-radius: 4px;
}

QCheckBox::indicator:checked {
    background-color: #2563eb;
    border: 1px solid #1d4ed8;
    border-radius: 4px;
}


/* =========================================================
   GROUPBOX
   ========================================================= */

QGroupBox {
    background-color: #ffffff;
    color: #111827;
    border: 1px solid #9ca3af;
    border-radius: 8px;
    margin-top: 14px;
    padding: 18px 12px 12px 12px;
    font-weight: 600;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: #111827;
    background-color: #ffffff;
}


/* =========================================================
   LABELS DENTRO DE FORMULARIOS
   ========================================================= */

QFormLayout QLabel {
    color: #374151;
    font-weight: 500;
}


/* =========================================================
   TABLAS
   ========================================================= */

QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #f9fafb;
    color: #111827;
    border: 1px solid #d1d5db;
    gridline-color: #d1d5db;
    selection-background-color: #dbeafe;
    selection-color: #111827;
}

QHeaderView::section {
    background-color: #e5e7eb;
    color: #111827;
    border: none;
    border-bottom: 1px solid #9ca3af;
    padding: 9px;
    font-weight: 700;
}

QTableWidget::item {
    padding: 7px;
}


/* =========================================================
   TABULADORES
   ========================================================= */

QTabWidget::pane {
    background-color: #ffffff;
    border: 1px solid #9ca3af;
    border-radius: 6px;
}

QTabBar::tab {
    background-color: #e5e7eb;
    color: #374151;
    border: 1px solid #d1d5db;
    padding: 10px 18px;
    margin-right: 2px;
}

QTabBar::tab:hover {
    background-color: #dbeafe;
    color: #1e3a8a;
}

QTabBar::tab:selected {
    background-color: #ffffff;
    color: #1d4ed8;
    border-bottom: 3px solid #2563eb;
    font-weight: 700;
}


/* =========================================================
   MENSAJES
   ========================================================= */

QMessageBox {
    background-color: #ffffff;
    color: #111827;
}

QMessageBox QLabel {
    color: #111827;
}


/* =========================================================
   SCROLLBARS
   ========================================================= */

QScrollBar:vertical {
    background-color: #e5e7eb;
    width: 12px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #9ca3af;
    border-radius: 6px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #6b7280;
}

QScrollBar:horizontal {
    background-color: #e5e7eb;
    height: 12px;
}

QScrollBar::handle:horizontal {
    background-color: #9ca3af;
    border-radius: 6px;
    min-width: 30px;
}


/* =========================================================
   SEPARADORES
   ========================================================= */

QFrame[frameShape="4"] {
    color: #d1d5db;
}

QFrame[frameShape="5"] {
    color: #d1d5db;
}
"""