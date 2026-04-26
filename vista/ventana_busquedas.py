from PySide6.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QVBoxLayout,
    QPushButton, QFrame, QStackedWidget
)
from PySide6.QtCore import Qt


from .interfaz_internas import InterfazInternas
from .interfaz_externas import InterfazExternas
from .VistaIndices import VistaIndices


class VentanaBusquedas(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ===== SIDEBAR =====
        sidebar = QFrame()
        sidebar.setFixedWidth(330)
        sidebar.setStyleSheet("background-color: #1b4332;")
        s_layout = QVBoxLayout(sidebar)
        s_layout.setContentsMargins(0, 0, 0, 0)

        titulo = QLabel("BÚSQUEDAS")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color:white; font-size:24px; font-weight:bold; padding:40px 20px;")
        s_layout.addWidget(titulo)

        btn_internas = self.boton("  📁  Internas")
        btn_externas = self.boton("  🌐  Externas")
        btn_indices = self.boton("  📌  Índices")
        btn_volver = self.boton("  ⬅  Volver")

        btn_internas.clicked.connect(self.abrir_internas)
        btn_externas.clicked.connect(self.abrir_externas)
        btn_indices.clicked.connect(self.abrir_indices)
        btn_volver.clicked.connect(self.volver_inicio)

        s_layout.addWidget(btn_internas)
        s_layout.addWidget(btn_externas)
        s_layout.addWidget(btn_indices)
        s_layout.addSpacing(20)
        s_layout.addWidget(btn_volver)
        s_layout.addStretch()

        # ===== STACK DE CONTENIDO LOCAL =====
        self.local_stack = QStackedWidget()
        self.local_stack.setStyleSheet("background-color:#f0f7f4;")
        
        # Widget de bienvenida
        bienvenida = QWidget()
        b_layout = QVBoxLayout(bienvenida)
        label = QLabel("Seleccione un tipo de búsqueda")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size:28px; color:#1b4332; font-weight:bold;")
        b_layout.addStretch()
        b_layout.addWidget(label)
        b_layout.addStretch()
        
        self.local_stack.addWidget(bienvenida)

        layout.addWidget(sidebar)
        layout.addWidget(self.local_stack)

    def boton(self, texto):
        btn = QPushButton(texto)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(60)
        btn.setStyleSheet("""
            QPushButton{
                background-color:#2d6a4f;
                color:white;
                padding-left:30px;
                text-align:left;
                border:none;
                font-size:17px;
                font-weight:500;
            }
            QPushButton:hover{
                background-color:#40916c;
            }
        """)
        return btn

    def abrir_internas(self):
        self.i = InterfazInternas(self.main_window, self)
        self.main_window.cambiar_pantalla(self.i)

    def abrir_externas(self):
        self.e = InterfazExternas(self.main_window, self)
        self.main_window.cambiar_pantalla(self.e)

    # En VentanaBusquedas.py
    def abrir_indices(self):
        # Ahora pasamos 'self.main_window' y 'self' (como parent_window)
        # Esto soluciona el TypeError de los 3 argumentos
        self.ind = VistaIndices(self.main_window, self)
        self.main_window.cambiar_pantalla(self.ind)

    def volver_inicio(self):
        self.main_window.volver_inicio()
