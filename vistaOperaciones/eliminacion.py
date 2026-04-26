import json
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QLineEdit, QMessageBox, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QPen
# Reutilizamos los componentes de union.py
from .union import EditorGrafoContenedor, AristaVisual, VerticeVisual

class InterfazEliminacionVertices(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
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
            QLineEdit, QComboBox { 
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
        btn_g_save = QPushButton("💾 GUARDAR GRAFO")
        btn_g_load = QPushButton("📂 RECUPERAR GRAFO")
        btn_g_save.clicked.connect(self.guardar_todo)
        btn_g_load.clicked.connect(self.cargar_todo)
        file_lay.addWidget(btn_g_save); file_lay.addWidget(btn_g_load)

        # Grupo Eliminación
        del_lay = QVBoxLayout()
        self.input_borrar = QLineEdit(); self.input_borrar.setPlaceholderText("Nombre del vértice")
        self.input_borrar.setFixedWidth(180); self.input_borrar.setFixedHeight(30)
        self.btn_resolver = QPushButton("⚡ ELIMINAR VÉRTICE")
        self.btn_resolver.setFixedHeight(32); self.btn_resolver.clicked.connect(self.resolver_eliminacion)
        del_lay.addWidget(self.input_borrar); del_lay.addWidget(self.btn_resolver)

        ribbon_lay.addStretch(1)
        ribbon_lay.addLayout(file_lay)
        ribbon_lay.addStretch(1)
        ribbon_lay.addWidget(create_sep())
        ribbon_lay.addStretch(1)
        ribbon_lay.addLayout(del_lay)
        ribbon_lay.addStretch(2)

        layout.addWidget(self.ribbon)

        # TÍTULO
        self.main_title = QLabel("OPERACIÓN: ELIMINACIÓN DE VÉRTICES")
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
        
        self.g1 = EditorGrafoContenedor("GRAFO ORIGINAL")
        self.g_res = EditorGrafoContenedor("RESULTADO (Vértice eliminado)", modo_lectura=True)
        
        self.cuerpo_editores.addWidget(self.g1)
        self.cuerpo_editores.addWidget(self.g_res)
        layout.addLayout(self.cuerpo_editores)
        layout.setStretch(2, 1)

    def resolver_eliminacion(self):
        target = self.input_borrar.text().strip()

        # Validación
        v_target = next((v for v in self.g1.vertices if v.nombre == target), None)

        if not v_target:
            QMessageBox.warning(self, "Error", f"El vértice '{target}' no existe.")
            return

        # Limpiar resultado
        self.g_res.escena.clear()
        self.g_res.vertices = []
        self.g_res.aristas = []
        self.g_res.show()

        nodos_mapeo = {}

        # 1. Copiar todos los vértices EXCEPTO el eliminado
        for v in self.g1.vertices:
            if v.nombre != target:
                nuevo_v = VerticeVisual(v.pos().x(), v.pos().y(), v.nombre, self.g_res, movible=True)
                self.g_res.vertices.append(nuevo_v)
                self.g_res.escena.addItem(nuevo_v)
                nodos_mapeo[v.nombre] = nuevo_v

        # 2. Copiar solo las aristas que NO tocaban al vértice eliminado
        for a in self.g1.aristas:
            # Una arista sobrevive solo si sus DOS extremos NO son el vértice borrado
            if a.v1.nombre != target and a.v2.nombre != target:
                v1_res = nodos_mapeo[a.v1.nombre]
                v2_res = nodos_mapeo[a.v2.nombre]
                
                nueva_a = AristaVisual(v1_res, v2_res, a.nombre, editable=False)
                self.g_res.aristas.append(nueva_a)
                self.g_res.escena.addItem(nueva_a)

        self.g_res.actualizar_aristas()

    def guardar_todo(self):
        path, _ = QFileDialog.getSaveFileName(self, "Guardar Grafo", "", "JSON Files (*.json)")
        if path:
            data = {"g1": {
                "v": [{"n": v.nombre, "x": v.pos().x(), "y": v.pos().y()} for v in self.g1.vertices],
                "a": [{"n": a.nombre, "v1": a.v1.nombre, "v2": a.v2.nombre} for a in self.g1.aristas]
            }}
            with open(path, 'w') as f: json.dump(data, f, indent=4)

    def cargar_todo(self):
        path, _ = QFileDialog.getOpenFileName(self, "Cargar Grafo", "", "JSON Files (*.json)")
        if path:
            with open(path, 'r') as f: data = json.load(f)
            self.g1.escena.clear(); self.g1.vertices = []; self.g1.aristas = []
            for v in data["g1"]["v"]: self.g1.agregar_vertice_objetivo(v["x"], v["y"], v["n"])
            for a in data["g1"]["a"]:
                v1 = next((v for v in self.g1.vertices if v.nombre == a["v1"]), None)
                v2 = next((v for v in self.g1.vertices if v.nombre == a["v2"]), None)
                if v1 and v2:
                    nueva = AristaVisual(v1, v2, a["n"])
                    self.g1.aristas.append(nueva); self.g1.escena.addItem(nueva)