from PySide6.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QVBoxLayout,
    QPushButton, QFrame, QStackedWidget, QScrollArea
)
from PySide6.QtCore import Qt

# Importaciones de las interfaces de operaciones
from .union import InterfazUnion
from .interseccion import InterfazInterseccion 
from .sumaAnillos import InterfazSumaAnillos
from .suma import InterfazSuma
from .fusionVertices import InterfazFusionVertices
from .eliminacion import InterfazEliminacionVertices    
from .contraccion import InterfazContraccionAristas
from .adicion import InterfazAdicionAristas  
from .complemento import InterfazComplemento
from .eliminacionAristas import InterfazEliminacionAristas
class InterfazOperaciones(QWidget):
    def __init__(self, main_window, parent=None):
        super().__init__()
        self.main_window = main_window
        self.parent_v = parent # Referencia a VentanaGrafos

        # Diccionario para cachear las interfaces y no duplicarlas
        self.vistas_operaciones = {}

        self.layout_principal = QHBoxLayout(self)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)

        # ===== SIDEBAR IZQUIERDA =====
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(330)
        self.sidebar.setStyleSheet("background-color: #1b4332; border: none;")
        self.s_layout = QVBoxLayout(self.sidebar)
        self.s_layout.setContentsMargins(0, 0, 0, 0); self.s_layout.setSpacing(0)

        # Header Sidebar
        header = QFrame()
        header.setFixedHeight(120)
        header.setStyleSheet("background-color: #081c15;")
        h_lay = QVBoxLayout(header)
        
        titulo = QLabel("⚙️ OPERACIONES")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color: #b7e4c7; font-size: 24px; font-weight: bold; letter-spacing: 2px;")
        sub_titulo = QLabel("MANIPULACIÓN DE GRAFOS")
        sub_titulo.setAlignment(Qt.AlignCenter)
        sub_titulo.setStyleSheet("color: #74c69d; font-size: 10px; font-weight: bold; text-transform: uppercase;")
        
        h_lay.addStretch(); h_lay.addWidget(titulo); h_lay.addWidget(sub_titulo); h_lay.addStretch()
        self.s_layout.addWidget(header)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none; background-color: transparent;")
        
        container_botones = QWidget()
        container_botones.setStyleSheet("background-color: transparent;")
        self.botones_layout = QVBoxLayout(container_botones)
        self.botones_layout.setContentsMargins(15, 20, 15, 20)
        self.botones_layout.setSpacing(8)

        ops = [
            ("UNIÓN", "Union"), ("INTERSECCIÓN", "Interseccion"), ("SUMA ANILLO", "Suma Anillo"), 
            ("SUMA (JOIN)", "Suma"), ("FUSIÓN VÉRTICES", "Fusion Vertices"), 
            ("ELIMINAR VÉRTICE", "Eliminacion Vertices"), ("CONTRACCIÓN ARISTA", "Contraccion Aristas"), 
            ("ADICIÓN ARISTA", "Adicion Aristas"), ("ELIMINAR ARISTA", "Eliminacion Aristas"), 
            ("COMPLEMENTO", "Complemento")
        ]

        self.btn_group = []
        for label, internal_name in ops:
            btn = self.crear_boton_lateral(f"    {label}")
            btn.clicked.connect(lambda checked, n=internal_name, b=btn: self.mostrar_operacion(n, b))
            self.botones_layout.addWidget(btn)
            self.btn_group.append(btn)

        self.botones_layout.addStretch()
        scroll_area.setWidget(container_botones)
        self.s_layout.addWidget(scroll_area)

        # Footer Sidebar (Volver)
        footer = QFrame()
        footer.setFixedHeight(80)
        footer.setStyleSheet("background-color: #081c15;")
        f_lay = QVBoxLayout(footer)
        f_lay.setContentsMargins(15, 10, 15, 10)
        
        btn_volver = QPushButton("  ⬅  VOLVER AL MENÚ")
        btn_volver.setCursor(Qt.PointingHandCursor); btn_volver.setFixedHeight(50)
        btn_volver.setStyleSheet("""
            QPushButton { 
                background-color: #2d6a4f; color: white; border-radius: 10px; 
                font-size: 14px; font-weight: bold; border: 1px solid #40916c;
            }
            QPushButton:hover { background-color: #40916c; border-color: #52b788; }
        """)
        btn_volver.clicked.connect(self.volver_menu_grafos)
        f_lay.addWidget(btn_volver)
        self.s_layout.addWidget(footer)

        # ===== CONTENIDO DERECHA =====
        self.stack_contenido = QStackedWidget()
        self.stack_contenido.setStyleSheet("background-color: #f0f7f4;")
        
        self.vista_inicio = QWidget()
        v_layout = QVBoxLayout(self.vista_inicio)
        lbl = QLabel("SELECCIONE UNA OPERACIÓN\nPARA COMENZAR")
        lbl.setStyleSheet("font-size: 28px; color: #1b4332; font-weight: bold; letter-spacing: 1px;")
        lbl.setAlignment(Qt.AlignCenter)
        v_layout.addStretch(); v_layout.addWidget(lbl); v_layout.addStretch()
        
        self.stack_contenido.addWidget(self.vista_inicio)

        self.layout_principal.addWidget(self.sidebar)
        self.layout_principal.addWidget(self.stack_contenido)

    def crear_boton_lateral(self, texto):
        btn = QPushButton(texto); btn.setCheckable(True); btn.setCursor(Qt.PointingHandCursor); btn.setFixedHeight(50)
        btn.setStyleSheet("""
            QPushButton { 
                background-color: transparent; color: #b7e4c7; text-align: left; 
                border: none; border-radius: 10px; font-size: 13px; font-weight: 600;
                padding-left: 10px;
            }
            QPushButton:hover { background-color: #2d6a4f; color: white; }
            QPushButton:checked { 
                background-color: #40916c; color: white; border-left: 5px solid #b7e4c7;
            }
        """)
        return btn

    def mostrar_operacion(self, nombre, boton_clicado=None):
        # Actualizar estado de botones (Checkable)
        if boton_clicado:
            for b in self.btn_group:
                b.setChecked(b == boton_clicado)

        # Si la vista ya fue creada anteriormente, la recuperamos
        if nombre in self.vistas_operaciones:
            self.stack_contenido.setCurrentWidget(self.vistas_operaciones[nombre])
            return

        nueva_interfaz = None

        if nombre == "Union":
            nueva_interfaz = InterfazUnion(self.main_window) 
        elif nombre == "Interseccion":
            nueva_interfaz = InterfazInterseccion(self.main_window)
        elif nombre == "Suma Anillo":
            nueva_interfaz = InterfazSumaAnillos(self.main_window)
        elif nombre == "Suma":
            nueva_interfaz = InterfazSuma(self.main_window)
        elif nombre == "Fusion Vertices":
            nueva_interfaz = InterfazFusionVertices(self.main_window)
        elif nombre == "Eliminacion Vertices":
            nueva_interfaz = InterfazEliminacionVertices(self.main_window)   
        elif nombre == "Contraccion Aristas":
            nueva_interfaz = InterfazContraccionAristas(self.main_window)
        elif nombre == "Adicion Aristas":
            nueva_interfaz = InterfazAdicionAristas(self.main_window)
        elif nombre == "Complemento":
            nueva_interfaz = InterfazComplemento(self.main_window)    
        elif nombre == "Eliminacion Aristas":
            nueva_interfaz = InterfazEliminacionAristas(self.main_window)   

        if nueva_interfaz:
            self.vistas_operaciones[nombre] = nueva_interfaz
            self.stack_contenido.addWidget(nueva_interfaz)
            self.stack_contenido.setCurrentWidget(nueva_interfaz)
        else:
            # Placeholder para operaciones aún no implementadas
            vista_temp = QWidget()
            l = QVBoxLayout(vista_temp)
            msg = QLabel(f"Interfaz de {nombre} en desarrollo...")
            msg.setStyleSheet("font-size: 18px; color: gray;")
            msg.setAlignment(Qt.AlignCenter)
            l.addStretch(); l.addWidget(msg); l.addStretch()
            
            self.stack_contenido.addWidget(vista_temp)
            self.stack_contenido.setCurrentWidget(vista_temp)

    def volver_menu_grafos(self):
        if self.parent_v:
            self.main_window.cambiar_pantalla(self.parent_v)