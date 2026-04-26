"""
vista_arbol_central.py
Vista para el Árbol Central.
Usa CentralController para toda la lógica algorítmica.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSpinBox, QTextEdit, QTabWidget, QComboBox
)
from PySide6.QtCore import Qt
from vista.visualizador_grafo_no_dirigido import VisualizadorGrafoNoDirigido
from controlador.arboles.centralController import CentralController


class VistaArbolCentral(QWidget):

    def __init__(self, main_window, hub):
        super().__init__()
        self.main_window = main_window
        self.hub = hub

        # Estado local (expuesto para compatibilidad con ctrl.set_grafo)
        self.num_vertices = 0
        self.aristas      = []
        self.etiquetas    = {}

        self.ctrl = CentralController()

        self._build_ui()
        self.nuevo_grafo()

    # ── UI ───────────────────────────────────────────────────────────────────
    def _build_ui(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(15, 12, 15, 12)
        main.setSpacing(10)

        ribbon = QFrame()
        ribbon.setFixedHeight(105)
        ribbon.setStyleSheet("""
            QFrame#ribbon { background-color: #f8faf9; border: 1px solid #d8e3dc; border-radius: 12px; }
            QLabel { color: #1b4332; font-weight: bold; font-size: 10px; text-transform: uppercase; }
            QSpinBox, QComboBox {
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
            QSpinBox:focus, QComboBox:focus { border-color: #2d6a4f; }
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
        ribbon.setObjectName("ribbon")
        r = QHBoxLayout(ribbon)
        r.setContentsMargins(30, 0, 30, 0); r.setSpacing(20)

        # --- Definición de Widgets ---
        btn_back = QPushButton("⬅ VOLVER")
        btn_back.setFixedWidth(80); btn_back.clicked.connect(lambda: self.main_window.cambiar_pantalla(self.hub))
        
        self.spin_v = QSpinBox(); self.spin_v.setRange(2, 15); self.spin_v.setValue(6); self.spin_v.setFixedWidth(50)
        btn_crear = QPushButton("↺ REINICIAR"); btn_crear.setFixedWidth(100); btn_crear.clicked.connect(self.nuevo_grafo)
        
        self.cb_nom = QComboBox(); self.cb_nom.setFixedWidth(60); self.cb_nom.addItems(["123", "ABC", "abc"])
        self.cb_nom.currentIndexChanged.connect(self.actualizar_nomenclatura)
        
        self.cb_orig = QComboBox(); self.cb_orig.setFixedWidth(70); self.cb_orig.setEditable(True)
        self.cb_dest = QComboBox(); self.cb_dest.setFixedWidth(70); self.cb_dest.setEditable(True)
        
        btn_add = QPushButton("➕ AGREGAR"); btn_add.setFixedWidth(100); btn_add.clicked.connect(self.add_arista)
        self.btn_del_sel = QPushButton("🗑️ ELIMINAR"); self.btn_del_sel.setFixedWidth(100)
        self.btn_del_sel.clicked.connect(self.eliminar_seleccionado)

        btn_calc = QPushButton("⚡ CALCULAR CENTRO"); btn_calc.setObjectName("btn_calc")
        btn_calc.clicked.connect(self.ejecutar)

        btn_save = QPushButton("💾 GUARDAR"); btn_save.setFixedWidth(100); btn_save.clicked.connect(self.guardar_grafo)
        self.btn_load = QPushButton("📂 RECUPERAR"); self.btn_load.setFixedWidth(100); self.btn_load.clicked.connect(self.recuperar_arbol)

        # --- Grupos ---
        def create_sep():
            line = QFrame(); line.setFrameShape(QFrame.VLine); line.setFrameShadow(QFrame.Plain)
            line.setStyleSheet("color: #d8e3dc; margin: 10px 0;"); return line

        # 1. Grupo Nav/Config
        nav_lay = QVBoxLayout()
        nav_lay.addWidget(btn_back)
        lbl_nom = QLabel("🔤 Nom."); lbl_nom.setFixedWidth(60)
        config_row = QHBoxLayout(); config_row.addWidget(lbl_nom); config_row.addWidget(self.cb_nom)
        nav_lay.addLayout(config_row)

        # 2. Grupo Grafo
        grafo_lay = QVBoxLayout()
        lbl_ver = QLabel("📏 Vértices"); lbl_ver.setFixedWidth(70)
        v_row = QHBoxLayout(); v_row.addWidget(lbl_ver); v_row.addWidget(self.spin_v)
        grafo_lay.addLayout(v_row); grafo_lay.addWidget(btn_crear)

        # 3. Grupo Edición
        edit_lay = QVBoxLayout()
        edit_top = QHBoxLayout()
        lbl_de = QLabel("📍 De"); lbl_de.setFixedWidth(40)
        lbl_a = QLabel("➜ A"); lbl_a.setFixedWidth(40)
        edit_top.addWidget(lbl_de); edit_top.addWidget(self.cb_orig)
        edit_top.addWidget(lbl_a); edit_top.addWidget(self.cb_dest)
        edit_bot = QHBoxLayout(); edit_bot.addWidget(btn_add); edit_bot.addWidget(self.btn_del_sel)
        edit_lay.addLayout(edit_top); edit_lay.addLayout(edit_bot)

        # 4. Grupo Archivos
        file_lay = QVBoxLayout()
        file_lay.addWidget(btn_save); file_lay.addWidget(self.btn_load)

        r.addStretch(1)
        r.addLayout(nav_lay)
        r.addStretch(1)
        r.addWidget(create_sep())
        r.addStretch(1)
        r.addLayout(grafo_lay)
        r.addStretch(1)
        r.addWidget(create_sep())
        r.addStretch(1)
        r.addLayout(edit_lay)
        r.addStretch(1)
        r.addWidget(create_sep())
        r.addStretch(1)
        r.addLayout(file_lay)
        r.addStretch(2)
        r.addWidget(btn_calc)
        r.addStretch(1)

        main.addWidget(ribbon)

        # Body
        body = QHBoxLayout(); body.setSpacing(10)

        # Panel visualizador
        viz_frame = QFrame()
        viz_frame.setStyleSheet("background:white; border:1px solid #d8e3dc; border-radius:10px;")
        vl = QVBoxLayout(viz_frame); vl.setContentsMargins(10, 10, 10, 10)
        lbl = QLabel("🗺️  ARQUITECTURA DEL ÁRBOL")
        lbl.setStyleSheet("color:#1b4332; font-weight:bold; font-size:13px;")
        vl.addWidget(lbl)
        self.vis = VisualizadorGrafoNoDirigido("Árbol")
        self.vis.solicitud_eliminacion.connect(self.eliminar_seleccionado)
        vl.addWidget(self.vis, stretch=1)
        body.addWidget(viz_frame, stretch=2)

        # Panel resultados
        res_frame = QFrame()
        res_frame.setStyleSheet("background:white; border:1px solid #d8e3dc; border-radius:10px;")
        rl = QVBoxLayout(res_frame); rl.setContentsMargins(8, 8, 8, 8)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border:1px solid #d8e3dc; background:white; }
            QTabBar::tab { background:#f0f7f4; padding:8px 12px;
                           color:#1b4332; font-weight:bold; border-top-left-radius:6px; }
            QTabBar::tab:selected { background:white; color:#2d6a4f; }
        """)

        self.txt_dist = self._txt()   # Tabla de distancias + excentricidades
        self.txt_met  = self._txt()   # Centro / Radio / Diámetro / Detalles
        self.txt_paso = self._txt()   # Pasos del algoritmo

        self.tabs.addTab(self.txt_dist, "📐 Distancias")
        self.tabs.addTab(self.txt_met,  "🎯 Centro/Radio")
        self.tabs.addTab(self.txt_paso, "🪜 Pasos")

        rl.addWidget(self.tabs)
        body.addWidget(res_frame, stretch=1)

        main.addLayout(body, stretch=1)

    # ── Lógica de la vista ───────────────────────────────────────────────────
    def nuevo_grafo(self):
        n = self.spin_v.value()
        self.num_vertices = n
        self.aristas      = []
        self.actualizar_nomenclatura()
        for t in (self.txt_dist, self.txt_met, self.txt_paso):
            t.setHtml("")

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
        
        self._refresh_combos()
        self.vis.set_grafo(self.num_vertices, self.aristas, self.etiquetas, {})

    def _refresh_combos(self):
        self.cb_orig.clear(); self.cb_dest.clear()
        noms = [self.etiquetas[i] for i in range(self.num_vertices)]
        self.cb_orig.addItems(noms); self.cb_dest.addItems(noms)

    def add_arista(self):
        u, v = self.cb_orig.currentIndex(), self.cb_dest.currentIndex()
        if u == v:
            return
        a = tuple(sorted((u, v)))
        if a not in self.aristas:
            self.aristas.append(a)
        self.vis.set_grafo(self.num_vertices, self.aristas, self.etiquetas, {})

    def guardar_grafo(self):
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        import json
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Árbol Central", "", "JSON Files (*.json)")
        if archivo:
            datos = {
                'vertices': self.num_vertices,
                'aristas': self.aristas,
                'etiquetas': self.etiquetas,
                'nom': self.cb_nom.currentIndex()
            }
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4)
            QMessageBox.information(self, "Éxito", "Árbol guardado correctamente.")

    def recuperar_arbol(self):
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        import json
        archivo, _ = QFileDialog.getOpenFileName(self, "Cargar Árbol Central", "", "JSON Files (*.json)")
        if archivo:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            self.num_vertices = datos['vertices']
            self.aristas = [tuple(a) for a in datos['aristas']]
            self.etiquetas = {int(k): v for k, v in datos.get('etiquetas', {}).items()}
            self.spin_v.setValue(self.num_vertices)
            self.cb_nom.setCurrentIndex(datos.get('nom', 0))
            self.actualizar_vista()
            QMessageBox.information(self, "Éxito", "Árbol cargado correctamente.")

    def actualizar_vista(self):
        self._refresh_combos()
        self.vis.set_grafo(self.num_vertices, self.aristas, self.etiquetas, {})

    def del_arista(self):
        u, v = self.cb_orig.currentIndex(), self.cb_dest.currentIndex()
        a = tuple(sorted((u, v)))
        if a in self.aristas:
            self.aristas.remove(a)
        self.vis.set_grafo(self.num_vertices, self.aristas, self.etiquetas, {})

    def eliminar_seleccionado(self):
        sel = self.vis.objeto_seleccionado
        if sel:
            tipo, idx = sel
            if tipo == 'vertice':
                if self.num_vertices > 1:
                    self.spin_v.setValue(self.num_vertices - 1)
                    self.nuevo_grafo()
            elif tipo == 'arista':
                if 0 <= idx < len(self.aristas):
                    self.aristas.pop(idx)
                    self.vis.objeto_seleccionado = None
                    self.vis.set_grafo(self.num_vertices, self.aristas, self.etiquetas, {})
        else:
            self.del_arista()

    def ejecutar(self):
        """Delega el cálculo al controlador y muestra los resultados."""
        self.ctrl.set_grafo(self.num_vertices, self.aristas, self.etiquetas)

        centro, exc, radio, diametro, detalles = self.ctrl.calcular_centro()

        if centro is None:
            err = f"<p style='color:red;'><b>ERROR:</b> {detalles}</p>"
            self.txt_dist.setHtml(err)
            self.txt_met.setHtml(err)
            self.txt_paso.setHtml(err)
            return

        # ── Tab 1: Tabla de distancias con excentricidades ──────────────────
        html_tabla = self.ctrl.generar_tabla_distancias_html()
        self.txt_dist.setHtml(
            "<h3>Tabla de Distancias y Excentricidades</h3>"
            "<p style='font-size:11px;color:#666;'>Las filas del centro están resaltadas.</p>"
            + html_tabla
        )

        # ── Tab 2: Centro / Radio / Diámetro ────────────────────────────────
        centro_et = [self.etiquetas.get(v, str(v)) for v in centro]
        html_met = (
            f"<h3>Métricas del Árbol</h3>"
            f"<p><b>Radio:</b> {radio}</p>"
            f"<p><b>Diámetro:</b> {diametro}</p>"
            f"<p><b>🎯 CENTRO:</b> {{{', '.join(centro_et)}}}</p>"
            f"<hr>"
            f"<h4>Detalles de Excentricidades:</h4>"
        )
        for v in range(self.num_vertices):
            et = self.etiquetas.get(v, str(v))
            marca = " ⭐ CENTRO" if v in centro else ""
            color = "color:#2d6a4f; font-weight:bold;" if v in centro else ""
            html_met += (f"<p style='{color}'>e({et}) = {exc[v]}{marca}</p>")

        html_met += f"<hr><pre style='font-family:Courier; font-size:12px;'>{detalles}</pre>"
        self.txt_met.setHtml(html_met)

        # ── Tab 3: Pasos del algoritmo ───────────────────────────────────────
        pasos = self.ctrl.generar_pasos_algoritmo()
        html_p = "<h3>Pasos del Algoritmo (Poda de Hojas)</h3>"
        for paso in pasos:
            html_p += (
                f"<p><b>{paso['titulo']}</b><br>"
                f"<span style='white-space:pre;font-family:Courier;font-size:12px;'>"
                f"{paso['descripcion']}</span></p><hr>"
            )
        self.txt_paso.setHtml(html_p)

    # ── Helpers ──────────────────────────────────────────────────────────────
    def _txt(self):
        t = QTextEdit()
        t.setReadOnly(True)
        t.setStyleSheet("border:none; font-family:'Segoe UI',sans-serif; font-size:13px;")
        return t
