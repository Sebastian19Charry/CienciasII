from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QTextEdit, QSpinBox, QComboBox, QLineEdit
)
from PySide6.QtCore import Qt
from vista.visualizador_grafo_dirigido import VisualizadorGrafoDirigido
from controlador.algoritmos.bellman_controller import BellmanController

class VistaBellman(QWidget):
    def __init__(self):
        super().__init__()
        self.num_vertices = 0; self.aristas = []; self.ponderaciones = {}
        self.etiquetas = {i: chr(65+i) for i in range(26)}
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15); main_layout.setSpacing(15)
        
        # --- Ribbon de Controles Altamente Estandarizado ---
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
        self.spin_v = QSpinBox(); self.spin_v.setRange(2, 12); self.spin_v.setValue(5); self.spin_v.setFixedWidth(50)
        btn_crear = QPushButton("↺ REINICIAR"); btn_crear.setFixedWidth(100); btn_crear.clicked.connect(self.nuevo_grafo)
        
        self.cb_orig = QComboBox(); self.cb_orig.setFixedWidth(70); self.cb_orig.setEditable(True)
        self.cb_dest = QComboBox(); self.cb_dest.setFixedWidth(70); self.cb_dest.setEditable(True)
        self.peso_edit = QLineEdit("1"); self.peso_edit.setFixedWidth(50)
        
        btn_add = QPushButton("➕ AGREGAR"); btn_add.setFixedWidth(100); btn_add.clicked.connect(self.add_arista)
        self.btn_del_sel = QPushButton("🗑️ ELIMINAR"); self.btn_del_sel.setFixedWidth(100)
        self.btn_del_sel.clicked.connect(self.eliminar_seleccionado)

        self.cb_nom = QComboBox(); self.cb_nom.setFixedWidth(60); self.cb_nom.addItems(["123", "ABC", "abc"])
        self.cb_nom.currentIndexChanged.connect(self.actualizar_nomenclatura)

        self.btn_calc = QPushButton("⚡ EJECUTAR BELLMAN-FORD"); self.btn_calc.setObjectName("btn_calc")
        self.btn_calc.setFixedWidth(220)
        self.btn_calc.clicked.connect(self.ejecutar)

        self.btn_save = QPushButton("💾 GUARDAR"); self.btn_save.setFixedWidth(100); self.btn_save.clicked.connect(self.guardar_grafo)
        self.btn_load = QPushButton("📂 RECUPERAR"); self.btn_load.setFixedWidth(100); self.btn_load.clicked.connect(self.cargar_archivo)
        
        def create_sep():
            line = QFrame(); line.setFrameShape(QFrame.VLine); line.setFrameShadow(QFrame.Plain)
            line.setStyleSheet("color: #d8e3dc; margin: 10px 0;"); return line

        # 1. Grupo Configuración
        config_lay = QVBoxLayout()
        lbl_v = QLabel("📏 Vértices"); lbl_v.setFixedWidth(70)
        lbl_n = QLabel("🔤 Nom."); lbl_n.setFixedWidth(70)
        config_top = QHBoxLayout(); config_top.addWidget(lbl_v); config_top.addWidget(self.spin_v)
        config_bot = QHBoxLayout(); config_bot.addWidget(lbl_n); config_bot.addWidget(self.cb_nom)
        config_lay.addLayout(config_top); config_lay.addLayout(config_bot)
        
        # 2. Grupo Edición
        edit_lay = QVBoxLayout()
        edit_top = QHBoxLayout()
        lbl_de = QLabel("📍 De"); lbl_de.setFixedWidth(40)
        lbl_a = QLabel("➜ A"); lbl_a.setFixedWidth(40)
        lbl_p = QLabel("⚖️ Peso"); lbl_p.setFixedWidth(50)
        edit_top.addWidget(lbl_de); edit_top.addWidget(self.cb_orig)
        edit_top.addWidget(lbl_a); edit_top.addWidget(self.cb_dest)
        edit_top.addWidget(lbl_p); edit_top.addWidget(self.peso_edit)
        edit_bot = QHBoxLayout(); edit_bot.addWidget(btn_crear); edit_bot.addWidget(btn_add); edit_bot.addWidget(self.btn_del_sel)
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
        
        body = QHBoxLayout()
        viz_wrap = QFrame()
        viz_wrap.setStyleSheet("background: white; border: 1px solid #d8e3dc; border-radius: 10px;")
        viz_lay = QVBoxLayout(viz_wrap)
        lbl_viz_title = QLabel("🗺️ MAPA DEL GRAFO (ORIGINAL)")
        lbl_viz_title.setStyleSheet("color: #1b4332; font-weight: bold; font-size: 14px; padding: 5px;")
        viz_lay.addWidget(lbl_viz_title)
        self.grafo_original = VisualizadorGrafoDirigido("Bellman", ancho=600, alto=600)
        self.grafo_original.solicitud_eliminacion.connect(self.eliminar_seleccionado)
        viz_lay.addWidget(self.grafo_original, stretch=1)
        body.addWidget(viz_wrap, stretch=2)
        
        # Necesario para el controlador original de Bellman
        self.grafo_enumerado = VisualizadorGrafoDirigido("Enumerado", ancho=1, alto=1)
        self.grafo_enumerado.hide()
        
        res_wrap = QFrame()
        res_wrap.setStyleSheet("background: white; border: 1px solid #d8e3dc; border-radius: 10px;")
        res_lay = QVBoxLayout(res_wrap)
        lbl_res = QLabel("📋 TABLA DE DISTANCIAS")
        lbl_res.setStyleSheet("color: #1b4332; font-weight: bold; padding: 5px; border-bottom: 1px solid #f0f7f4;")
        res_lay.addWidget(lbl_res)
        self.txt_res = QTextEdit(); self.txt_res.setReadOnly(True)
        self.txt_res.setStyleSheet("border: none; color: #1b4332; font-family: 'Consolas'; font-size: 11px;")
        res_lay.addWidget(self.txt_res)
        body.addWidget(res_wrap, stretch=1)
        
        main_layout.addLayout(body)
        self.controller = BellmanController(self)
        self.nuevo_grafo()

    def nuevo_grafo(self):
        n = self.spin_v.value(); self.num_vertices = n; self.aristas = []; self.ponderaciones = {}
        self.actualizar_nomenclatura()

    def actualizar_nomenclatura(self):
        modo = self.cb_nom.currentText()
        self.etiquetas = {}
        for i in range(self.num_vertices):
            if modo == "ABC":
                label, t = "", i
                while t >= 0: label = chr(65 + (t % 26)) + label; t = (t // 26) - 1
                self.etiquetas[i] = label
            elif modo == "abc":
                label, t = "", i
                while t >= 0: label = chr(97 + (t % 26)) + label; t = (t // 26) - 1
                self.etiquetas[i] = label
            else: self.etiquetas[i] = str(i + 1)
        
        self.cb_orig.clear(); self.cb_dest.clear()
        labs = [self.etiquetas[i] for i in range(self.num_vertices)]
        self.cb_orig.addItems(labs); self.cb_dest.addItems(labs)
        self.actualizar_vista()

    def add_arista(self):
        u, v = self.cb_orig.currentIndex(), self.cb_dest.currentIndex()
        try:
            w = float(self.peso_edit.text().replace(',', '.'))
        except ValueError:
            w = 1
        if (u, v) not in self.aristas: self.aristas.append((u, v))
        self.ponderaciones[(u, v)] = str(w); self.actualizar_vista()

    def eliminar_seleccionado(self):
        sel = self.grafo_original.objeto_seleccionado
        if not sel: return
        tipo, idx = sel
        if tipo == 'vertice':
            if self.num_vertices > 2:
                self.spin_v.setValue(self.num_vertices - 1)
                self.nuevo_grafo()
        elif tipo == 'arista':
            if 0 <= idx < len(self.aristas):
                a = self.aristas.pop(idx)
                self.ponderaciones.pop(a, None)
                self.grafo_original.objeto_seleccionado = None
                self.actualizar_vista()

    def ejecutar(self):
        if not self.aristas:
            self.txt_res.setText("Agrega al menos una arista para ejecutar Bellman-Ford.")
            return
        res = self.controller.ejecutar_bellman()
        texto = "<html><body style='color:#1b4332;'><b>--- ITERACIONES ---</b><br><br>"
        for it in res['iteraciones']:
            dists = ", ".join([f"{k}:{v}" for k, v in it['distancias'].items()])
            texto += f"<b>Iteración {it['iteracion']}:</b><br>{dists}<br>"
            if it['cambios']: texto += f"<i style='color:green;'>Cambios: {it['cambios']}</i><br>"
            texto += "<hr>"
        texto += "</body></html>"; self.txt_res.setHtml(texto)

    def guardar_grafo(self):
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        import json
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Grafo", "", "JSON Files (*.json)")
        if archivo:
            datos = {
                'vertices': self.num_vertices,
                'aristas': self.aristas,
                'ponderaciones': {str(k): v for k, v in self.ponderaciones.items()},
                'nom': self.cb_nom.currentIndex()
            }
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4)
            QMessageBox.information(self, "Éxito", "Grafo guardado correctamente.")

    def cargar_archivo(self):
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        import json
        archivo, _ = QFileDialog.getOpenFileName(self, "Cargar Grafo", "", "JSON Files (*.json)")
        if archivo:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            self.num_vertices = datos['vertices']
            self.aristas = [tuple(a) for a in datos['aristas']]
            self.ponderaciones = {}
            for k, v in datos.get('ponderaciones', {}).items():
                try:
                    arista_tuple = tuple(map(int, k.strip('()').split(', ')))
                    self.ponderaciones[arista_tuple] = v
                except: pass
            self.spin_v.setValue(self.num_vertices)
            self.cb_nom.setCurrentIndex(datos.get('nom', 0))
            self.actualizar_vista()
            QMessageBox.information(self, "Éxito", "Grafo cargado correctamente.")

    def actualizar_vista(self):
        weights = [str(self.ponderaciones.get(a, "1")) for a in self.aristas]
        # Sincronizar con el controlador
        self.controller.cargar_grafo(self.num_vertices, self.aristas, self.etiquetas, weights)

    def actualizar_combos_aristas(self):
        # El controlador espera este método. No hace nada aquí porque los combos se manejan en nuevo_grafo
        pass
