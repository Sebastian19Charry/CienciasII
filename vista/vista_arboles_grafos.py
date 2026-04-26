from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSpinBox, QTextEdit, QScrollArea, QTabWidget
)
from PySide6.QtCore import Qt
from vista.visualizador_grafo import VisualizadorGrafo
from vista.dialogo_arista import DialogoArista

class VistaArbolesExpansion(QWidget):
    def __init__(self):
        super().__init__()
        self.num_vertices = 0
        self.aristas = []
        self.etiquetas = {}
        self.ponderaciones = {}
        self.arbol_aristas = []
        
        layout = QVBoxLayout(self)
        
        # Ribbon
        ribbon = QFrame(); ribbon.setStyleSheet("background-color: #1b4332; border-radius: 10px;")
        rib_lay = QHBoxLayout(ribbon)
        self.spin = QSpinBox(); self.spin.setRange(2, 10); self.spin.setValue(4)
        btn_crear = QPushButton("🆕 Crear"); btn_crear.clicked.connect(self.crear_grafo)
        btn_add = QPushButton("➕ Arista"); btn_add.clicked.connect(self.add_arista)
        btn_exec = QPushButton("🌳 GENERAR ÁRBOL"); btn_exec.setStyleSheet("background: #2d6a4f; color: white; font-weight: bold;")
        btn_exec.clicked.connect(self.ejecutar)
        
        rib_lay.addWidget(QLabel("V:")); rib_lay.addWidget(self.spin); rib_lay.addWidget(btn_crear)
        rib_lay.addWidget(btn_add); rib_lay.addStretch(); rib_lay.addWidget(btn_exec)
        layout.addWidget(ribbon)
        
        # Grafos
        grafos_lay = QHBoxLayout()
        self.vis_orig = VisualizadorGrafo("Grafo Original", ancho=400, alto=400)
        self.vis_arb = VisualizadorGrafo("Árbol Resultante", ancho=400, alto=400)
        grafos_lay.addWidget(self.vis_orig); grafos_lay.addWidget(self.vis_arb)
        layout.addLayout(grafos_lay)
        
        self.txt_res = QTextEdit(); self.txt_res.setReadOnly(True)
        layout.addWidget(self.txt_res)
        
        self.crear_grafo()

    def crear_grafo(self):
        self.num_vertices = self.spin.value()
        self.aristas = []; self.ponderaciones = {}
        self.etiquetas = {i: str(i+1) for i in range(self.num_vertices)}
        self.actualizar_vistas()

    def add_arista(self):
        dlg = DialogoArista(self.num_vertices, self, self.etiquetas)
        if dlg.exec():
            e = dlg.get_arista()
            if e not in self.aristas:
                self.aristas.append(e)
                from PySide6.QtWidgets import QInputDialog
                val, ok = QInputDialog.getDouble(self, "Peso", f"Peso para {e}:", 1)
                if ok: self.ponderaciones[e] = val
                self.actualizar_vistas()

    def actualizar_vistas(self):
        self.vis_orig.set_grafo(self.num_vertices, self.aristas, self.etiquetas, self.ponderaciones)
        self.vis_arb.set_grafo(0, [], {}, {})

    def ejecutar(self):
        # Algoritmo de Kruskal simplificado para el ejemplo
        aristas_sort = sorted(self.aristas, key=lambda x: self.ponderaciones.get(x, 1))
        parent = list(range(self.num_vertices))
        def find(i):
            if parent[i] == i: return i
            return find(parent[i])
        def union(i, j):
            root_i, root_j = find(i), find(j)
            if root_i != root_j: parent[root_i] = root_j; return True
            return False
            
        tree = []; total = 0
        for e in aristas_sort:
            if union(e[0], e[1]):
                tree.append(e); total += self.ponderaciones.get(e, 1)
        
        self.vis_arb.set_grafo(self.num_vertices, tree, self.etiquetas, self.ponderaciones)
        self.txt_res.setText(f"Árbol de Expansión Mínima\nPeso Total: {total}\nAristas: {tree}")
