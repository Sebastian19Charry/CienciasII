from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QStackedWidget, QFrame
)
from PySide6.QtCore import Qt
from vista.vista_dijkstra import VistaDijkstra
from vista.vista_bellman import VistaBellman
from vista.vista_floyd import VistaFloyd

class InterfazAlgoritmosGrafos(QWidget):
    def __init__(self, main_window, anterior):
        super().__init__()
        self.main_window = main_window
        self.anterior = anterior
        
        self.layout_principal = QHBoxLayout(self)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)
        
        # Sidebar interno para algoritmos
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(330)
        self.sidebar.setStyleSheet("background-color: #1b4332;")
        s_layout = QVBoxLayout(self.sidebar)
        s_layout.setContentsMargins(0, 0, 0, 0); s_layout.setSpacing(0)
        
        titulo = QLabel("ALGORITMOS")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color:white; font-size:24px; font-weight:bold; padding:40px 20px;")
        s_layout.addWidget(titulo)
        
        self.btn_dijkstra = self.crear_boton("  🔢  Dijkstra")
        self.btn_bellman = self.crear_boton("  🔢  Bellman-Ford")
        self.btn_floyd = self.crear_boton("  🔢  Floyd-Warshall")
        self.btn_volver = self.crear_boton("  ⬅  Volver")
        
        s_layout.addWidget(self.btn_dijkstra)
        s_layout.addWidget(self.btn_bellman)
        s_layout.addWidget(self.btn_floyd)
        s_layout.addSpacing(20)
        s_layout.addWidget(self.btn_volver)
        s_layout.addStretch()
        
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: #f0f7f4;")
        
        # Welcome screen for algorithms
        bienvenida = QWidget()
        b_lay = QVBoxLayout(bienvenida)
        lbl = QLabel("Seleccione un algoritmo de rutas cortas")
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-size:26px; color:#1b4332; font-weight:bold;")
        b_lay.addStretch(); b_lay.addWidget(lbl); b_lay.addStretch()
        
        self.view_dijkstra = VistaDijkstra()
        self.view_bellman = VistaBellman()
        self.view_floyd = VistaFloyd()
        
        self.stack.addWidget(bienvenida)      # 0
        self.stack.addWidget(self.view_dijkstra) # 1
        self.stack.addWidget(self.view_bellman)  # 2
        self.stack.addWidget(self.view_floyd)    # 3
        
        self.layout_principal.addWidget(self.sidebar)
        self.layout_principal.addWidget(self.stack)
        
        self.btn_dijkstra.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_bellman.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.btn_floyd.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        self.btn_volver.clicked.connect(self.regresar)

    def regresar(self):
        self.main_window.cambiar_pantalla(self.anterior)

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
