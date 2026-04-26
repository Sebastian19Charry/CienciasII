from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame
)
from PySide6.QtCore import Qt
from vista.vista_arbol_expansion import VistaArbolExpansion
from vista.vista_arbol_central import VistaArbolCentral
from vista.vista_distancia_arboles import VistaDistanciaArboles

class InterfazArbolesGrafos(QWidget):
    def __init__(self, main_window, anterior):
        super().__init__()
        self.main_window = main_window
        self.anterior = anterior
        
        self.layout_principal = QHBoxLayout(self)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)
        
        # Sidebar estandarizado
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(330)
        self.sidebar.setStyleSheet("background-color: #1b4332;")
        s_layout = QVBoxLayout(self.sidebar)
        s_layout.setContentsMargins(0, 0, 0, 0); s_layout.setSpacing(0)
        
        titulo = QLabel("MÓDULO ÁRBOLES")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color:white; font-size:24px; font-weight:bold; padding:40px 20px;")
        s_layout.addWidget(titulo)

        # Botones de Algoritmos
        self.btn_min = self.crear_boton("  📉 Expansión Mínima")
        self.btn_max = self.crear_boton("  📈 Expansión Máxima")
        self.btn_central = self.crear_boton("  🎯 Árbol Central")
        self.btn_dist = self.crear_boton("  📏 Distancia entre Árboles")
        self.btn_volver = self.crear_boton("  ⬅ Volver al Menú")
        
        s_layout.addWidget(self.btn_min)
        s_layout.addWidget(self.btn_max)
        s_layout.addWidget(self.btn_central)
        s_layout.addWidget(self.btn_dist)
        s_layout.addSpacing(20)
        s_layout.addWidget(self.btn_volver)
        s_layout.addStretch()
        
        # Contenido de Bienvenida
        self.contenido = QWidget()
        self.contenido.setStyleSheet("background-color: #f0f7f4;")
        cont_lay = QVBoxLayout(self.contenido)
        cont_lay.addStretch()
        lbl_msg = QLabel("SELECCIONE UNA OPERACIÓN DE ÁRBOLES")
        lbl_msg.setAlignment(Qt.AlignCenter)
        lbl_msg.setStyleSheet("font-size: 26px; font-weight: bold; color: #1b4332;")
        cont_lay.addWidget(lbl_msg)
        lbl_hint = QLabel("Gestión avanzada de árboles de expansión y métricas estructurales")
        lbl_hint.setAlignment(Qt.AlignCenter)
        lbl_hint.setStyleSheet("font-size: 16px; color: #2d6a4f;")
        cont_lay.addWidget(lbl_hint)
        cont_lay.addStretch()
        
        self.layout_principal.addWidget(self.sidebar)
        self.layout_principal.addWidget(self.contenido)
        
        # Conexiones con Screens Full
        self.btn_min.clicked.connect(lambda: self.abrir_expansion("minimo"))
        self.btn_max.clicked.connect(lambda: self.abrir_expansion("maximo"))
        self.btn_central.clicked.connect(self.abrir_central)
        self.btn_dist.clicked.connect(self.abrir_distancia)
        self.btn_volver.clicked.connect(self.regresar)

    def regresar(self):
        self.main_window.cambiar_pantalla(self.anterior)

    def abrir_expansion(self, modo):
        view = VistaArbolExpansion(self.main_window, self, modo)
        self.main_window.cambiar_pantalla(view)

    def abrir_central(self):
        view = VistaArbolCentral(self.main_window, self)
        self.main_window.cambiar_pantalla(view)

    def abrir_distancia(self):
        view = VistaDistanciaArboles(self.main_window, self)
        self.main_window.cambiar_pantalla(view)

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
