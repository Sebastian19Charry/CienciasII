from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

class InterfazHash(QWidget):
    def __init__(self, main_window, anterior):
        super().__init__()
        self.main_window = main_window
        self.anterior = anterior  # Referencia a InterfazExternas

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # === SIDEBAR (Sub-menú Hash) ===
        sidebar = QFrame()
        sidebar.setFixedWidth(330)
        # Usamos un tono ligeramente distinto para indicar jerarquía
        sidebar.setStyleSheet("background-color:#143626;") 
        s = QVBoxLayout(sidebar)
        s.setContentsMargins(0, 0, 0, 0)

        titulo = QLabel("FUNCIONES HASH")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            color: #74c69d; 
            font-size: 22px; 
            font-weight: bold; 
            padding: 40px 20px;
        """)
        s.addWidget(titulo)

        # Opciones específicas de Hash
        opciones = [
            ("  🔑  Hash - Módulo", "Modulo"),
            ("  🔑  Hash - Cuadrado", "Cuadrado"),
            ("  🔑  Hash - Truncamiento", "Truncamiento"),
            ("  🔑  Hash - Plegamiento", "Plegamiento")
        ]

        for texto_mostrar, op in opciones:
            btn = self.boton_hash(texto_mostrar)
            btn.clicked.connect(lambda checked=False, o=op: self.mostrar_algoritmo(o))
            s.addWidget(btn)

        s.addStretch()
        
        # Botón para regresar a la pantalla de Búsquedas Externas
        btn_regresar = self.boton_volver_atras()
        s.addWidget(btn_regresar)

        # === ÁREA DE CONTENIDO (Derecha) ===
        self.local_stack = QStackedWidget()
        self.local_stack.setStyleSheet("background:#f0f7f4;")
        
        # Pantalla inicial del sub-menú
        self.bienvenida = QWidget()
        b_layout = QVBoxLayout(self.bienvenida)
        self.lbl_mensaje = QLabel("Seleccione un método Hash para visualizar")
        self.lbl_mensaje.setAlignment(Qt.AlignCenter)
        self.lbl_mensaje.setStyleSheet("font-size:24px; color:#1b4332; font-weight:bold;")
        b_layout.addStretch()
        b_layout.addWidget(self.lbl_mensaje)
        b_layout.addStretch()
        
        self.local_stack.addWidget(self.bienvenida)

        layout.addWidget(sidebar)
        layout.addWidget(self.local_stack)

    def mostrar_algoritmo(self, nombre):
        # Aquí luego integraremos las tablas o visualizaciones de cada Hash
        self.lbl_mensaje.setText(f"Visualización de:\n{nombre}\n(Área de dibujo lista)")

    def boton_hash(self, t):
        b = QPushButton(t)
        b.setCursor(Qt.PointingHandCursor)
        b.setFixedHeight(55)
        b.setStyleSheet("""
            QPushButton{
                background:transparent;
                color:white;
                padding-left:30px;
                text-align:left;
                border:none;
                font-size:15px;
            }
            QPushButton:hover{
                background:#1b4332;
                color:#74c69d;
            }
        """)
        return b

    def boton_volver_atras(self):
        b = QPushButton("  ⬅  Regresar a Externas")
        b.setCursor(Qt.PointingHandCursor)
        b.setFixedHeight(60)
        b.setStyleSheet("""
            QPushButton{
                background:#143626;
                color:#95d5b2;
                padding-left:30px;
                text-align:left;
                font-size:14px;
                font-weight: bold;
                border-top: 1px solid #2d6a4f;
            }
            QPushButton:hover{
                background:#1b4332;
                color:white;
            }
        """)
        b.clicked.connect(self.regresar)
        return b

    def regresar(self):
        # Regresa a la interfaz anterior (InterfazExternas)
        self.main_window.cambiar_pantalla(self.anterior)