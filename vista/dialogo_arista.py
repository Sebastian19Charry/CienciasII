from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QDialogButtonBox, QDoubleSpinBox, QFrame
)


class DialogoArista(QDialog):
    """
    Diálogo para seleccionar una arista (origen, destino, peso).
    Compatible con los controladores de árboles de expansión.
    """

    def __init__(self, max_vertices, parent=None, etiquetas=None):
        super().__init__(parent)
        self.setWindowTitle("Gestionar Arista")
        self.setModal(True)
        self.setFixedWidth(300)
        self.etiquetas = etiquetas if etiquetas else {}
        self.setStyleSheet("""
            QDialog  { background:#f0f7f4; }
            QLabel   { color:#1b4332; font-family:Arial; font-weight:bold; }
            QComboBox, QDoubleSpinBox {
                background:white; color:#1b4332; border:1px solid #2d6a4f;
                border-radius:6px; padding:4px 8px; min-height:30px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Origen
        layout.addWidget(QLabel("Nodo Origen:"))
        self.origen = QComboBox()
        for i in range(max_vertices):
            self.origen.addItem(self.etiquetas.get(i, str(i + 1)), i)
        layout.addWidget(self.origen)

        # Destino
        layout.addWidget(QLabel("Nodo Destino:"))
        self.destino = QComboBox()
        for i in range(max_vertices):
            self.destino.addItem(self.etiquetas.get(i, str(i + 1)), i)
        layout.addWidget(self.destino)

        # Peso
        sep = QFrame(); sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color:#d8e3dc;"); layout.addWidget(sep)

        layout.addWidget(QLabel("Peso (ponderación):"))
        self.peso_spin = QDoubleSpinBox()
        self.peso_spin.setRange(-9999, 9999)
        self.peso_spin.setValue(1)
        self.peso_spin.setDecimals(2)
        layout.addWidget(self.peso_spin)

        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_arista(self):
        """Retorna la arista como tupla ordenada (u, v)."""
        u = self.origen.currentData()
        v = self.destino.currentData()
        return tuple(sorted([u, v]))

    def get_peso(self):
        """Retorna el peso ingresado."""
        return self.peso_spin.value()
