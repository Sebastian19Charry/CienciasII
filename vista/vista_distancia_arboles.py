"""
vista_distancia_arboles.py
Vista para Distancia entre Árboles.
Usa DistanciaController para toda la lógica algorítmica.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSpinBox, QTextEdit, QComboBox, QLineEdit
)
from PySide6.QtCore import Qt
from vista.visualizador_grafo_no_dirigido import VisualizadorGrafoNoDirigido
from controlador.arboles.distanciaController import DistanciaController


class VistaDistanciaArboles(QWidget):

    def __init__(self, main_window, hub):
        super().__init__()
        self.main_window = main_window
        self.hub         = hub

        # Estado de cada árbol
        self.t1_v, self.t1_e, self.t1_et, self.t1_p = 0, [], {}, {}
        self.t2_v, self.t2_e, self.t2_et, self.t2_p = 0, [], {}, {}

        self.ctrl = DistanciaController()

        self._build_ui()
        self.crear(1)
        self.crear(2)

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
        ribbon.setObjectName("ribbon")
        r = QHBoxLayout(ribbon); r.setContentsMargins(30, 0, 30, 0); r.setSpacing(20)

        # --- Definición de Widgets ---
        btn_back = QPushButton("⬅ VOLVER")
        btn_back.setFixedWidth(80); btn_back.clicked.connect(lambda: self.main_window.cambiar_pantalla(self.hub))
        
        self.cb_nom = QComboBox(); self.cb_nom.setFixedWidth(60); self.cb_nom.addItems(["123", "ABC", "abc"])
        self.cb_nom.currentIndexChanged.connect(self.actualizar_nomenclatura)

        self.spin1 = QSpinBox(); self.spin1.setRange(2, 15); self.spin1.setValue(4); self.spin1.setFixedWidth(50)
        btn_c1 = QPushButton("↺ REINICIAR T1"); btn_c1.setFixedWidth(120); btn_c1.clicked.connect(lambda: self.crear(1))
        
        self.spin2 = QSpinBox(); self.spin2.setRange(2, 15); self.spin2.setValue(4); self.spin2.setFixedWidth(50)
        btn_c2 = QPushButton("↺ REINICIAR T2"); btn_c2.setFixedWidth(120); btn_c2.clicked.connect(lambda: self.crear(2))

        btn_calc = QPushButton("⚡ CALCULAR DISTANCIA"); btn_calc.setObjectName("btn_calc"); btn_calc.clicked.connect(self.calcular)

        btn_save = QPushButton("💾 GUARDAR"); btn_save.setFixedWidth(100); btn_save.clicked.connect(self.guardar_sesion)
        self.btn_load = QPushButton("📂 RECUPERAR"); self.btn_load.setFixedWidth(120); self.btn_load.clicked.connect(self.cargar_sesion)

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

        # 2. T1 Config
        t1_lay = QVBoxLayout()
        lbl_v1 = QLabel("🌳 T1 Vértices"); lbl_v1.setFixedWidth(100)
        v1_row = QHBoxLayout(); v1_row.addWidget(lbl_v1); v1_row.addWidget(self.spin1)
        t1_lay.addLayout(v1_row); t1_lay.addWidget(btn_c1)

        # 3. T2 Config
        t2_lay = QVBoxLayout()
        lbl_v2 = QLabel("🌳 T2 Vértices"); lbl_v2.setFixedWidth(100)
        v2_row = QHBoxLayout(); v2_row.addWidget(lbl_v2); v2_row.addWidget(self.spin2)
        t2_lay.addLayout(v2_row); t2_lay.addWidget(btn_c2)

        # 4. Grupo Archivos
        file_lay = QVBoxLayout()
        file_lay.addWidget(btn_save); file_lay.addWidget(self.btn_load)

        r.addStretch(1)
        r.addLayout(nav_lay)
        r.addStretch(1)
        r.addWidget(create_sep())
        r.addStretch(1)
        r.addLayout(t1_lay)
        r.addStretch(1)
        r.addWidget(create_sep())
        r.addStretch(1)
        r.addLayout(t2_lay)
        r.addStretch(1)
        r.addWidget(create_sep())
        r.addStretch(1)
        r.addLayout(file_lay)
        r.addStretch(2)
        r.addWidget(btn_calc)
        r.addStretch(1)

        main.addWidget(ribbon)

        # ── Cuerpo: dos paneles de árboles ───────────────────────────────────
        body = QHBoxLayout(); body.setSpacing(12)

        self._panel_t1 = self._build_arbol_panel(1)
        self._panel_t2 = self._build_arbol_panel(2)
        body.addWidget(self._panel_t1)
        body.addWidget(self._panel_t2)

        main.addLayout(body, stretch=3)

        # ── Panel de resultados ──────────────────────────────────────────────
        res_frame = QFrame()
        res_frame.setStyleSheet("background:white; border:1px solid #d8e3dc; border-radius:10px;")
        rl = QVBoxLayout(res_frame); rl.setContentsMargins(10, 10, 10, 10)

        lbl_res = QLabel("📊 RESULTADO")
        lbl_res.setStyleSheet("color:#1b4332; font-weight:bold; font-size:13px;")
        rl.addWidget(lbl_res)

        self.txt_res = QTextEdit()
        self.txt_res.setReadOnly(True)
        self.txt_res.setStyleSheet(
            "border:none; font-family:'Segoe UI',sans-serif; font-size:13px;")
        rl.addWidget(self.txt_res)

        main.addWidget(res_frame, stretch=2)

    def _build_arbol_panel(self, n):
        """Construye el panel de un árbol (T1 o T2)."""
        frame = QFrame()
        frame.setStyleSheet("background:white; border:1px solid #d8e3dc; border-radius:10px;")
        lay = QVBoxLayout(frame); lay.setContentsMargins(10, 10, 10, 10); lay.setSpacing(6)

        # Título
        lbl = QLabel(f"🌳  ÁRBOL T{n}")
        lbl.setStyleSheet("color:#1b4332; font-weight:bold; font-size:13px;")
        lay.addWidget(lbl)

        # Visualizador
        vis = VisualizadorGrafoNoDirigido(f"T{n}")
        vis.solicitud_eliminacion.connect(lambda: self.del_arista(n))
        lay.addWidget(vis, stretch=1)

        # Controles de aristas
        ctrl_ss = """
            QComboBox, QLineEdit {
                background:white; color:#1b4332; border:2px solid #e0e6e3;
                border-radius:6px; padding:4px; font-weight:bold; font-size:12px;
            }
            QComboBox QAbstractItemView {
                background-color: white; color: black;
                selection-background-color: #2d6a4f; selection-color: white;
            }
            QComboBox:focus, QLineEdit:focus { border-color: #2d6a4f; }
            QLabel { color:#1b4332; font-weight:bold; font-size:10px; text-transform: uppercase; }
            QPushButton {
                background-color: #2d6a4f; color: white; font-weight: bold;
                border: none; border-radius: 8px; padding: 6px 12px; font-size: 11px;
            }
            QPushButton:hover { background-color: #1b4332; }
        """
        ctrl = QFrame(); ctrl.setStyleSheet(ctrl_ss)
        cl = QHBoxLayout(ctrl); cl.setContentsMargins(5, 5, 5, 5); cl.setSpacing(6)

        cb_o = QComboBox(); cb_o.setMinimumWidth(65); cb_o.setEditable(True)
        cb_d = QComboBox(); cb_d.setMinimumWidth(65); cb_d.setEditable(True)
        peso_edit = QLineEdit("1"); peso_edit.setFixedWidth(60)
        peso_edit.setStyleSheet("background:white; color:#1b4332; border:1px solid #2d6a4f; border-radius:4px; padding:2px 5px; font-weight:bold; min-height:26px;")

        btn_add = QPushButton("+ Arista")
        btn_del = QPushButton("🗑️ ELIMINAR")
        btn_del.setObjectName("btn_delete")

        cl.addWidget(QLabel("De:")); cl.addWidget(cb_o)
        cl.addWidget(QLabel("A:"));  cl.addWidget(cb_d)
        cl.addWidget(QLabel("W:")); cl.addWidget(peso_edit)
        cl.addWidget(btn_add); cl.addWidget(btn_del)
        lay.addWidget(ctrl)

        # Guardar refs según número de árbol
        if n == 1:
            self.vis1 = vis
            self.cb1_o, self.cb1_d, self.peso1_edit = cb_o, cb_d, peso_edit
            btn_add.clicked.connect(lambda: self.add(1))
            btn_del.clicked.connect(lambda: self.del_arista(1))
        else:
            self.vis2 = vis
            self.cb2_o, self.cb2_d, self.peso2_edit = cb_o, cb_d, peso_edit
            btn_add.clicked.connect(lambda: self.add(2))
            btn_del.clicked.connect(lambda: self.del_arista(2))

        return frame

    # ── Lógica de la vista ───────────────────────────────────────────────────
    def crear(self, n):
        """Reinicia un árbol."""
        if n == 1:
            v = self.spin1.value()
            self.t1_v = v; self.t1_e = []; self.t1_p = {}
            self.actualizar_nomenclatura_tree(1)
        else:
            v = self.spin2.value()
            self.t2_v = v; self.t2_e = []; self.t2_p = {}
            self.actualizar_nomenclatura_tree(2)

    def actualizar_nomenclatura(self):
        self.actualizar_nomenclatura_tree(1)
        self.actualizar_nomenclatura_tree(2)

    def actualizar_nomenclatura_tree(self, n):
        modo = self.cb_nom.currentText()
        if n == 1:
            v = self.t1_v
            self.t1_et = {}
            for i in range(v):
                if modo == "ABC":
                    label, t = "", i
                    while t >= 0: label = chr(65 + (t % 26)) + label; t = (t // 26) - 1
                    self.t1_et[i] = label
                elif modo == "abc":
                    label, t = "", i
                    while t >= 0: label = chr(97 + (t % 26)) + label; t = (t // 26) - 1
                    self.t1_et[i] = label
                else: self.t1_et[i] = str(i + 1)
            self.cb1_o.clear(); self.cb1_d.clear()
            labs = [self.t1_et[i] for i in range(v)]
            self.cb1_o.addItems(labs); self.cb1_d.addItems(labs)
            self.vis1.set_grafo(v, self.t1_e, self.t1_et, self.t1_p)
        else:
            v = self.t2_v
            self.t2_et = {}
            for i in range(v):
                if modo == "ABC":
                    label, t = "", i
                    while t >= 0: label = chr(65 + (t % 26)) + label; t = (t // 26) - 1
                    self.t2_et[i] = label
                elif modo == "abc":
                    label, t = "", i
                    while t >= 0: label = chr(97 + (t % 26)) + label; t = (t // 26) - 1
                    self.t2_et[i] = label
                else: self.t2_et[i] = str(i + 1)
            self.cb2_o.clear(); self.cb2_d.clear()
            labs = [self.t2_et[i] for i in range(v)]
            self.cb2_o.addItems(labs); self.cb2_d.addItems(labs)
            self.vis2.set_grafo(v, self.t2_e, self.t2_et, self.t2_p)

    def add(self, n):
        """Agrega una arista al árbol n."""
        if n == 1:
            u, v = self.cb1_o.currentIndex(), self.cb1_d.currentIndex()
            if u == v: return
            try:
                w = float(self.peso1_edit.text().replace(',', '.'))
            except ValueError:
                w = 1.0
            a = tuple(sorted((u, v)))
            if a not in self.t1_e: self.t1_e.append(a)
            self.t1_p[a] = w
            self.vis1.set_grafo(self.t1_v, self.t1_e, self.t1_et, self.t1_p)
        else:
            u, v = self.cb2_o.currentIndex(), self.cb2_d.currentIndex()
            if u == v: return
            try:
                w = float(self.peso2_edit.text().replace(',', '.'))
            except ValueError:
                w = 1.0
            a = tuple(sorted((u, v)))
            if a not in self.t2_e: self.t2_e.append(a)
            self.t2_p[a] = w
            self.vis2.set_grafo(self.t2_v, self.t2_e, self.t2_et, self.t2_p)

    def del_arista(self, n):
        """Elimina una arista o vértice seleccionado del árbol n."""
        if n == 1:
            sel = self.vis1.objeto_seleccionado
            if sel:
                tipo, idx = sel
                if tipo == 'vertice':
                    if self.t1_v > 2:
                        self.spin1.setValue(self.t1_v - 1)
                        self.crear(1)
                elif tipo == 'arista':
                    if 0 <= idx < len(self.t1_e):
                        a = self.t1_e.pop(idx)
                        self.t1_p.pop(a, None)
                        self.vis1.objeto_seleccionado = None
                        self.vis1.set_grafo(self.t1_v, self.t1_e, self.t1_et, self.t1_p)
            else:
                u, v = self.cb1_o.currentIndex(), self.cb1_d.currentIndex()
                a = tuple(sorted((u, v)))
                if a in self.t1_e: self.t1_e.remove(a)
                self.t1_p.pop(a, None)
                self.vis1.set_grafo(self.t1_v, self.t1_e, self.t1_et, self.t1_p)
        else:
            sel = self.vis2.objeto_seleccionado
            if sel:
                tipo, idx = sel
                if tipo == 'vertice':
                    if self.t2_v > 2:
                        self.spin2.setValue(self.t2_v - 1)
                        self.crear(2)
                elif tipo == 'arista':
                    if 0 <= idx < len(self.t2_e):
                        a = self.t2_e.pop(idx)
                        self.t2_p.pop(a, None)
                        self.vis2.objeto_seleccionado = None
                        self.vis2.set_grafo(self.t2_v, self.t2_e, self.t2_et, self.t2_p)
            else:
                u, v = self.cb2_o.currentIndex(), self.cb2_d.currentIndex()
                a = tuple(sorted((u, v)))
                if a in self.t2_e: self.t2_e.remove(a)
                self.t2_p.pop(a, None)
                self.vis2.set_grafo(self.t2_v, self.t2_e, self.t2_et, self.t2_p)

    def calcular(self):
        """Delega el cálculo al DistanciaController y muestra el reporte HTML completo."""
        self.ctrl.set_arbol1(self.t1_v, self.t1_e, self.t1_et, self.t1_p)
        self.ctrl.set_arbol2(self.t2_v, self.t2_e, self.t2_et, self.t2_p)

        distancia, detalles = self.ctrl.calcular_distancia_arboles()

        if distancia is None:
            self.txt_res.setHtml(
                f"<p style='color:red;'><b>ERROR:</b> {detalles}</p>")
            return

        # Usar el reporte HTML completo del controlador (idéntico a la referencia)
        html = self.ctrl.generar_reporte_html(detalles)
        self.txt_res.setHtml(html)

    def guardar_sesion(self):
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        import json
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Sesión Distancia", "", "JSON Files (*.json)")
        if archivo:
            datos = {
                't1': { 'v': self.t1_v, 'e': self.t1_e, 'et': self.t1_et, 'p': {str(k):v for k,v in self.t1_p.items()} },
                't2': { 'v': self.t2_v, 'e': self.t2_e, 'et': self.t2_et, 'p': {str(k):v for k,v in self.t2_p.items()} },
                'nom': self.cb_nom.currentIndex()
            }
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4)
            QMessageBox.information(self, "Éxito", "Sesión guardada correctamente.")

    def cargar_sesion(self):
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        import json
        archivo, _ = QFileDialog.getOpenFileName(self, "Cargar Sesión Distancia", "", "JSON Files (*.json)")
        if archivo:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            # T1
            self.t1_v = datos['t1']['v']
            self.t1_e = [tuple(a) for a in datos['t1']['e']]
            self.t1_et = {int(k): v for k, v in datos['t1']['et'].items()}
            self.t1_p = {}
            for k, v in datos['t1'].get('p', {}).items():
                try: self.t1_p[tuple(map(int, k.strip('()').split(', ')))] = v
                except: pass
            self.spin1.setValue(self.t1_v)
            # T2
            self.t2_v = datos['t2']['v']
            self.t2_e = [tuple(a) for a in datos['t2']['e']]
            self.t2_et = {int(k): v for k, v in datos['t2']['et'].items()}
            self.t2_p = {}
            for k, v in datos['t2'].get('p', {}).items():
                try: self.t2_p[tuple(map(int, k.strip('()').split(', ')))] = v
                except: pass
            self.spin2.setValue(self.t2_v)
            
            self.cb_nom.setCurrentIndex(datos.get('nom', 0))
            self.vis1.set_grafo(self.t1_v, self.t1_e, self.t1_et, self.t1_p)
            self.vis2.set_grafo(self.t2_v, self.t2_e, self.t2_et, self.t2_p)
            self._actualizar_combos(1); self._actualizar_combos(2)
            QMessageBox.information(self, "Éxito", "Sesión cargada correctamente.")

    def _actualizar_combos(self, n):
        if n == 1:
            self.cb1_o.clear(); self.cb1_d.clear()
            items = [self.t1_et.get(i, str(i+1)) for i in range(self.t1_v)]
            self.cb1_o.addItems(items); self.cb1_d.addItems(items)
        else:
            self.cb2_o.clear(); self.cb2_d.clear()
            items = [self.t2_et.get(i, str(i+1)) for i in range(self.t2_v)]
            self.cb2_o.addItems(items); self.cb2_d.addItems(items)
