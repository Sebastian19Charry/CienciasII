from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSpinBox, QFileDialog, QComboBox, QTabWidget, QSplitter
)
from PySide6.QtCore import Qt
from vista.visualizador_grafo import VisualizadorGrafo
from vista.dialogo_arista import DialogoArista
from vista.dialogo_clave import DialogoClave
import json


class VistaFusionContraccion(QWidget):
    """Vista que agrupa Fusión de Vértices y Contracción de Aristas"""

    def __init__(self, main_window, parent_nav):
        super().__init__()
        self.main_window = main_window
        self.parent_nav = parent_nav

        self.g_fusion = {'v': 0, 'a': [], 'e': {}}
        self.g_contra = {'v': 0, 'a': [], 'e': {}}

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

        titulo = QLabel("Transformaciones de Grafos")
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

        self.tabs.addTab(self._crear_tab_fusion(), "🤝  Fusión de Vértices")
        self.tabs.addTab(self._crear_tab_contraccion(), "✂️  Contracción de Aristas")

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

    def _guardar(self, g, nombre):
        if g['v'] == 0:
            DialogoClave(0, "Error", "mensaje", self, "El grafo está vacío.").exec()
            return
        path, _ = QFileDialog.getSaveFileName(
            self, f"Guardar {nombre}", "", "JSON (*.json)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"vertices": g['v'], "aristas": g['a'],
                           "etiquetas": g['e']}, f, indent=2)

    def _cargar(self, nombre):
        path, _ = QFileDialog.getOpenFileName(
            self, f"Cargar {nombre}", "", "JSON (*.json)")
        if not path:
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                d = json.load(f)
            return (d["vertices"],
                    [tuple(a) for a in d["aristas"]],
                    {int(k): v for k, v in d.get("etiquetas", {}).items()})
        except Exception as e:
            DialogoClave(0, "Error", "mensaje", self, str(e)).exec()
            return None

    # ════════════════════════════════════════════════════════════════════════
    # TAB FUSIÓN
    # ════════════════════════════════════════════════════════════════════════
    def _crear_tab_fusion(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(5)

        ctrls = QFrame()
        ctrls.setStyleSheet(
            "background:#f8fcf9; border:1px solid #d8e3dc; border-radius:8px;")
        l_c = QHBoxLayout(ctrls)
        l_c.setContentsMargins(10, 5, 10, 5)
        l_c.setSpacing(6)

        l_c.addWidget(QLabel("V:"))
        self.sp_v_fusion = QSpinBox()
        self.sp_v_fusion.setRange(2, 20)
        self.sp_v_fusion.setValue(4)
        l_c.addWidget(self.sp_v_fusion)

        btn_crear = self.boton_accion("Reiniciar")
        btn_crear.clicked.connect(self._crear_fusion)
        l_c.addWidget(btn_crear)

        btn_add = self.boton_accion("+ Arista")
        btn_add.clicked.connect(self._agregar_arista_fusion)
        l_c.addWidget(btn_add)

        btn_del = self.boton_accion("− Arista")
        btn_del.clicked.connect(self._eliminar_arista_fusion)
        l_c.addWidget(btn_del)

        btn_save = self.boton_accion("💾")
        btn_save.setToolTip("Guardar grafo")
        btn_save.clicked.connect(lambda: self._guardar(self.g_fusion, "Fusión"))
        l_c.addWidget(btn_save)

        btn_load = self.boton_accion("📂")
        btn_load.setToolTip("Cargar grafo")
        btn_load.clicked.connect(self._cargar_fusion)
        l_c.addWidget(btn_load)

        l_c.addSpacing(15)
        l_c.addWidget(QLabel("Fusionar:"))
        self.combo_f1 = QComboBox()
        self.combo_f2 = QComboBox()
        l_c.addWidget(self.combo_f1)
        l_c.addWidget(QLabel("↔"))
        l_c.addWidget(self.combo_f2)

        l_c.addStretch()

        btn_do = self.boton_accion("▶ FUSIONAR")
        btn_do.setStyleSheet(
            btn_do.styleSheet() + "QPushButton { background:#1b4332; }")
        btn_do.clicked.connect(self._operar_fusion)
        l_c.addWidget(btn_do)

        layout.addWidget(ctrls)

        splitter = QSplitter(Qt.Horizontal)
        self.vis_f_orig = VisualizadorGrafo("G  (original)", self)
        self.vis_f_res = VisualizadorGrafo("G'  (fusionado)", self,
                                            es_editable=False)
        self.vis_f_orig.etiqueta_cambiada.connect(
            lambda idx, et: self.g_fusion['e'].update({idx: et}) or
            self._actualizar_combos_fusion())
        for v in (self.vis_f_orig, self.vis_f_res):
            v.setStyleSheet(
                "background:white; border:1px solid #d8e3dc; border-radius:10px;")
            splitter.addWidget(v)
        layout.addWidget(splitter)

        return tab

    def _crear_fusion(self):
        n = self.sp_v_fusion.value()
        self.g_fusion = {'v': n, 'a': [], 'e': {i: str(i + 1) for i in range(n)}}
        self.vis_f_orig.set_grafo(n, [], self.g_fusion['e'])
        self.vis_f_res.set_grafo(0, [], {})
        self._actualizar_combos_fusion()

    def _agregar_arista_fusion(self):
        if self.g_fusion['v'] == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "Primero crea el grafo.").exec()
            return
        dlg = DialogoArista(self.g_fusion['v'], self, self.g_fusion['e'])
        if dlg.exec():
            a = dlg.get_arista()
            if a not in self.g_fusion['a']:
                self.g_fusion['a'].append(a)
                self.vis_f_orig.set_grafo(
                    self.g_fusion['v'], self.g_fusion['a'], self.g_fusion['e'])

    def _eliminar_arista_fusion(self):
        if not self.g_fusion['a']:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay aristas para eliminar.").exec()
            return
        dlg = DialogoArista(self.g_fusion['v'], self, self.g_fusion['e'])
        if dlg.exec():
            a = dlg.get_arista()
            if a in self.g_fusion['a']:
                self.g_fusion['a'].remove(a)
                self.vis_f_orig.set_grafo(
                    self.g_fusion['v'], self.g_fusion['a'], self.g_fusion['e'])
            else:
                DialogoClave(0, "Error", "mensaje", self,
                             "Esa arista no existe.").exec()

    def _cargar_fusion(self):
        res = self._cargar("Fusión")
        if res:
            n, a, e = res
            self.g_fusion = {'v': n, 'a': a, 'e': e}
            self.sp_v_fusion.setValue(n)
            self.vis_f_orig.set_grafo(n, a, e)
            self._actualizar_combos_fusion()

    def _actualizar_combos_fusion(self):
        self.combo_f1.clear()
        self.combo_f2.clear()
        for i, et in self.g_fusion['e'].items():
            self.combo_f1.addItem(et, i)
            self.combo_f2.addItem(et, i)

    def _operar_fusion(self):
        v1 = self.combo_f1.currentData()
        v2 = self.combo_f2.currentData()
        if v1 is None or v2 is None or v1 == v2:
            DialogoClave(0, "Error", "mensaje", self,
                         "Selecciona dos vértices distintos.").exec()
            return

        if v1 > v2:
            v1, v2 = v2, v1

        et1 = self.g_fusion['e'][v1]
        et2 = self.g_fusion['e'][v2]
        nueva_et = f"{et1},{et2}"

        n_new = self.g_fusion['v'] - 1
        et_new = {}
        mapeo = {}
        curr = 0
        for i in range(self.g_fusion['v']):
            if i == v1:
                mapeo[i] = curr
                et_new[curr] = nueva_et
                curr += 1
            elif i == v2:
                mapeo[i] = mapeo[v1]
            else:
                mapeo[i] = curr
                et_new[curr] = self.g_fusion['e'][i]
                curr += 1

        a_new = list({tuple(sorted((mapeo[a[0]], mapeo[a[1]])))
                      for a in self.g_fusion['a']
                      if mapeo[a[0]] != mapeo[a[1]]})

        self.vis_f_res.set_grafo(n_new, a_new, et_new)
        DialogoClave(0, "Fusión exitosa", "mensaje", self,
                     f"Vértices '{et1}' y '{et2}' fusionados en '{nueva_et}'.\n"
                     f"Vértices resultantes: {n_new}").exec()

    # ════════════════════════════════════════════════════════════════════════
    # TAB CONTRACCIÓN
    # ════════════════════════════════════════════════════════════════════════
    def _crear_tab_contraccion(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(5)

        ctrls = QFrame()
        ctrls.setStyleSheet(
            "background:#f8fcf9; border:1px solid #d8e3dc; border-radius:8px;")
        l_c = QHBoxLayout(ctrls)
        l_c.setContentsMargins(10, 5, 10, 5)
        l_c.setSpacing(6)

        l_c.addWidget(QLabel("V:"))
        self.sp_v_contra = QSpinBox()
        self.sp_v_contra.setRange(2, 20)
        self.sp_v_contra.setValue(4)
        l_c.addWidget(self.sp_v_contra)

        btn_crear = self.boton_accion("Reiniciar")
        btn_crear.clicked.connect(self._crear_contra)
        l_c.addWidget(btn_crear)

        btn_add = self.boton_accion("+ Arista")
        btn_add.clicked.connect(self._agregar_arista_contra)
        l_c.addWidget(btn_add)

        btn_del = self.boton_accion("− Arista")
        btn_del.clicked.connect(self._eliminar_arista_contra)
        l_c.addWidget(btn_del)

        btn_save = self.boton_accion("💾")
        btn_save.setToolTip("Guardar grafo")
        btn_save.clicked.connect(lambda: self._guardar(self.g_contra, "Contracción"))
        l_c.addWidget(btn_save)

        btn_load = self.boton_accion("📂")
        btn_load.setToolTip("Cargar grafo")
        btn_load.clicked.connect(self._cargar_contra)
        l_c.addWidget(btn_load)

        l_c.addSpacing(15)
        l_c.addWidget(QLabel("Contraer arista:"))
        self.combo_arista_contra = QComboBox()
        l_c.addWidget(self.combo_arista_contra)

        l_c.addStretch()

        btn_do = self.boton_accion("▶ CONTRAER")
        btn_do.setStyleSheet(
            btn_do.styleSheet() + "QPushButton { background:#1b4332; }")
        btn_do.clicked.connect(self._operar_contraccion)
        l_c.addWidget(btn_do)

        layout.addWidget(ctrls)

        splitter = QSplitter(Qt.Horizontal)
        self.vis_c_orig = VisualizadorGrafo("G  (original)", self)
        self.vis_c_res = VisualizadorGrafo("G'  (contraído)", self,
                                            es_editable=False)
        self.vis_c_orig.etiqueta_cambiada.connect(
            lambda idx, et: self.g_contra['e'].update({idx: et}) or
            self._actualizar_combos_contra())
        for v in (self.vis_c_orig, self.vis_c_res):
            v.setStyleSheet(
                "background:white; border:1px solid #d8e3dc; border-radius:10px;")
            splitter.addWidget(v)
        layout.addWidget(splitter)

        return tab

    def _crear_contra(self):
        n = self.sp_v_contra.value()
        self.g_contra = {'v': n, 'a': [], 'e': {i: str(i + 1) for i in range(n)}}
        self.vis_c_orig.set_grafo(n, [], self.g_contra['e'])
        self.vis_c_res.set_grafo(0, [], {})
        self._actualizar_combos_contra()

    def _agregar_arista_contra(self):
        if self.g_contra['v'] == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "Primero crea el grafo.").exec()
            return
        dlg = DialogoArista(self.g_contra['v'], self, self.g_contra['e'])
        if dlg.exec():
            a = dlg.get_arista()
            if a not in self.g_contra['a']:
                self.g_contra['a'].append(a)
                self.vis_c_orig.set_grafo(
                    self.g_contra['v'], self.g_contra['a'], self.g_contra['e'])
                self._actualizar_combos_contra()

    def _eliminar_arista_contra(self):
        if not self.g_contra['a']:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay aristas para eliminar.").exec()
            return
        dlg = DialogoArista(self.g_contra['v'], self, self.g_contra['e'])
        if dlg.exec():
            a = dlg.get_arista()
            if a in self.g_contra['a']:
                self.g_contra['a'].remove(a)
                self.vis_c_orig.set_grafo(
                    self.g_contra['v'], self.g_contra['a'], self.g_contra['e'])
                self._actualizar_combos_contra()
            else:
                DialogoClave(0, "Error", "mensaje", self,
                             "Esa arista no existe.").exec()

    def _cargar_contra(self):
        res = self._cargar("Contracción")
        if res:
            n, a, e = res
            self.g_contra = {'v': n, 'a': a, 'e': e}
            self.sp_v_contra.setValue(n)
            self.vis_c_orig.set_grafo(n, a, e)
            self._actualizar_combos_contra()

    def _actualizar_combos_contra(self):
        self.combo_arista_contra.clear()
        for a in self.g_contra['a']:
            et_o = self.g_contra['e'].get(a[0], str(a[0] + 1))
            et_d = self.g_contra['e'].get(a[1], str(a[1] + 1))
            self.combo_arista_contra.addItem(f"{et_o} — {et_d}", a)

    def _operar_contraccion(self):
        arista = self.combo_arista_contra.currentData()
        if not arista:
            DialogoClave(0, "Error", "mensaje", self,
                         "Agrega aristas al grafo primero.").exec()
            return

        v1, v2 = arista
        et1 = self.g_contra['e'][v1]
        et2 = self.g_contra['e'][v2]
        nueva_et = f"{et1},{et2}"

        n_new = self.g_contra['v'] - 1
        et_new = {}
        mapeo = {}
        curr = 0
        for i in range(self.g_contra['v']):
            if i == v1:
                mapeo[i] = curr
                et_new[curr] = nueva_et
                curr += 1
            elif i == v2:
                mapeo[i] = mapeo[v1]
            else:
                mapeo[i] = curr
                et_new[curr] = self.g_contra['e'][i]
                curr += 1

        a_new = []
        for a in self.g_contra['a']:
            if set(a) == {v1, v2}:
                continue  # Eliminar la arista contraída
            no = mapeo[a[0]]
            nd = mapeo[a[1]]
            ar = tuple(sorted((no, nd)))
            if no != nd and ar not in a_new:
                a_new.append(ar)

        self.vis_c_res.set_grafo(n_new, a_new, et_new)
        DialogoClave(0, "Contracción exitosa", "mensaje", self,
                     f"Arista ({et1} — {et2}) contraída.\n"
                     f"Nuevo vértice: '{nueva_et}'\n"
                     f"Vértices resultantes: {n_new}").exec()
