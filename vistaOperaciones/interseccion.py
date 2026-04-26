import json
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QFrame)
from PySide6.QtCore import Qt
# Reutilizamos las clases que ya definimos en union.py (asumiendo que están en el mismo nivel)
from .union import EditorGrafoContenedor, AristaVisual, VerticeVisual

class InterfazInterseccion(QWidget):
    def __init__(self, main_window):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # --- Ribbon de Operaciones ---
        self.ribbon = QFrame()
        self.ribbon.setFixedHeight(105)
        self.ribbon.setStyleSheet("""
            QFrame { background-color: #f8faf9; border: 1px solid #d8e3dc; border-radius: 12px; }
            QLabel { color: #1b4332; font-weight: bold; font-size: 10px; text-transform: uppercase; }
            QPushButton { 
                background-color: #2d6a4f; color: white; border-radius: 8px; 
                font-weight: bold; font-size: 12px; padding: 8px;
            }
            QPushButton:hover { background-color: #1b4332; }
            QComboBox, QLineEdit { 
                background: white; color: #1b4332; border: 2px solid #e0e6e3; 
                border-radius: 6px; padding: 4px; font-weight: bold;
            }
            QComboBox QAbstractItemView {
                background-color: white; color: black;
                selection-background-color: #2d6a4f; selection-color: white;
            }
        """)
        ribbon_lay = QHBoxLayout(self.ribbon)
        ribbon_lay.setContentsMargins(30, 0, 30, 0); ribbon_lay.setSpacing(20)

        def create_sep():
            line = QFrame(); line.setFrameShape(QFrame.VLine); line.setFrameShadow(QFrame.Plain)
            line.setStyleSheet("color: #d8e3dc; margin: 10px 0;"); return line

        # Grupo Archivos
        file_lay = QVBoxLayout()
        btn_g_save = QPushButton("💾 GUARDAR PROYECTO")
        btn_g_load = QPushButton("📂 RECUPERAR PROYECTO")
        btn_g_save.clicked.connect(self.guardar_todo)
        btn_g_load.clicked.connect(self.cargar_todo)
        file_lay.addWidget(btn_g_save); file_lay.addWidget(btn_g_load)

        # Grupo Acciones
        self.btn_resolver = QPushButton("⚡ CALCULAR INTERSECCIÓN (G1 ∩ G2)")
        self.btn_resolver.setFixedHeight(50); self.btn_resolver.setFixedWidth(280)
        self.btn_resolver.clicked.connect(self.resolver_interseccion)

        ribbon_lay.addStretch(1)
        ribbon_lay.addLayout(file_lay)
        ribbon_lay.addStretch(1)
        ribbon_lay.addWidget(create_sep())
        ribbon_lay.addStretch(1)
        ribbon_lay.addWidget(self.btn_resolver)
        ribbon_lay.addStretch(2)

        layout.addWidget(self.ribbon)

        # TÍTULO
        self.main_title = QLabel("OPERACIÓN: INTERSECCIÓN DE GRAFOS")
        self.main_title.setStyleSheet("""
            color: #1b4332; font-size: 24px; font-weight: bold; 
            margin: 10px; text-transform: uppercase; letter-spacing: 1px;
        """)
        self.main_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.main_title)

        # CUERPO (Side by Side)
        self.cuerpo_editores = QHBoxLayout()
        self.cuerpo_editores.setSpacing(20)
        self.cuerpo_editores.setContentsMargins(15, 0, 15, 15)
        
        self.g1 = EditorGrafoContenedor("GRAFO G1")
        self.g2 = EditorGrafoContenedor("GRAFO G2")
        self.cuerpo_editores.addWidget(self.g1)
        self.cuerpo_editores.addWidget(self.g2)
        
        layout.addLayout(self.cuerpo_editores)

        # RESULTADO (Oculto inicialmente)
        self.g_res = EditorGrafoContenedor("RESULTADO DE LA INTERSECCIÓN", modo_lectura=True)
        self.g_res.hide()
        layout.addWidget(self.g_res)
        layout.setStretch(2, 1) # Dar peso al cuerpo de editores

    def resolver_interseccion(self):
        self.g_res.show()
        self.g_res.escena.clear()
        self.g_res.vertices = []
        self.g_res.aristas = []
        
        nodos_resultado = {}
        
        # LÓGICA DE INTERSECCIÓN:
        # 1. Vértices: Solo los que tienen el mismo nombre en G1 Y en G2
        nombres_g1 = {v.nombre for v in self.g1.vertices}
        nombres_g2 = {v.nombre for v in self.g2.vertices}
        comunes_v = nombres_g1.intersection(nombres_g2)

        for nombre in comunes_v:
            # Buscamos la posición original en G1 (por ejemplo)
            v_orig = next(v for v in self.g1.vertices if v.nombre == nombre)
            nuevo_v = VerticeVisual(v_orig.pos().x(), v_orig.pos().y(), nombre, self.g_res, movible=True)
            self.g_res.vertices.append(nuevo_v)
            self.g_res.escena.addItem(nuevo_v)
            nodos_resultado[nombre] = nuevo_v

        # 2. Aristas: Solo si la arista existe en ambos y conecta los mismos nombres
        def get_dict_aristas(grafo):
            # Clave: (nombre_arista, (v1, v2) ordenados)
            return {(a.nombre, tuple(sorted((a.v1.nombre, a.v2.nombre)))): a for a in grafo.aristas}

        aristas_g1 = get_dict_aristas(self.g1)
        aristas_g2 = get_dict_aristas(self.g2)
        
        claves_comunes = set(aristas_g1.keys()).intersection(set(aristas_g2.keys()))

        for clave in claves_comunes:
            nombre_a, (n1, n2) = clave
            # Solo la agregamos si los vértices que conecta sobrevivieron a la intersección
            if n1 in nodos_resultado and n2 in nodos_resultado:
                nueva_a = AristaVisual(nodos_resultado[n1], nodos_resultado[n2], nombre_a, editable=False)
                self.g_res.aristas.append(nueva_a)
                self.g_res.escena.addItem(nueva_a)

        self.g_res.actualizar_aristas()


    def guardar_todo(self):
        path, _ = QFileDialog.getSaveFileName(self, "Guardar Proyecto", "", "JSON Files (*.json)")
        if path:
            def serializar(grafo):
                return {
                    "v": [{"n": v.nombre, "x": v.pos().x(), "y": v.pos().y()} for v in grafo.vertices],
                    "a": [{"n": a.nombre, "v1": a.v1.nombre, "v2": a.v2.nombre} for a in grafo.aristas]
                }
            data = {"g1": serializar(self.g1), "g2": serializar(self.g2)}
            with open(path, 'w') as f:
                json.dump(data, f, indent=4)

    def cargar_todo(self):
        path, _ = QFileDialog.getOpenFileName(self, "Cargar Proyecto", "", "JSON Files (*.json)")
        if path:
            with open(path, 'r') as f:
                data = json.load(f)
            
            for key, grafo_obj in [("g1", self.g1), ("g2", self.g2)]:
                grafo_obj.escena.clear()
                grafo_obj.vertices = []
                grafo_obj.aristas = []
                # Cargar Vértices
                for v in data[key]["v"]:
                    grafo_obj.agregar_vertice_objetivo(v["x"], v["y"], v["n"])
                # Cargar Aristas
                for a in data[key]["a"]:
                    v1 = next((v for v in grafo_obj.vertices if v.nombre == a["v1"]), None)
                    v2 = next((v for v in grafo_obj.vertices if v.nombre == a["v2"]), None)
                    if v1 and v2:
                        nueva = AristaVisual(v1, v2, a["n"])
                        grafo_obj.aristas.append(nueva)
                        grafo_obj.escena.addItem(nueva)
            self.g_res.hide()