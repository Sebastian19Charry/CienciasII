from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QTextEdit, QScrollArea,
    QSpinBox, QFileDialog, QTabWidget, QSplitter
)
from PySide6.QtCore import Qt, QTimer
from vista.visualizador_grafo import VisualizadorGrafo
from vista.dialogo_arista import DialogoArista
from vista.dialogo_clave import DialogoClave
from controlador.arboles.CentralController import CentralController
import math

class VistaExpansionCentral(QWidget):
    def __init__(self, main_window, parent_nav):
        super().__init__()
        self.main_window = main_window
        self.parent_nav = parent_nav
        self.controller = CentralController()
        
        # Estado
        self.num_vertices = 4; self.aristas = []; self.etiquetas = {}
        self.pasos_algoritmo = []; self.paso_actual = 0
        self.timer = QTimer(); self.timer.timeout.connect(self.mostrar_siguiente_paso)

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

        titulo = QLabel("Centro de Árbol")
        titulo.setStyleSheet("font-size:22px; font-weight:bold; color:#1b4332;")
        header.addWidget(titulo); header.addStretch()
        layout.addLayout(header)

        # Controls Ribbon
        controles = QFrame()
        controles.setStyleSheet("background:#f8fcf9; border:1px solid #d8e3dc; border-radius:8px;")
        l_ctrls = QHBoxLayout(controles)
        l_ctrls.setContentsMargins(10, 5, 10, 5)
        l_ctrls.setSpacing(6)

        l_ctrls.addWidget(QLabel("V:"))
        self.sp_v = QSpinBox(); self.sp_v.setRange(3, 15); self.sp_v.setValue(4)
        l_ctrls.addWidget(self.sp_v)

        btn_gen = self.boton_accion("Reiniciar")
        btn_gen.clicked.connect(self.generar_vacio)
        l_ctrls.addWidget(btn_gen)

        btn_add_a = self.boton_accion("+ Arista")
        btn_add_a.clicked.connect(self.agregar_arista)
        l_ctrls.addWidget(btn_add_a)

        btn_del_a = self.boton_accion("− Arista")
        btn_del_a.clicked.connect(self.eliminar_arista)
        l_ctrls.addWidget(btn_del_a)

        l_ctrls.addStretch()

        self.btn_calc = self.boton_accion("▶ EJECUTAR")
        self.btn_calc.setStyleSheet(self.btn_calc.styleSheet() + "QPushButton { background:#1b4332; }")
        self.btn_calc.clicked.connect(self.iniciar_animacion)
        l_ctrls.addWidget(self.btn_calc)

        layout.addWidget(controles)

        # Main Vertical Splitter
        v_splitter = QSplitter(Qt.Vertical)
        
        # Visualizer
        self.visualizador = VisualizadorGrafo("Árbol", self, es_editable=True)
        v_splitter.addWidget(self.visualizador)
        
        # Bottom: Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #d8e3dc; border-radius: 8px; background: white; }
            QTabBar::tab { background: #f0f7f4; padding: 6px 12px; border-top-left-radius: 6px; border-top-right-radius: 6px; color: #1b4332; font-weight: bold; }
            QTabBar::tab:selected { background: white; border: 1px solid #d8e3dc; border-bottom-color: white; color: #2d6a4f; }
        """)
        
        self.tab_pasos = QWidget()
        self.pasos_scroll = QScrollArea(); self.pasos_scroll.setWidgetResizable(True)
        self.pasos_cont = QWidget(); self.pasos_layout = QVBoxLayout(self.pasos_cont)
        self.pasos_scroll.setWidget(self.pasos_cont)
        vp = QVBoxLayout(self.tab_pasos); vp.addWidget(self.pasos_scroll)
        self.tabs.addTab(self.tab_pasos, "Animación Paso a Paso")
        
        self.tab_res = QWidget()
        self.res_text = QTextEdit(); self.res_text.setReadOnly(True)
        vr = QVBoxLayout(self.tab_res); vr.addWidget(self.res_text)
        self.tabs.addTab(self.tab_res, "Reporte Final")
        
        v_splitter.addWidget(self.tabs)
        v_splitter.setStretchFactor(0, 3)
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

    def generar_vacio(self):
        self.num_vertices = self.sp_v.value()
        self.aristas = []
        self.etiquetas = {i: chr(97 + i) for i in range(self.num_vertices)}
        self.visualizador.set_grafo(self.num_vertices, [], self.etiquetas)
        self.limpiar_layout(self.pasos_layout)
        self.res_text.clear()

    def agregar_arista(self):
        if self.num_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "Primero crea el árbol.").exec()
            return
        dlg = DialogoArista(self.num_vertices, self, self.etiquetas)
        if dlg.exec():
            a = dlg.get_arista()
            if a not in self.aristas:
                self.aristas.append(a)
                self.visualizador.set_grafo(
                    self.num_vertices, self.aristas, self.etiquetas)

    def eliminar_arista(self):
        if not self.aristas:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay aristas para eliminar.").exec()
            return
        dlg = DialogoArista(self.num_vertices, self, self.etiquetas)
        if dlg.exec():
            a = dlg.get_arista()
            if a in self.aristas:
                self.aristas.remove(a)
                self.visualizador.set_grafo(
                    self.num_vertices, self.aristas, self.etiquetas)
            else:
                DialogoClave(0, "Error", "mensaje", self,
                             "Esa arista no existe.").exec()

    def limpiar_layout(self, lyt):
        while lyt.count():
            item = lyt.takeAt(0)
            if item.widget(): item.widget().deleteLater()

    def iniciar_animacion(self):
        # Leer datos actuales del visualizador
        datos = self.visualizador.get_datos_grafo()
        self.num_vertices = datos['vertices'] if datos['vertices'] > 0 else self.num_vertices
        self.aristas = datos['aristas']
        self.controller.set_grafo(self.num_vertices, [tuple(a) for a in self.aristas], self.etiquetas)
        
        if not self.controller.es_arbol():
            from vista.dialogo_clave import DialogoClave
            DialogoClave(0, "Error", "mensaje", self, "El grafo no es un árbol válido (n-1 aristas y conexo).").exec()
            return

        self.pasos_algoritmo = self.controller.generar_pasos_algoritmo()
        self.paso_actual = 0
        self.limpiar_layout(self.pasos_layout)
        self.tabs.setCurrentIndex(1)
        self.timer.start(1000)

    def mostrar_siguiente_paso(self):
        if self.paso_actual >= len(self.pasos_algoritmo):
            self.timer.stop(); self.mostrar_reporte(); return
        
        p = self.pasos_algoritmo[self.paso_actual]
        f = QFrame(); f.setStyleSheet("border: 1px solid #d8e3dc; border-radius: 5px; background: white; margin: 5px; padding: 5px;")
        l = QVBoxLayout(f)
        l.addWidget(QLabel(f"<b>{p['titulo']}</b>"))
        l.addWidget(QLabel(p['descripcion']))
        self.pasos_layout.addWidget(f)
        self.paso_actual += 1

    def mostrar_reporte(self):
        c, ex, r, d, det = self.controller.calcular_centro()
        self.res_text.setHtml(self.controller.generar_tabla_distancias_html() + "<br>" + det.replace("\n", "<br>"))
        self.tabs.setCurrentIndex(2)
