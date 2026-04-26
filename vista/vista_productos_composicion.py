from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSpinBox, QFileDialog, QTabWidget, QSplitter
)
from PySide6.QtCore import Qt
from vista.visualizador_grafo import VisualizadorGrafo
from vista.dialogo_arista import DialogoArista
from vista.dialogo_clave import DialogoClave
import json


class VistaProductosComposicion(QWidget):
    """Vista que agrupa Productos (Cartesiano, Tensorial) y Composición de Grafos"""

    def __init__(self, main_window, parent_nav):
        super().__init__()
        self.main_window = main_window
        self.parent_nav = parent_nav

        self.g1 = {'v': 0, 'a': [], 'e': {}}
        self.g2 = {'v': 0, 'a': [], 'e': {}}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        # ── Header ──────────────────────────────────────────────────────────
        header = QHBoxLayout()
        self.btn_regresar = QPushButton("  ⬅  ")
        self.btn_regresar.setCursor(Qt.PointingHandCursor)
        self.btn_regresar.setFixedSize(35, 35)
        self.btn_regresar.setStyleSheet(
            "background:#1b4332; color:white; border-radius:17px; font-weight:bold;")
        self.btn_regresar.clicked.connect(self.regresar_menu)
        header.addWidget(self.btn_regresar)

        titulo = QLabel("Álgebra de Grafos — Productos y Composición")
        titulo.setStyleSheet("font-size:22px; font-weight:bold; color:#1b4332;")
        header.addWidget(titulo)
        header.addStretch()
        layout.addLayout(header)

        # ── Ribbon de entrada G1 y G2 ────────────────────────────────────────
        panel_in = QFrame()
        panel_in.setStyleSheet(
            "background:#f8fcf9; border:1px solid #d8e3dc; border-radius:8px;")
        lyt_in = QHBoxLayout(panel_in)
        lyt_in.setContentsMargins(10, 5, 10, 5)
        lyt_in.setSpacing(6)

        # G1
        lbl_g1 = QLabel("<b>G₁</b>")
        lbl_g1.setStyleSheet("color:#1b4332; font-size:14px;")
        lyt_in.addWidget(lbl_g1)
        lyt_in.addWidget(QLabel("V:"))
        self.sp1 = QSpinBox()
        self.sp1.setRange(2, 6)
        self.sp1.setValue(3)
        lyt_in.addWidget(self.sp1)
        btn_c1 = self.boton_accion("Reiniciar")
        btn_c1.clicked.connect(self.crear_g1)
        lyt_in.addWidget(btn_c1)
        btn_a1 = self.boton_accion("+ Arista")
        btn_a1.clicked.connect(self.agregar_a1)
        lyt_in.addWidget(btn_a1)
        btn_d1 = self.boton_accion("− Arista")
        btn_d1.clicked.connect(self.eliminar_a1)
        lyt_in.addWidget(btn_d1)
        btn_s1 = self.boton_accion("💾")
        btn_s1.setToolTip("Guardar G₁")
        btn_s1.clicked.connect(lambda: self._guardar(self.g1, "G₁"))
        lyt_in.addWidget(btn_s1)
        btn_l1 = self.boton_accion("📂")
        btn_l1.setToolTip("Cargar G₁")
        btn_l1.clicked.connect(self._cargar_g1)
        lyt_in.addWidget(btn_l1)

        lyt_in.addSpacing(20)

        # G2
        lbl_g2 = QLabel("<b>G₂</b>")
        lbl_g2.setStyleSheet("color:#1b4332; font-size:14px;")
        lyt_in.addWidget(lbl_g2)
        lyt_in.addWidget(QLabel("V:"))
        self.sp2 = QSpinBox()
        self.sp2.setRange(2, 6)
        self.sp2.setValue(3)
        lyt_in.addWidget(self.sp2)
        btn_c2 = self.boton_accion("Reiniciar")
        btn_c2.clicked.connect(self.crear_g2)
        lyt_in.addWidget(btn_c2)
        btn_a2 = self.boton_accion("+ Arista")
        btn_a2.clicked.connect(self.agregar_a2)
        lyt_in.addWidget(btn_a2)
        btn_d2 = self.boton_accion("− Arista")
        btn_d2.clicked.connect(self.eliminar_a2)
        lyt_in.addWidget(btn_d2)
        btn_s2 = self.boton_accion("💾")
        btn_s2.setToolTip("Guardar G₂")
        btn_s2.clicked.connect(lambda: self._guardar(self.g2, "G₂"))
        lyt_in.addWidget(btn_s2)
        btn_l2 = self.boton_accion("📂")
        btn_l2.setToolTip("Cargar G₂")
        btn_l2.clicked.connect(self._cargar_g2)
        lyt_in.addWidget(btn_l2)

        lyt_in.addStretch()
        layout.addWidget(panel_in)

        # ── Splitter vertical: grafos arriba / operaciones abajo ─────────────
        v_splitter = QSplitter(Qt.Vertical)

        # Grafos de entrada
        h_splitter = QSplitter(Qt.Horizontal)
        self.vis1 = VisualizadorGrafo("G₁", self)
        self.vis2 = VisualizadorGrafo("G₂", self)
        self.vis1.etiqueta_cambiada.connect(
            lambda idx, et: self.g1['e'].update({idx: et}))
        self.vis2.etiqueta_cambiada.connect(
            lambda idx, et: self.g2['e'].update({idx: et}))
        for v in (self.vis1, self.vis2):
            v.setStyleSheet(
                "background:white; border:1px solid #d8e3dc; border-radius:10px;")
            h_splitter.addWidget(v)
        v_splitter.addWidget(h_splitter)

        # Tabs de operaciones
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #d8e3dc;
                border-radius: 8px;
                background: white;
            }
            QTabBar::tab {
                background: #f0f7f4;
                padding: 8px 18px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                color: #1b4332;
                font-weight: bold;
                font-size: 13px;
            }
            QTabBar::tab:selected {
                background: white;
                border: 1px solid #d8e3dc;
                border-bottom-color: white;
                color: #2d6a4f;
            }
        """)

        self.tab_cart = self._crear_tab("Cartesiano  □", self.operar_cartesiano)
        self.tab_tens = self._crear_tab("Tensorial  ⊗", self.operar_tensorial)
        self.tab_comp = self._crear_tab("Composición  ∘", self.operar_composicion)

        self.tabs.addTab(self.tab_cart, "□  Cartesiano")
        self.tabs.addTab(self.tab_tens, "⊗  Tensorial")
        self.tabs.addTab(self.tab_comp, "∘  Composición")

        v_splitter.addWidget(self.tabs)
        v_splitter.setStretchFactor(0, 1)
        v_splitter.setStretchFactor(1, 2)

        layout.addWidget(v_splitter)

    # ── Utilidades ───────────────────────────────────────────────────────────
    def boton_accion(self, t):
        btn = QPushButton(t)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background: #2d6a4f;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 12px;
                border: none;
            }
            QPushButton:hover { background: #40916c; }
            QPushButton:pressed { background: #1b4332; }
        """)
        return btn

    def regresar_menu(self):
        self.parent_nav.regresar_a_menu()

    def _crear_tab(self, titulo_op, func_op):
        tab = QWidget()
        lyt = QVBoxLayout(tab)
        lyt.setContentsMargins(8, 8, 8, 8)

        hdr = QHBoxLayout()
        hdr.addWidget(QLabel(f"<b>{titulo_op}</b>"))
        hdr.addStretch()
        btn_calc = self.boton_accion("▶ CALCULAR")
        btn_calc.setStyleSheet(
            btn_calc.styleSheet() + "QPushButton { background:#1b4332; }")
        btn_calc.clicked.connect(func_op)
        hdr.addWidget(btn_calc)
        lyt.addLayout(hdr)

        vis = VisualizadorGrafo("Resultado", self, es_editable=False)
        vis.setStyleSheet(
            "background:white; border:1px solid #d8e3dc; border-radius:10px;")
        lyt.addWidget(vis)

        tab.vis_res = vis
        return tab

    def _guardar(self, g, nombre):
        if g['v'] == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         f"{nombre} está vacío.").exec()
            return
        path, _ = QFileDialog.getSaveFileName(
            self, f"Guardar {nombre}", "", "JSON (*.json)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"vertices": g['v'], "aristas": g['a'],
                           "etiquetas": g['e']}, f, indent=2)

    def _cargar_g1(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Cargar G₁", "", "JSON (*.json)")
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    d = json.load(f)
                n = d["vertices"]
                a = [tuple(x) for x in d["aristas"]]
                e = {int(k): v for k, v in d.get("etiquetas", {}).items()}
                self.g1 = {'v': n, 'a': a, 'e': e}
                self.sp1.setValue(n)
                self.vis1.set_grafo(n, a, e)
            except Exception as ex:
                DialogoClave(0, "Error", "mensaje", self, str(ex)).exec()

    def _cargar_g2(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Cargar G₂", "", "JSON (*.json)")
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    d = json.load(f)
                n = d["vertices"]
                a = [tuple(x) for x in d["aristas"]]
                e = {int(k): v for k, v in d.get("etiquetas", {}).items()}
                self.g2 = {'v': n, 'a': a, 'e': e}
                self.sp2.setValue(n)
                self.vis2.set_grafo(n, a, e)
            except Exception as ex:
                DialogoClave(0, "Error", "mensaje", self, str(ex)).exec()

    # ── Crear / Manejar grafos ───────────────────────────────────────────────
    def crear_g1(self):
        n = self.sp1.value()
        self.g1 = {'v': n, 'a': [], 'e': {i: chr(65 + i) for i in range(n)}}
        self.vis1.set_grafo(n, [], self.g1['e'])

    def crear_g2(self):
        n = self.sp2.value()
        self.g2 = {'v': n, 'a': [], 'e': {i: str(i + 1) for i in range(n)}}
        self.vis2.set_grafo(n, [], self.g2['e'])

    def agregar_a1(self):
        if self.g1['v'] == 0:
            DialogoClave(0, "Error", "mensaje", self, "Primero crea G₁.").exec()
            return
        dlg = DialogoArista(self.g1['v'], self, self.g1['e'])
        if dlg.exec():
            a = dlg.get_arista()
            if a not in self.g1['a']:
                self.g1['a'].append(a)
                self.vis1.set_grafo(self.g1['v'], self.g1['a'], self.g1['e'])

    def agregar_a2(self):
        if self.g2['v'] == 0:
            DialogoClave(0, "Error", "mensaje", self, "Primero crea G₂.").exec()
            return
        dlg = DialogoArista(self.g2['v'], self, self.g2['e'])
        if dlg.exec():
            a = dlg.get_arista()
            if a not in self.g2['a']:
                self.g2['a'].append(a)
                self.vis2.set_grafo(self.g2['v'], self.g2['a'], self.g2['e'])

    def eliminar_a1(self):
        if not self.g1['a']:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay aristas en G₁.").exec()
            return
        dlg = DialogoArista(self.g1['v'], self, self.g1['e'])
        if dlg.exec():
            a = dlg.get_arista()
            if a in self.g1['a']:
                self.g1['a'].remove(a)
                self.vis1.set_grafo(self.g1['v'], self.g1['a'], self.g1['e'])

    def eliminar_a2(self):
        if not self.g2['a']:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay aristas en G₂.").exec()
            return
        dlg = DialogoArista(self.g2['v'], self, self.g2['e'])
        if dlg.exec():
            a = dlg.get_arista()
            if a in self.g2['a']:
                self.g2['a'].remove(a)
                self.vis2.set_grafo(self.g2['v'], self.g2['a'], self.g2['e'])

    def _check_grafos(self):
        if self.g1['v'] == 0 or self.g2['v'] == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "Crea y configura ambos grafos primero.").exec()
            return False
        return True

    # ── Operaciones ──────────────────────────────────────────────────────────
    def _build_mapeo(self):
        n1, n2 = self.g1['v'], self.g2['v']
        mapeo = {}
        et_res = {}
        curr = 0
        for i in range(n1):
            for j in range(n2):
                mapeo[(i, j)] = curr
                et_res[curr] = f"{self.g1['e'].get(i, str(i+1))}"  \
                                f"{self.g2['e'].get(j, str(j+1))}"
                curr += 1
        return mapeo, et_res, n1 * n2

    def operar_cartesiano(self):
        if not self._check_grafos():
            return
        n1, n2 = self.g1['v'], self.g2['v']
        mapeo, et_res, n_res = self._build_mapeo()

        a_res = []
        # u constante, aristas de G2
        for u in range(n1):
            for a2 in self.g2['a']:
                a_res.append((mapeo[(u, a2[0])], mapeo[(u, a2[1])]))
        # v constante, aristas de G1
        for v in range(n2):
            for a1 in self.g1['a']:
                a_res.append((mapeo[(a1[0], v)], mapeo[(a1[1], v)]))

        self.tab_cart.vis_res.set_grafo(n_res, a_res, et_res)

    def operar_tensorial(self):
        if not self._check_grafos():
            return
        mapeo, et_res, n_res = self._build_mapeo()

        a_res = []
        for a1 in self.g1['a']:
            for a2 in self.g2['a']:
                a_res.append((mapeo[(a1[0], a2[0])], mapeo[(a1[1], a2[1])]))
                a_res.append((mapeo[(a1[0], a2[1])], mapeo[(a1[1], a2[0])]))

        self.tab_tens.vis_res.set_grafo(n_res, a_res, et_res)

    def operar_composicion(self):
        if not self._check_grafos():
            return
        mapeo, et_res, n_res = self._build_mapeo()

        ady1 = {tuple(sorted(a)) for a in self.g1['a']}
        ady2 = {tuple(sorted(a)) for a in self.g2['a']}
        inv_mapeo = {v: k for k, v in mapeo.items()}

        a_res = []
        for idx1 in range(n_res):
            for idx2 in range(idx1 + 1, n_res):
                u1, v1 = inv_mapeo[idx1]
                u2, v2 = inv_mapeo[idx2]
                if tuple(sorted((u1, u2))) in ady1:
                    a_res.append((idx1, idx2))
                elif u1 == u2 and tuple(sorted((v1, v2))) in ady2:
                    a_res.append((idx1, idx2))

        self.tab_comp.vis_res.set_grafo(n_res, a_res, et_res)
