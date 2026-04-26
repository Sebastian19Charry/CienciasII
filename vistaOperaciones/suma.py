import json
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QFrame)
from PySide6.QtCore import Qt
# Reutilizamos los componentes de union.py
from .union import EditorGrafoContenedor, AristaVisual, VerticeVisual
from PySide6.QtGui import QBrush, QPen, QColor, QPainter

class InterfazSuma(QWidget):
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
        self.btn_resolver = QPushButton("⚡ CALCULAR SUMA (G1 + G2)")
        self.btn_resolver.setFixedHeight(50); self.btn_resolver.setFixedWidth(280)
        self.btn_resolver.clicked.connect(self.resolver_suma)

        ribbon_lay.addStretch(1)
        ribbon_lay.addLayout(file_lay)
        ribbon_lay.addStretch(1)
        ribbon_lay.addWidget(create_sep())
        ribbon_lay.addStretch(1)
        ribbon_lay.addWidget(self.btn_resolver)
        ribbon_lay.addStretch(2)

        layout.addWidget(self.ribbon)

        # TÍTULO
        self.main_title = QLabel("OPERACIÓN: SUMA DE GRAFOS")
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
        self.g_res = EditorGrafoContenedor("RESULTADO DE LA SUMA", modo_lectura=True)
        self.g_res.hide()
        layout.addWidget(self.g_res)
        layout.setStretch(2, 1) # Dar peso al cuerpo de editores

    def resolver_suma(self):
        self.g_res.show()
        self.g_res.escena.clear()
        self.g_res.vertices = []
        self.g_res.aristas = []
        
        nodos_g1_res = []
        nodos_g2_res = []
        nodos_resultado = {} # Para mapear nombres a objetos visuales

        # 1. Crear Vértices de G1 en el resultado
        for v in self.g1.vertices:
            # Si hay nombres duplicados entre G1 y G2, les ponemos un sufijo para diferenciarlos
            # ya que en la suma se consideran conjuntos disjuntos de vértices
            nombre_final = f"{v.nombre}_g1" if any(v2.nombre == v.nombre for v2 in self.g2.vertices) else v.nombre
            
            nuevo_v = VerticeVisual(v.pos().x(), v.pos().y(), nombre_final, self.g_res, movible=True)
            self.g_res.vertices.append(nuevo_v)
            self.g_res.escena.addItem(nuevo_v)
            nodos_g1_res.append(nuevo_v)
            nodos_resultado[v.nombre + "_g1"] = nuevo_v

        # 2. Crear Vértices de G2 en el resultado
        for v in self.g2.vertices:
            nombre_final = f"{v.nombre}_g2" if any(v1.nombre == v.nombre for v1 in self.g1.vertices) else v.nombre
            
            nuevo_v = VerticeVisual(v.pos().x() + 400, v.pos().y(), nombre_final, self.g_res, movible=True)
            self.g_res.vertices.append(nuevo_v)
            self.g_res.escena.addItem(nuevo_v)
            nodos_g2_res.append(nuevo_v)
            nodos_resultado[v.nombre + "_g2"] = nuevo_v

        # 3. Recrear aristas originales de G1
        for a in self.g1.aristas:
            v1_res = next(v for v in nodos_g1_res if v.nombre.startswith(a.v1.nombre))
            v2_res = next(v for v in nodos_g1_res if v.nombre.startswith(a.v2.nombre))
            nueva_a = AristaVisual(v1_res, v2_res, a.nombre, editable=False)
            self.g_res.aristas.append(nueva_a)
            self.g_res.escena.addItem(nueva_a)

        # 4. Recrear aristas originales de G2
        for a in self.g2.aristas:
            v1_res = next(v for v in nodos_g2_res if v.nombre.startswith(a.v1.nombre))
            v2_res = next(v for v in nodos_g2_res if v.nombre.startswith(a.v2.nombre))
            nueva_a = AristaVisual(v1_res, v2_res, a.nombre, editable=False)
            self.g_res.aristas.append(nueva_a)
            self.g_res.escena.addItem(nueva_a)

        # 5. LÓGICA DE SUMA: Conectar cada vértice de G1 con cada vértice de G2
        contador_suma = 1
        for v1 in nodos_g1_res:
            for v2 in nodos_g2_res:
                nueva_a = AristaVisual(v1, v2, f"s{contador_suma}", editable=False)
                
                # CORRECCIÓN AQUÍ: Creamos un objeto QPen con el estilo deseado
                pen_estilo = QPen(QColor("gray"), 1, Qt.DashLine)
                nueva_a.setPen(pen_estilo) 
                
                self.g_res.aristas.append(nueva_a)
                self.g_res.escena.addItem(nueva_a)
                contador_suma += 1

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