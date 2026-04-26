from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSpinBox, QFileDialog, QScrollArea, QTextEdit, QTabWidget, QSplitter
)
from PySide6.QtCore import Qt
from vista.visualizador_grafo import VisualizadorGrafo
from controlador.arboles.maximaController import MaximaController

class VistaExpansionMaxima(QWidget):
    def __init__(self, main_window, parent_nav):
        super().__init__()
        self.main_window = main_window
        self.parent_nav = parent_nav
        self.controller = MaximaController(self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        # Header Ribbon
        header = QHBoxLayout()
        self.btn_regresar = QPushButton("  ⬅  ")
        self.btn_regresar.setCursor(Qt.PointingHandCursor)
        self.btn_regresar.setFixedSize(35, 35)
        self.btn_regresar.setStyleSheet("background:#1b4332; color:white; border-radius:17px; font-weight:bold;")
        self.btn_regresar.clicked.connect(self.regresar_menu)
        header.addWidget(self.btn_regresar)

        titulo = QLabel("Árbol de Expansión Máxima")
        titulo.setStyleSheet("font-size:22px; font-weight:bold; color:#1b4332;")
        header.addWidget(titulo); header.addStretch()
        layout.addLayout(header)

        # Controles Ribbon
        controles = QFrame()
        controles.setStyleSheet("background-color: #f8fcf9; border: 1px solid #d8e3dc; border-radius: 8px;")
        controles_layout = QHBoxLayout(controles)
        controles_layout.setContentsMargins(10, 5, 10, 5)
        
        controles_layout.addWidget(QLabel("V:"))
        self.vertices_spin = QSpinBox()
        self.vertices_spin.setRange(2, 15); self.vertices_spin.setValue(4)
        controles_layout.addWidget(self.vertices_spin)
        
        self.btn_crear = self.boton_accion("Reiniciar")
        self.btn_crear.clicked.connect(self.controller.crear_grafo)
        controles_layout.addWidget(self.btn_crear)
        
        self.btn_agregar_arista = self.boton_accion("+ Arista")
        self.btn_agregar_arista.clicked.connect(self.controller.agregar_arista)
        controles_layout.addWidget(self.btn_agregar_arista)
        
        controles_layout.addStretch()
        
        self.btn_ejecutar = self.boton_accion("🌳 EJECUTAR")
        self.btn_ejecutar.setStyleSheet(self.btn_ejecutar.styleSheet() + "QPushButton { background: #1b4332; }")
        self.btn_ejecutar.clicked.connect(self.controller.ejecutar_algoritmo)
        controles_layout.addWidget(self.btn_ejecutar)
        layout.addWidget(controles)

        # Main Vertical Splitter
        v_splitter = QSplitter(Qt.Vertical)
        
        # Top: Visualización (Horizontal Splitter)
        h_splitter = QSplitter(Qt.Horizontal)
        self.visual_grafo = VisualizadorGrafo("G Original", self, es_editable=True)
        self.visual_arbol = VisualizadorGrafo("A.E.Máx.", self, es_editable=False)
        self.visual_grafo.etiqueta_cambiada.connect(self.controller.actualizar_etiqueta)
        self.visual_grafo.ponderacion_cambiada.connect(self.controller.actualizar_ponderacion)
        h_splitter.addWidget(self.visual_grafo)
        h_splitter.addWidget(self.visual_arbol)
        v_splitter.addWidget(h_splitter)

        # Bottom: Tabs de Resultados
        self.tabs_resultados = QTabWidget()
        self.tabs_resultados.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #d8e3dc; border-radius: 8px; background: white; }
            QTabBar::tab { background: #f0f7f4; padding: 6px 12px; border-top-left-radius: 6px; border-top-right-radius: 6px; color: #1b4332; font-weight: bold; font-size: 11px; }
            QTabBar::tab:selected { background: white; border: 1px solid #d8e3dc; border-bottom-color: white; color: #2d6a4f; }
        """)
        
        self.info_text = QTextEdit(); self.info_text.setReadOnly(True)
        self.circuitos_text = QTextEdit(); self.circuitos_text.setReadOnly(True)
        self.circuitos_fund_text = QTextEdit(); self.circuitos_fund_text.setReadOnly(True)
        self.conjuntos_text = QTextEdit(); self.conjuntos_text.setReadOnly(True)
        self.matrices_text = QTextEdit(); self.matrices_text.setReadOnly(True)
        
        self.tabs_resultados.addTab(self.info_text, "📊 Info")
        self.tabs_resultados.addTab(self.circuitos_text, "🔄 Ciclos")
        self.tabs_resultados.addTab(self.circuitos_fund_text, "⭕ Fund.")
        self.tabs_resultados.addTab(self.conjuntos_text, "✂️ Cortes")
        self.tabs_resultados.addTab(self.matrices_text, "📋 Mat.")
        
        v_splitter.addWidget(self.tabs_resultados)
        v_splitter.setStretchFactor(0, 2)
        v_splitter.setStretchFactor(1, 1)
        
        layout.addWidget(v_splitter)

    def boton_accion(self, t):
        btn = QPushButton(t)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background: #2d6a4f;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 13px;
                border: none;
            }
            QPushButton:hover {
                background: #40916c;
            }
            QPushButton:pressed {
                background: #1b4332;
            }
        """)
        return btn

    def regresar_menu(self):
        self.parent_nav.regresar_a_menu()
