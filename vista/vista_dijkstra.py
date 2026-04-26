from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QTextEdit, QSpinBox, QMessageBox, QFileDialog,
    QComboBox, QLineEdit
)
from PySide6.QtCore import Qt
from vista.visualizador_grafo_dirigido import VisualizadorGrafoDirigido
from controlador.algoritmos.dijkstra_controller import DijkstraController

class ModeloGrafoInterno:
    def __init__(self):
        self.num_vertices = 0; self.aristas = []
        self.etiquetas = {}; self.ponderaciones_lista = []

    def crear_grafo(self, num_vertices):
        self.num_vertices = num_vertices; self.aristas = []; self.ponderaciones_lista = []

    def agregar_arista(self, origen, destino, peso):
        if origen < 0 or origen >= self.num_vertices or destino < 0 or destino >= self.num_vertices: return False
        arista = (origen, destino)
        if arista not in self.aristas:
            self.aristas.append(arista); self.ponderaciones_lista.append(str(peso))
        else:
            idx = self.aristas.index(arista); self.ponderaciones_lista[idx] = str(peso)
        return True

    def obtener_num_vertices(self):
        return self.num_vertices

    def obtener_aristas(self):
        return self.aristas

    def obtener_ponderaciones_como_lista(self):
        return self.ponderaciones_lista

class VistaDijkstra(QWidget):
    def __init__(self):
        super().__init__()
        self.model = ModeloGrafoInterno(); self.controller = DijkstraController(self.model)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15); main_layout.setSpacing(15)
        
        # --- Ribbon Altamente Estandarizado (Anchos Fijos para evitar saltos de pixeles) ---
        self.ribbon = QFrame()
        self.ribbon.setFixedHeight(100)
        self.ribbon.setStyleSheet("""
            QFrame#ribbon { background-color: #f8faf9; border: 1px solid #d8e3dc; border-radius: 12px; }
            QLabel { color: #1b4332; font-weight: bold; font-size: 10px; text-transform: uppercase; }
            QSpinBox, QComboBox, QLineEdit {
                background-color: white; color: #1b4332;
                border: 2px solid #e0e6e3; border-radius: 6px;
                padding: 4px; font-weight: bold; font-size: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                selection-background-color: #2d6a4f;
                selection-color: white;
            }
            QSpinBox:focus, QComboBox:focus, QLineEdit:focus { border-color: #2d6a4f; }
            QPushButton {
                background-color: #2d6a4f; color: white; font-weight: bold;
                border: none; border-radius: 8px; padding: 8px 15px; font-size: 11px;
            }
            QPushButton:hover { background-color: #1b4332; }
            QPushButton#btn_calc { 
                background-color: #1b4332; font-size: 13px; border-radius: 10px;
                padding: 10px 25px;
            }
            QPushButton#btn_calc:hover { background-color: #081c15; }
        """)
        self.ribbon.setObjectName("ribbon")
        
        ribbon_layout = QHBoxLayout(self.ribbon)
        ribbon_layout.setContentsMargins(30, 0, 30, 0); ribbon_layout.setSpacing(20)
        
        # --- Definición de Widgets ---
        self.spin_vertices = QSpinBox(); self.spin_vertices.setRange(2, 20); self.spin_vertices.setValue(6); self.spin_vertices.setFixedWidth(50)
        self.btn_crear = QPushButton("↺ REINICIAR"); self.btn_crear.setFixedWidth(100)
        self.btn_crear.clicked.connect(self.crear_grafo)
        self.cb_nom = QComboBox(); self.cb_nom.setFixedWidth(60); self.cb_nom.addItems(["123", "ABC", "abc"])
        self.cb_nom.currentIndexChanged.connect(self.actualizar_nomenclatura)
        
        self.cb_origen = QComboBox(); self.cb_origen.setFixedWidth(70); self.cb_origen.setEditable(True)
        self.cb_destino = QComboBox(); self.cb_destino.setFixedWidth(70); self.cb_destino.setEditable(True)
        self.peso_edit = QLineEdit("1"); self.peso_edit.setFixedWidth(50)
        
        self.btn_add = QPushButton("➕ AGREGAR"); self.btn_add.setFixedWidth(100)
        self.btn_add.clicked.connect(self.agregar_arista)
        self.btn_del_sel = QPushButton("🗑️ ELIMINAR"); self.btn_del_sel.setFixedWidth(100)
        self.btn_del_sel.clicked.connect(self.eliminar_seleccionado)

        self.btn_calc = QPushButton("⚡ EJECUTAR DIJKSTRA"); self.btn_calc.setObjectName("btn_calc")
        self.btn_calc.setFixedWidth(220)
        self.btn_calc.clicked.connect(self.ejecutar_dijkstra)

        self.btn_save = QPushButton("💾 GUARDAR"); self.btn_save.setFixedWidth(100); self.btn_save.clicked.connect(self.guardar_grafo)
        self.btn_load = QPushButton("📂 RECUPERAR"); self.btn_load.setFixedWidth(100); self.btn_load.clicked.connect(self.cargar_grafo)
        
        def create_sep():
            line = QFrame(); line.setFrameShape(QFrame.VLine); line.setFrameShadow(QFrame.Plain)
            line.setStyleSheet("color: #d8e3dc; margin: 10px 0;"); return line

        # 1. Grupo Configuración
        config_lay = QVBoxLayout()
        lbl_v = QLabel("📏 Vértices"); lbl_v.setFixedWidth(70)
        lbl_n = QLabel("🔤 Nom."); lbl_n.setFixedWidth(70)
        config_top = QHBoxLayout(); config_top.addWidget(lbl_v); config_top.addWidget(self.spin_vertices)
        config_bot = QHBoxLayout(); config_bot.addWidget(lbl_n); config_bot.addWidget(self.cb_nom)
        config_lay.addLayout(config_top); config_lay.addLayout(config_bot)
        
        # 2. Grupo Edición
        edit_lay = QVBoxLayout()
        edit_top = QHBoxLayout()
        lbl_de = QLabel("📍 De"); lbl_de.setFixedWidth(40)
        lbl_a = QLabel("➜ A"); lbl_a.setFixedWidth(40)
        lbl_p = QLabel("⚖️ Peso"); lbl_p.setFixedWidth(50)
        edit_top.addWidget(lbl_de); edit_top.addWidget(self.cb_origen)
        edit_top.addWidget(lbl_a); edit_top.addWidget(self.cb_destino)
        edit_top.addWidget(lbl_p); edit_top.addWidget(self.peso_edit)
        edit_bot = QHBoxLayout(); edit_bot.addWidget(self.btn_crear); edit_bot.addWidget(self.btn_add); edit_bot.addWidget(self.btn_del_sel)
        edit_lay.addLayout(edit_top); edit_lay.addLayout(edit_bot)

        # 3. Grupo Archivos
        file_lay = QVBoxLayout()
        file_lay.addWidget(self.btn_save); file_lay.addWidget(self.btn_load)

        ribbon_layout.addStretch(1)
        ribbon_layout.addLayout(config_lay)
        ribbon_layout.addStretch(1)
        ribbon_layout.addWidget(create_sep())
        ribbon_layout.addStretch(1)
        ribbon_layout.addLayout(edit_lay)
        ribbon_layout.addStretch(1)
        ribbon_layout.addWidget(create_sep())
        ribbon_layout.addStretch(1)
        ribbon_layout.addLayout(file_lay)
        ribbon_layout.addStretch(2)
        ribbon_layout.addWidget(self.btn_calc)
        ribbon_layout.addStretch(1)
        
        main_layout.addWidget(self.ribbon)
        
        # --- Cuerpo ---
        body = QHBoxLayout()
        
        viz_wrap = QFrame()
        viz_wrap.setStyleSheet("background: white; border: 1px solid #d8e3dc; border-radius: 10px;")
        viz_lay = QVBoxLayout(viz_wrap)
        lbl_viz_title = QLabel("🗺️ MAPA DEL GRAFO / RED DE CAMINOS")
        lbl_viz_title.setStyleSheet("color: #1b4332; font-weight: bold; font-size: 14px; padding: 5px;")
        viz_lay.addWidget(lbl_viz_title)
        self.visualizador = VisualizadorGrafoDirigido("Dijkstra", ancho=600, alto=600)
        self.visualizador.solicitud_eliminacion.connect(self.eliminar_seleccionado)
        viz_lay.addWidget(self.visualizador, stretch=1)
        body.addWidget(viz_wrap, stretch=2) # Ajustado de 3 a 2 para balancear con resultados
        
        res_wrap = QFrame()
        res_wrap.setStyleSheet("background: white; border: 1px solid #d8e3dc; border-radius: 10px;")
        res_lay = QVBoxLayout(res_wrap)
        lbl_res = QLabel("📋 PROCESO Y RESULTADOS")
        lbl_res.setStyleSheet("color: #1b4332; font-weight: bold; padding: 5px; border-bottom: 1px solid #f0f7f4;")
        res_lay.addWidget(lbl_res)
        self.texto_proceso = QTextEdit(); self.texto_proceso.setReadOnly(True)
        self.texto_proceso.setStyleSheet("border: none; color: #1b4332; font-family: 'Consolas'; font-size: 11px;")
        res_lay.addWidget(self.texto_proceso)
        body.addWidget(res_wrap, stretch=1)
        
        main_layout.addLayout(body)
        
        self.btn_crear.clicked.connect(self.crear_grafo)
        self.btn_add.clicked.connect(self.agregar_arista)
        self.btn_calc.clicked.connect(self.ejecutar_dijkstra)
        self.crear_grafo()

    def crear_grafo(self):
        n = self.spin_vertices.value(); self.model.crear_grafo(n)
        self.actualizar_nomenclatura()

    def actualizar_nomenclatura(self):
        modo = self.cb_nom.currentText()
        self.model.etiquetas = {}
        for i in range(self.model.num_vertices):
            if modo == "ABC":
                label, t = "", i
                while t >= 0: label = chr(65 + (t % 26)) + label; t = (t // 26) - 1
                self.model.etiquetas[i] = label
            elif modo == "abc":
                label, t = "", i
                while t >= 0: label = chr(97 + (t % 26)) + label; t = (t // 26) - 1
                self.model.etiquetas[i] = label
            else: self.model.etiquetas[i] = str(i + 1)
        
        self.cb_origen.clear(); self.cb_destino.clear()
        labs = [self.model.etiquetas[i] for i in range(self.model.num_vertices)]
        self.cb_origen.addItems(labs); self.cb_destino.addItems(labs)
        self.actualizar_vista()

    def agregar_arista(self):
        u = self.cb_origen.currentIndex()
        v = self.cb_destino.currentIndex()
        try:
            w = float(self.peso_edit.text().replace(',', '.'))
        except ValueError:
            w = 1
        if self.model.agregar_arista(u, v, w): self.actualizar_vista()

    def eliminar_seleccionado(self):
        sel = self.visualizador.objeto_seleccionado
        if not sel: return
        tipo, idx = sel
        if tipo == 'vertice':
            # Para Dijkstra, si eliminamos un vértice usualmente es el último o reducimos el conteo
            if self.model.num_vertices > 2:
                n = self.model.num_vertices - 1
                self.spin_vertices.setValue(n)
                self.crear_grafo()
        elif tipo == 'arista':
            if 0 <= idx < len(self.model.aristas):
                self.model.aristas.pop(idx)
                self.model.ponderaciones_lista.pop(idx)
                self.visualizador.objeto_seleccionado = None
                self.actualizar_vista()

    def ejecutar_dijkstra(self):
        origen = self.cb_origen.currentIndex()
        res = self.controller.ejecutar_dijkstra(origen)
        if res[0] is not None:
            self.texto_proceso.setHtml(f"<b style='color:#2d6a4f;'>Iniciando Dijkstra desde el nodo {chr(65+origen)}:</b><br><br>" + 
                                      "<br>".join(res[3]).replace("\n", "<br>"))

    def guardar_grafo(self):
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Grafo", "", "JSON Files (*.json)")
        if archivo:
            import json
            datos = {
                'vertices': self.model.num_vertices,
                'aristas': self.model.aristas,
                'etiquetas': self.model.etiquetas,
                'ponderaciones': self.model.ponderaciones_lista,
                'nom': self.cb_nom.currentIndex()
            }
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4)
            QMessageBox.information(self, "Éxito", "Grafo guardado correctamente.")

    def cargar_grafo(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Cargar Grafo", "", "JSON Files (*.json)")
        if archivo:
            import json
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            self.model.num_vertices = datos['vertices']
            self.model.aristas = [tuple(a) for a in datos['aristas']]
            self.model.etiquetas = {int(k): v for k, v in datos.get('etiquetas', {}).items()}
            self.model.ponderaciones_lista = datos.get('ponderaciones', [])
            self.spin_vertices.setValue(self.model.num_vertices)
            self.cb_nom.setCurrentIndex(datos.get('nom', 0))
            self.actualizar_vista()
            QMessageBox.information(self, "Éxito", "Grafo cargado correctamente.")

    def actualizar_vista(self):
        self.visualizador.set_grafo(self.model.num_vertices, self.model.aristas, self.model.etiquetas, self.model.ponderaciones_lista)
