from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSpinBox, QFileDialog, QTabWidget, QSplitter, QMessageBox
)
from PySide6.QtCore import Qt
from vista.visualizador_grafo import VisualizadorGrafo
from vista.dialogo_arista import DialogoArista
from vista.dialogo_clave import DialogoClave
import json


class VistaLineaComplemento(QWidget):
    """Vista que agrupa Grafo Línea L(G) y Grafo Complementario Ḡ"""

    def __init__(self, main_window, parent_nav):
        super().__init__()
        self.main_window = main_window
        self.parent_nav = parent_nav

        # ── Estados independientes por tab ───────────────────────────────────
        self.g_linea = {'v': 0, 'a': [], 'e': {}}
        self.g_comple = {'v': 0, 'a': [], 'e': {}}

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

        titulo = QLabel("Álgebra de Grafos — Línea y Complemento")
        titulo.setStyleSheet("font-size:22px; font-weight:bold; color:#1b4332;")
        header.addWidget(titulo)
        header.addStretch()
        layout.addLayout(header)

        # ── Tabs ─────────────────────────────────────────────────────────────
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

        self.tab_linea = self._crear_tab_linea()
        self.tab_comple = self._crear_tab_complemento()

        self.tabs.addTab(self.tab_linea, "🛤️  Grafo Línea  L(G)")
        self.tabs.addTab(self.tab_comple, "🌓  Complemento  Ḡ")

        layout.addWidget(self.tabs)

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

    # ════════════════════════════════════════════════════════════════════════
    # TAB GRAFO LÍNEA
    # ════════════════════════════════════════════════════════════════════════
    def _crear_tab_linea(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(5)

        # Ribbon
        ctrls = QFrame()
        ctrls.setStyleSheet(
            "background:#f8fcf9; border:1px solid #d8e3dc; border-radius:8px;")
        l_c = QHBoxLayout(ctrls)
        l_c.setContentsMargins(10, 5, 10, 5)
        l_c.setSpacing(6)

        l_c.addWidget(QLabel("<b>G</b>"))
        l_c.addWidget(QLabel("V:"))
        self.sp_v_linea = QSpinBox()
        self.sp_v_linea.setRange(2, 20)
        self.sp_v_linea.setValue(4)
        l_c.addWidget(self.sp_v_linea)

        btn_crear = self.boton_accion("Reiniciar")
        btn_crear.clicked.connect(self.crear_grafo_linea)
        l_c.addWidget(btn_crear)

        btn_add = self.boton_accion("+ Arista")
        btn_add.clicked.connect(self.agregar_arista_linea)
        l_c.addWidget(btn_add)

        btn_del = self.boton_accion("− Arista")
        btn_del.clicked.connect(self.eliminar_arista_linea)
        l_c.addWidget(btn_del)

        btn_save = self.boton_accion("💾")
        btn_save.setToolTip("Guardar G")
        btn_save.clicked.connect(self.guardar_linea)
        l_c.addWidget(btn_save)

        btn_load = self.boton_accion("📂")
        btn_load.setToolTip("Cargar G")
        btn_load.clicked.connect(self.cargar_linea)
        l_c.addWidget(btn_load)

        l_c.addStretch()

        btn_gen = self.boton_accion("▶ GENERAR  L(G)")
        btn_gen.setStyleSheet(
            btn_gen.styleSheet() + "QPushButton { background:#1b4332; }")
        btn_gen.clicked.connect(self.operar_linea)
        l_c.addWidget(btn_gen)

        layout.addWidget(ctrls)

        # Visualizadores
        splitter = QSplitter(Qt.Horizontal)
        self.vis_l_orig = VisualizadorGrafo("Grafo G", self)
        self.vis_l_res = VisualizadorGrafo("L(G)", self, es_editable=False)
        self.vis_l_orig.etiqueta_cambiada.connect(
            lambda idx, et: self.g_linea['e'].update({idx: et}))
        for v in (self.vis_l_orig, self.vis_l_res):
            v.setStyleSheet(
                "background:white; border:1px solid #d8e3dc; border-radius:10px;")
            splitter.addWidget(v)
        layout.addWidget(splitter)

        return tab

    # ── Lógica Grafo Línea ───────────────────────────────────────────────────
    def crear_grafo_linea(self):
        n = self.sp_v_linea.value()
        self.g_linea = {'v': n, 'a': [], 'e': {i: str(i + 1) for i in range(n)}}
        self.vis_l_orig.set_grafo(n, [], self.g_linea['e'])
        self.vis_l_res.set_grafo(0, [], {})

    def agregar_arista_linea(self):
        if self.g_linea['v'] == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "Primero crea el grafo G.").exec()
            return
        dlg = DialogoArista(self.g_linea['v'], self, self.g_linea['e'])
        if dlg.exec():
            a = dlg.get_arista()
            if a not in self.g_linea['a']:
                self.g_linea['a'].append(a)
                self.vis_l_orig.set_grafo(
                    self.g_linea['v'], self.g_linea['a'], self.g_linea['e'])

    def eliminar_arista_linea(self):
        if not self.g_linea['a']:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay aristas para eliminar.").exec()
            return
        dlg = DialogoArista(self.g_linea['v'], self, self.g_linea['e'])
        if dlg.exec():
            a = dlg.get_arista()
            if a in self.g_linea['a']:
                self.g_linea['a'].remove(a)
                self.vis_l_orig.set_grafo(
                    self.g_linea['v'], self.g_linea['a'], self.g_linea['e'])
            else:
                DialogoClave(0, "Error", "mensaje", self,
                             "Esa arista no existe.").exec()

    def guardar_linea(self):
        if self.g_linea['v'] == 0:
            DialogoClave(0, "Error", "mensaje", self, "G está vacío.").exec()
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar G", "", "JSON (*.json)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"vertices": self.g_linea['v'],
                           "aristas": self.g_linea['a'],
                           "etiquetas": self.g_linea['e']}, f, indent=2)

    def cargar_linea(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Cargar G", "", "JSON (*.json)")
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    d = json.load(f)
                n = d["vertices"]
                a = [tuple(x) for x in d["aristas"]]
                e = {int(k): v for k, v in d.get("etiquetas", {}).items()}
                self.g_linea = {'v': n, 'a': a, 'e': e}
                self.sp_v_linea.setValue(n)
                self.vis_l_orig.set_grafo(n, a, e)
            except Exception as ex:
                DialogoClave(0, "Error", "mensaje", self, str(ex)).exec()

    def operar_linea(self):
        if not self.g_linea['a']:
            DialogoClave(0, "Error", "mensaje", self,
                         "Agrega al menos una arista a G.").exec()
            return
        n_res = len(self.g_linea['a'])
        et_res = {}
        for i, a in enumerate(self.g_linea['a']):
            et_res[i] = (f"{self.g_linea['e'].get(a[0], a[0]+1)}"
                         f"{self.g_linea['e'].get(a[1], a[1]+1)}")
        a_res = []
        for i in range(n_res):
            for j in range(i + 1, n_res):
                a1 = self.g_linea['a'][i]
                a2 = self.g_linea['a'][j]
                if set(a1) & set(a2):
                    a_res.append((i, j))
        self.vis_l_res.set_grafo(n_res, a_res, et_res)
        DialogoClave(0, "L(G) generado", "mensaje", self,
                     f"Grafo Línea generado exitosamente.\n"
                     f"Vértices de L(G): {n_res}\n"
                     f"Aristas de L(G): {len(a_res)}").exec()

    # ════════════════════════════════════════════════════════════════════════
    # TAB GRAFO COMPLEMENTO
    # ════════════════════════════════════════════════════════════════════════
    def _crear_tab_complemento(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(5)

        # Ribbon
        ctrls = QFrame()
        ctrls.setStyleSheet(
            "background:#f8fcf9; border:1px solid #d8e3dc; border-radius:8px;")
        l_c = QHBoxLayout(ctrls)
        l_c.setContentsMargins(10, 5, 10, 5)
        l_c.setSpacing(6)

        l_c.addWidget(QLabel("<b>G</b>"))
        l_c.addWidget(QLabel("V:"))
        self.sp_v_comple = QSpinBox()
        self.sp_v_comple.setRange(2, 20)
        self.sp_v_comple.setValue(4)
        l_c.addWidget(self.sp_v_comple)

        btn_crear = self.boton_accion("Reiniciar")
        btn_crear.clicked.connect(self.crear_grafo_comple)
        l_c.addWidget(btn_crear)

        btn_add = self.boton_accion("+ Arista")
        btn_add.clicked.connect(self.agregar_arista_comple)
        l_c.addWidget(btn_add)

        btn_del = self.boton_accion("− Arista")
        btn_del.clicked.connect(self.eliminar_arista_comple)
        l_c.addWidget(btn_del)

        btn_save = self.boton_accion("💾")
        btn_save.setToolTip("Guardar G")
        btn_save.clicked.connect(self.guardar_comple)
        l_c.addWidget(btn_save)

        btn_load = self.boton_accion("📂")
        btn_load.setToolTip("Cargar G")
        btn_load.clicked.connect(self.cargar_comple)
        l_c.addWidget(btn_load)

        l_c.addStretch()

        btn_gen = self.boton_accion("▶ GENERAR  Ḡ")
        btn_gen.setStyleSheet(
            btn_gen.styleSheet() + "QPushButton { background:#1b4332; }")
        btn_gen.clicked.connect(self.operar_comple)
        l_c.addWidget(btn_gen)

        layout.addWidget(ctrls)

        # Visualizadores
        splitter = QSplitter(Qt.Horizontal)
        self.vis_c_orig = VisualizadorGrafo("Grafo G", self)
        self.vis_c_res = VisualizadorGrafo("Ḡ  (Complemento)", self,
                                            es_editable=False)
        self.vis_c_orig.etiqueta_cambiada.connect(
            lambda idx, et: self.g_comple['e'].update({idx: et}))
        for v in (self.vis_c_orig, self.vis_c_res):
            v.setStyleSheet(
                "background:white; border:1px solid #d8e3dc; border-radius:10px;")
            splitter.addWidget(v)
        layout.addWidget(splitter)

        return tab

    # ── Lógica Complemento ───────────────────────────────────────────────────
    def crear_grafo_comple(self):
        n = self.sp_v_comple.value()
        self.g_comple = {'v': n, 'a': [], 'e': {i: str(i + 1) for i in range(n)}}
        self.vis_c_orig.set_grafo(n, [], self.g_comple['e'])
        self.vis_c_res.set_grafo(0, [], {})

    def agregar_arista_comple(self):
        if self.g_comple['v'] == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "Primero crea el grafo G.").exec()
            return
        dlg = DialogoArista(self.g_comple['v'], self, self.g_comple['e'])
        if dlg.exec():
            a = dlg.get_arista()
            if a not in self.g_comple['a']:
                self.g_comple['a'].append(a)
                self.vis_c_orig.set_grafo(
                    self.g_comple['v'], self.g_comple['a'], self.g_comple['e'])

    def eliminar_arista_comple(self):
        if not self.g_comple['a']:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay aristas para eliminar.").exec()
            return
        dlg = DialogoArista(self.g_comple['v'], self, self.g_comple['e'])
        if dlg.exec():
            a = dlg.get_arista()
            if a in self.g_comple['a']:
                self.g_comple['a'].remove(a)
                self.vis_c_orig.set_grafo(
                    self.g_comple['v'], self.g_comple['a'], self.g_comple['e'])
            else:
                DialogoClave(0, "Error", "mensaje", self,
                             "Esa arista no existe.").exec()

    def guardar_comple(self):
        if self.g_comple['v'] == 0:
            DialogoClave(0, "Error", "mensaje", self, "G está vacío.").exec()
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar G", "", "JSON (*.json)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"vertices": self.g_comple['v'],
                           "aristas": self.g_comple['a'],
                           "etiquetas": self.g_comple['e']}, f, indent=2)

    def cargar_comple(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Cargar G", "", "JSON (*.json)")
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    d = json.load(f)
                n = d["vertices"]
                a = [tuple(x) for x in d["aristas"]]
                e = {int(k): v for k, v in d.get("etiquetas", {}).items()}
                self.g_comple = {'v': n, 'a': a, 'e': e}
                self.sp_v_comple.setValue(n)
                self.vis_c_orig.set_grafo(n, a, e)
            except Exception as ex:
                DialogoClave(0, "Error", "mensaje", self, str(ex)).exec()

    def operar_comple(self):
        if self.g_comple['v'] < 2:
            DialogoClave(0, "Error", "mensaje", self,
                         "Se necesitan al menos 2 vértices.").exec()
            return
        n = self.g_comple['v']
        existentes = {tuple(sorted(a)) for a in self.g_comple['a']}
        a_res = []
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) not in existentes:
                    a_res.append((i, j))
        self.vis_c_res.set_grafo(n, a_res, self.g_comple['e'])
        DialogoClave(0, "Complemento generado", "mensaje", self,
                     f"Ḡ generado exitosamente.\n"
                     f"Vértices: {n}\n"
                     f"Aristas en Ḡ: {len(a_res)}\n"
                     f"(aristas que no estaban en G)").exec()
