from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from .vista_arboles import VistaArboles


class InterfazArboles(QWidget):
    def __init__(self, main_window, anterior):
        super().__init__()
        self.camino_resaltado = None
        self.main_window = main_window
        self.anterior = anterior

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setFixedWidth(330)
        sidebar.setStyleSheet("background:#1b4332;")  # Deep Green sidebar
        s = QVBoxLayout(sidebar)
        s.setContentsMargins(0, 0, 0, 0)

        titulo = QLabel("ÁRBOLES DE BÚSQUEDA")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color:white; font-size:22px; font-weight:bold; padding:40px 20px;")
        s.addWidget(titulo)

        opciones = [
            ("  🔢  Árboles Digitales", "Árboles Digitales"),
            ("  🍃  Tries de Residuos", "Tries de Residuos"),
            ("  🌳  Múltiples Residuo", "Múltiples Residuos"),
            ("  🎋  Árboles de Huffman", "Árboles de Huffman")
        ]

        for texto_mostrar, op in opciones:
            btn = self.boton(texto_mostrar)
            btn.clicked.connect(lambda checked=False, o=op: self.mostrar_algoritmo(o))
            s.addWidget(btn)

        s.addStretch()
        s.addWidget(self.volver())

        # ---------- STACK DE CONTENIDO LOCAL ----------
        self.local_stack = QStackedWidget()
        self.local_stack.setStyleSheet("background:#f0f7f4;")
        
        bienvenida = QWidget()
        b_layout = QVBoxLayout(bienvenida)
        self.lbl_mensaje = QLabel("Seleccione un tipo de árbol")
        self.lbl_mensaje.setAlignment(Qt.AlignCenter)
        self.lbl_mensaje.setStyleSheet("font-size:26px; color:#1b4332; font-weight:bold;")
        b_layout.addStretch()
        b_layout.addWidget(self.lbl_mensaje)
        b_layout.addStretch()
        
        self.local_stack.addWidget(bienvenida)

        layout.addWidget(sidebar)
        layout.addWidget(self.local_stack)

    def mostrar_algoritmo(self, nombre):
        # Crear la vista correspondiente
        vista = VistaArboles(self.main_window, nombre)
        
        # Añadir al stack y cambiar
        idx = self.local_stack.addWidget(vista)
        self.local_stack.setCurrentIndex(idx)

    def boton(self, t):
        b = QPushButton(t)
        b.setCursor(Qt.PointingHandCursor)
        b.setFixedHeight(60)
        b.setStyleSheet("""
            QPushButton{
                background:#2d6a4f;
                color:white;
                padding-left:30px;
                text-align:left;
                border:none;
                font-size:15px;
                font-weight:500;
            }
            QPushButton:hover{
                background:#40916c;
            }
        """)
        return b

    def volver(self):
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

    def regresar(self):
        self.main_window.cambiar_pantalla(self.anterior)

    def resaltar_camino(self, ruta):
        self.camino_resaltado = ruta
        self.actualizar_dibujo()