from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from .vista_lineal import VistaBusquedaLineal
from .vista_binaria import VistaBusquedaBinaria
from .interfaz_hash import InterfazHash
from .interfaz_arboles import InterfazArboles


class InterfazInternas(QWidget):
    def __init__(self, main_window, anterior):
        super().__init__()
        self.main_window = main_window
        self.anterior = anterior

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ---------- SIDEBAR ----------
        sidebar = QFrame()
        sidebar.setFixedWidth(330)
        sidebar.setStyleSheet("background-color:#1b4332;")  # Deep Green sidebar
        s = QVBoxLayout(sidebar)
        s.setContentsMargins(0, 0, 0, 0)

        titulo = QLabel("BÚSQUEDAS INTERNAS")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            color:white;
            font-size:22px;
            font-weight:bold;
            padding:40px 20px;
        """)
        s.addWidget(titulo)

        # ---------- BOTONES ----------
        btn_secuencial = self.boton("  🔢  Secuencial")
        btn_binaria = self.boton("  ⚖️  Binaria")
        btn_hash = self.boton("  🔑  Funciones Hash")
        btn_arboles = self.boton("  🌳  Árboles de búsqueda")

        # ---------- CONEXIONES ----------
        btn_secuencial.clicked.connect(self.abrir_secuencial)
        btn_binaria.clicked.connect(self.abrir_binaria)
        btn_hash.clicked.connect(self.abrir_hash)
        btn_arboles.clicked.connect(self.abrir_arboles)

        for b in [btn_secuencial, btn_binaria, btn_hash, btn_arboles]:
            s.addWidget(b)

        s.addStretch()
        s.addWidget(self.boton_volver())

        # ---------- STACK DE CONTENIDO LOCAL ----------
        self.local_stack = QStackedWidget()
        self.local_stack.setStyleSheet("background:#f0f7f4;")  # Soft Mint background
        
        bienvenida = QWidget()
        b_layout = QVBoxLayout(bienvenida)
        label = QLabel("Seleccione un algoritmo de búsqueda interna")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size:26px; color:#1b4332; font-weight:bold;")
        b_layout.addStretch()
        b_layout.addWidget(label)
        b_layout.addStretch()
        
        self.local_stack.addWidget(bienvenida)

        layout.addWidget(sidebar)
        layout.addWidget(self.local_stack)

    # ---------- COMPONENTES ----------
    def boton(self, texto):
        b = QPushButton(texto)
        b.setCursor(Qt.PointingHandCursor)
        b.setFixedHeight(60)
        b.setStyleSheet("""
            QPushButton{
                background:#2d6a4f;
                color:white;
                padding-left:30px;
                text-align:left;
                border:none;
                font-size:16px;
                font-weight:500;
            }
            QPushButton:hover{
                background:#40916c;
            }
        """)
        return b

    def boton_volver(self):
        b = QPushButton("  ⬅  Volver")
        b.setCursor(Qt.PointingHandCursor)
        b.setFixedHeight(60)
        b.setStyleSheet("""
            QPushButton{
                background:#1b4332;
                color:white;
                padding-left:30px;
                text-align:left;
                font-size:15px;
                border-top: 1px solid #40916c;
            }
            QPushButton:hover{
                background:#2d6a4f;
            }
        """)
        b.clicked.connect(self.regresar)
        return b

    # ---------- NAVEGACIÓN ----------
    def regresar(self):
        self.main_window.cambiar_pantalla(self.anterior)

    def cambiar_algoritmo(self, widget):
        # Check if widget is already in local stack
        idx = self.local_stack.indexOf(widget)
        if idx == -1:
            idx = self.local_stack.addWidget(widget)
        self.local_stack.setCurrentIndex(idx)

    def abrir_secuencial(self):
        from .vista_lineal import VistaBusquedaLineal
        self.v = VistaBusquedaLineal(self.main_window)
        self.cambiar_algoritmo(self.v)

    def abrir_binaria(self):
        from .vista_binaria import VistaBusquedaBinaria
        self.b = VistaBusquedaBinaria(self.main_window)
        self.cambiar_algoritmo(self.b)

    def abrir_hash(self):
        from .interfaz_hash import InterfazHash
        self.h = InterfazHash(self.main_window, self)
        # Hash interface is also a full sidebar-content switcher, 
        # normally we'd switch the main stack here.
        self.main_window.cambiar_pantalla(self.h)

    def abrir_arboles(self):
        from .interfaz_arboles import InterfazArboles
        self.a = InterfazArboles(self.main_window, self)
        self.main_window.cambiar_pantalla(self.a)
