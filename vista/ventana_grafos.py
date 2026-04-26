from PySide6.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QVBoxLayout,
    QPushButton, QFrame, QStackedWidget
)
from PySide6.QtCore import Qt
from vistaOperaciones.operaciones import InterfazOperaciones
from .interfaz_algoritmos_grafos import InterfazAlgoritmosGrafos
from .interfaz_arboles_grafos import InterfazArbolesGrafos
from vistaOperaciones.operaciones import InterfazOperaciones

class VentanaGrafos(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.layout_principal = QHBoxLayout(self)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)

        # ===== SIDEBAR (Graph Main Menu) =====
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(330)
        self.sidebar.setStyleSheet("background-color: #1b4332;")
        self.s_layout = QVBoxLayout(self.sidebar)
        self.s_layout.setContentsMargins(0, 0, 0, 0); self.s_layout.setSpacing(0)

        titulo = QLabel("GRAFOS")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color:white; font-size:24px; font-weight:bold; padding:40px 20px;")
        self.s_layout.addWidget(titulo)

        btn_alg = self.crear_boton("  📂  Algoritmos")
        btn_arb = self.crear_boton("  🌲  Árboles")
        btn_ope = self.crear_boton("  ⚙️  Operaciones")
        btn_vol = self.crear_boton("  ⬅  Volver")

        btn_alg.clicked.connect(self.abrir_algoritmos)
        btn_arb.clicked.connect(self.abrir_arboles)
        btn_ope.clicked.connect(self.abrir_operaciones)
        btn_vol.clicked.connect(self.main_window.volver_inicio)

        self.s_layout.addWidget(btn_alg)
        self.s_layout.addWidget(btn_arb)
        self.s_layout.addWidget(btn_ope)
        self.s_layout.addSpacing(20)
        self.s_layout.addWidget(btn_vol)
        self.s_layout.addStretch()

        # ===== STACK DE CONTENIDO (DERECHA) =====
        self.local_stack = QStackedWidget()
        self.local_stack.setStyleSheet("background-color: #f0f7f4;")
        
        # Vista de Bienvenida
        bienvenida = QWidget()
        v_layout = QVBoxLayout(bienvenida)
        lbl_inicio = QLabel("Seleccione una categoría del menú de grafos")
        lbl_inicio.setStyleSheet("font-size: 26px; color: #1b4332; font-weight: bold;")
        lbl_inicio.setAlignment(Qt.AlignCenter)
        v_layout.addStretch(); v_layout.addWidget(lbl_inicio); v_layout.addStretch()
        self.local_stack.addWidget(bienvenida)

        self.layout_principal.addWidget(self.sidebar)
        self.layout_principal.addWidget(self.local_stack)

        # Initialize child interfaces
        self.interfaz_alg = InterfazAlgoritmosGrafos(self.main_window, self)
        self.interfaz_arb = InterfazArbolesGrafos(self.main_window, self)
        self.interfaz_op = InterfazOperaciones(self.main_window, self)

    def abrir_algoritmos(self):
        self.main_window.cambiar_pantalla(self.interfaz_alg)

    def abrir_arboles(self):
        self.main_window.cambiar_pantalla(self.interfaz_arb)

    def abrir_operaciones(self):
        self.main_window.cambiar_pantalla(self.interfaz_op)

    def crear_boton(self, texto):
        btn = QPushButton(texto)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(60)
        btn.setStyleSheet("""
            QPushButton { background-color: #2d6a4f; color: white; padding-left: 30px; 
                          text-align: left; border: none; font-size: 17px; font-weight: 500; }
            QPushButton:hover { background-color: #40916c; }
        """)
        return btn