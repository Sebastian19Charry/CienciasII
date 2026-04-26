"""
dialogo_clave.py
Diálogo de mensaje informativo (reemplaza QMessageBox con estilo del proyecto).
Uso idéntico al proyecto de referencia CienciasII-main:
    DialogoClave(0, "Título", "mensaje", parent, "Texto del mensaje.").exec()
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame
)
from PySide6.QtCore import Qt


class DialogoClave(QDialog):
    """
    Diálogo de mensaje simple con estilo del proyecto.
    Parámetros (compatibles con referencia):
        tipo    : ignorado (compatibilidad)
        titulo  : título de la ventana
        subtipo : ignorado (compatibilidad)
        parent  : widget padre
        mensaje : texto a mostrar
    """

    def __init__(self, tipo, titulo, subtipo, parent=None, mensaje=""):
        super().__init__(parent)
        self.setWindowTitle(titulo or "Información")
        self.setModal(True)
        self.setMinimumWidth(320)
        self.setStyleSheet("""
            QDialog  { background:#f0f7f4; }
            QLabel   { color:#1b4332; font-family:'Segoe UI',Arial; }
            QPushButton {
                background:#1b4332; color:white; font-weight:bold;
                border:none; border-radius:8px; padding:8px 24px; font-size:13px;
            }
            QPushButton:hover { background:#2d6a4f; }
        """)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 20, 20, 16)
        lay.setSpacing(12)

        # Título
        lbl_titulo = QLabel(f"<b>{titulo}</b>")
        lbl_titulo.setStyleSheet("font-size:16px; color:#1b4332;")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        lay.addWidget(lbl_titulo)

        # Separador
        sep = QFrame(); sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color:#d8e3dc;"); lay.addWidget(sep)

        # Mensaje
        lbl_msg = QLabel(str(mensaje))
        lbl_msg.setWordWrap(True)
        lbl_msg.setAlignment(Qt.AlignCenter)
        lbl_msg.setStyleSheet("font-size:13px; color:#2d6a4f; padding:6px 0;")
        lay.addWidget(lbl_msg)

        # Botón OK
        btn_ok = QPushButton("Aceptar")
        btn_ok.clicked.connect(self.accept)
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(btn_ok)
        btn_row.addStretch()
        lay.addLayout(btn_row)
