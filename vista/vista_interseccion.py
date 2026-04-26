"""
Vista de Intersección de Grafos  G₁ ∩ G₂
Layout: ribbon compacto + 3 paneles side-by-side + barra de estado
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QSpinBox, QFileDialog, QSplitter, QMessageBox, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from vista.visualizador_grafo import VisualizadorGrafo
from vista.dialogo_arista import DialogoArista
from vista.dialogo_clave import DialogoClave
import json


class VistaInterseccion(QWidget):

    # ── Estilos centralizados ────────────────────────────────────────────────
    _SEC = "color:#1b4332; font-size:13px; font-weight:bold;"
    _BTN = """QPushButton{background:#2d6a4f;color:white;border-radius:6px;
               padding:4px 10px;font-size:12px;border:none;font-weight:bold;}
              QPushButton:hover{background:#40916c;}
              QPushButton:pressed{background:#1b4332;}"""
    _BTN_EXEC = """QPushButton{background:#1b4332;color:white;border-radius:8px;
                   padding:6px 18px;font-size:13px;border:none;font-weight:bold;}
                  QPushButton:hover{background:#2d6a4f;}"""
    _INFO_BASE = "padding:3px 10px; font-size:11px; border-radius:4px;"

    def __init__(self, main_window, parent_nav):
        super().__init__()
        self.main_window = main_window
        self.parent_nav = parent_nav

        self.g1 = dict(v=0, a=[], e={})
        self.g2 = dict(v=0, a=[], e={})

        root = QVBoxLayout(self)
        root.setContentsMargins(8, 6, 8, 6)
        root.setSpacing(4)

        # ── 1. Header compacto ──────────────────────────────────────────────
        root.addLayout(self._header("Intersección de Grafos", "G₁  ∩  G₂"))

        # ── 2. Ribbon de controles ──────────────────────────────────────────
        root.addWidget(self._ribbon())

        # ── 3. Área de grafos (3 paneles) ───────────────────────────────────
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)

        self.vis1 = self._panel("G₁",        editable=True,  color="#e8f5e9")
        self.vis2 = self._panel("G₂",        editable=True,  color="#e3f2fd")
        self.vis_r= self._panel("G₁ ∩ G₂",   editable=False, color="#fff8e1")

        self.vis1.etiqueta_cambiada.connect(lambda i, e: self.g1['e'].update({i: e}))
        self.vis2.etiqueta_cambiada.connect(lambda i, e: self.g2['e'].update({i: e}))

        for vis in (self.vis1, self.vis2, self.vis_r):
            self.splitter.addWidget(vis)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setStretchFactor(2, 1)
        root.addWidget(self.splitter, stretch=1)

        # ── 4. Barra de estado ──────────────────────────────────────────────
        root.addWidget(self._status_bar())

    # ── CONSTRUCTORES DE WIDGETS ─────────────────────────────────────────────
    def _header(self, titulo, subtitulo):
        h = QHBoxLayout()
        btn_back = QPushButton("⬅")
        btn_back.setFixedSize(32, 32)
        btn_back.setCursor(Qt.PointingHandCursor)
        btn_back.setStyleSheet(
            "background:#1b4332;color:white;border-radius:16px;font-weight:bold;font-size:14px;border:none;")
        btn_back.clicked.connect(self.regresar_menu)
        h.addWidget(btn_back)

        lbl = QLabel(f"<b>{titulo}</b>  <span style='color:#40916c;font-size:16px;'>{subtitulo}</span>")
        lbl.setStyleSheet("font-size:20px; color:#1b4332;")
        h.addWidget(lbl)
        h.addStretch()
        return h

    def _btn(self, txt, tip=None):
        b = QPushButton(txt)
        b.setCursor(Qt.PointingHandCursor)
        b.setStyleSheet(self._BTN)
        if tip:
            b.setToolTip(tip)
        return b

    def _ribbon(self):
        frame = QFrame()
        frame.setStyleSheet(
            "background:#f0faf3; border:1px solid #b7dfc5; border-radius:8px;")
        lay = QHBoxLayout(frame)
        lay.setContentsMargins(8, 4, 8, 4)
        lay.setSpacing(5)

        # — G1 grupo —
        g1_lbl = QLabel("G₁")
        g1_lbl.setStyleSheet(self._SEC)
        lay.addWidget(g1_lbl)
        lay.addWidget(QLabel("V:"))
        self.sp1 = QSpinBox(); self.sp1.setRange(1, 20); self.sp1.setValue(4)
        self.sp1.setFixedWidth(48)
        lay.addWidget(self.sp1)

        for txt, slot in [("↺ Crear", self.crear_g1), ("+ Arista", self.agregar_a1),
                           ("− Arista", self.eliminar_a1), ("💾", self.guardar_g1),
                           ("📂", self.cargar_g1)]:
            b = self._btn(txt)
            b.clicked.connect(slot)
            lay.addWidget(b)

        # Separador
        sep = QFrame(); sep.setFrameShape(QFrame.VLine)
        sep.setStyleSheet("color:#b7dfc5;"); lay.addWidget(sep)

        # — G2 grupo —
        g2_lbl = QLabel("G₂")
        g2_lbl.setStyleSheet("color:#1a5298; font-size:13px; font-weight:bold;")
        lay.addWidget(g2_lbl)
        lay.addWidget(QLabel("V:"))
        self.sp2 = QSpinBox(); self.sp2.setRange(1, 20); self.sp2.setValue(4)
        self.sp2.setFixedWidth(48)
        lay.addWidget(self.sp2)

        for txt, slot in [("↺ Crear", self.crear_g2), ("+ Arista", self.agregar_a2),
                           ("− Arista", self.eliminar_a2), ("💾", self.guardar_g2),
                           ("📂", self.cargar_g2)]:
            b = self._btn(txt)
            b.clicked.connect(slot)
            lay.addWidget(b)

        lay.addStretch()

        btn_clear = self._btn("🗑 Limpiar")
        btn_clear.clicked.connect(self.limpiar_todo)
        lay.addWidget(btn_clear)

        btn_calc = QPushButton("▶  INTERSECTAR")
        btn_calc.setCursor(Qt.PointingHandCursor)
        btn_calc.setStyleSheet(self._BTN_EXEC)
        btn_calc.clicked.connect(self.calcular)
        lay.addWidget(btn_calc)

        return frame

    def _panel(self, titulo, editable, color):
        vis = VisualizadorGrafo(titulo, self, es_editable=editable)
        vis.setStyleSheet(f"background:{color}; border:1px solid #d8e3dc; border-radius:10px;")
        return vis

    def _status_bar(self):
        bar = QFrame()
        bar.setFixedHeight(28)
        bar.setStyleSheet("background:#f0f7f4; border:1px solid #d8e3dc; border-radius:6px;")
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(10, 0, 10, 0)
        lay.setSpacing(20)

        self.lbl_s1 = QLabel("G₁: sin datos")
        self.lbl_s2 = QLabel("G₂: sin datos")
        self.lbl_sr = QLabel("Resultado: —")

        for lbl, col in [(self.lbl_s1, "#2d6a4f"), (self.lbl_s2, "#1a5298"),
                         (self.lbl_sr, "#b05000")]:
            lbl.setStyleSheet(f"color:{col}; font-size:11px; font-weight:bold;")
            lay.addWidget(lbl)

        lay.addStretch()
        hint = QLabel("Clic en vértice → editar etiqueta  |  Clic en arista → editar peso")
        hint.setStyleSheet("color:#888; font-size:10px; font-style:italic;")
        lay.addWidget(hint)
        return bar

    def _update_status(self):
        self.lbl_s1.setText(
            f"G₁:  {self.g1['v']} vértices · {len(self.g1['a'])} aristas")
        self.lbl_s2.setText(
            f"G₂:  {self.g2['v']} vértices · {len(self.g2['a'])} aristas")

    # ── NAVEGACIÓN ───────────────────────────────────────────────────────────
    def regresar_menu(self):
        self.parent_nav.regresar_a_menu()

    # ── G1 OPERACIONES ───────────────────────────────────────────────────────
    def crear_g1(self):
        n = self.sp1.value()
        self.g1 = dict(v=n, a=[], e={i: str(i+1) for i in range(n)})
        self.vis1.set_grafo(n, [], self.g1['e'])
        self.vis_r.set_grafo(0, [], {})
        self._update_status()

    def agregar_a1(self):
        if not self.g1['v']:
            return DialogoClave(0,"","",self,"Primero crea G₁.").exec()
        dlg = DialogoArista(self.g1['v'], self, self.g1['e'])
        if dlg.exec():
            a = dlg.get_arista()
            if a not in self.g1['a']:
                self.g1['a'].append(a)
                self.vis1.set_grafo(self.g1['v'], self.g1['a'], self.g1['e'])
                self._update_status()

    def eliminar_a1(self):
        if not self.g1['a']:
            return DialogoClave(0,"","",self,"No hay aristas en G₁.").exec()
        dlg = DialogoArista(self.g1['v'], self, self.g1['e'])
        if dlg.exec():
            a = dlg.get_arista()
            if a in self.g1['a']:
                self.g1['a'].remove(a)
                self.vis1.set_grafo(self.g1['v'], self.g1['a'], self.g1['e'])
                self._update_status()

    def guardar_g1(self):
        if not self.g1['v']:
            return
        p, _ = QFileDialog.getSaveFileName(self, "Guardar G₁", "", "JSON (*.json)")
        if p:
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"vertices":self.g1['v'],"aristas":self.g1['a'],
                           "etiquetas":self.g1['e']}, f, indent=2)

    def cargar_g1(self):
        p, _ = QFileDialog.getOpenFileName(self, "Cargar G₁", "", "JSON (*.json)")
        if p:
            try:
                with open(p, encoding="utf-8") as f: d = json.load(f)
                n = d["vertices"]
                a = [tuple(x) for x in d["aristas"]]
                e = {int(k): v for k, v in d.get("etiquetas",{}).items()}
                self.g1 = dict(v=n, a=a, e=e)
                self.sp1.setValue(n)
                self.vis1.set_grafo(n, a, e)
                self._update_status()
            except Exception as ex:
                DialogoClave(0,"Error","",self,str(ex)).exec()

    # ── G2 OPERACIONES ───────────────────────────────────────────────────────
    def crear_g2(self):
        n = self.sp2.value()
        self.g2 = dict(v=n, a=[], e={i: str(i+1) for i in range(n)})
        self.vis2.set_grafo(n, [], self.g2['e'])
        self.vis_r.set_grafo(0, [], {})
        self._update_status()

    def agregar_a2(self):
        if not self.g2['v']:
            return DialogoClave(0,"","",self,"Primero crea G₂.").exec()
        dlg = DialogoArista(self.g2['v'], self, self.g2['e'])
        if dlg.exec():
            a = dlg.get_arista()
            if a not in self.g2['a']:
                self.g2['a'].append(a)
                self.vis2.set_grafo(self.g2['v'], self.g2['a'], self.g2['e'])
                self._update_status()

    def eliminar_a2(self):
        if not self.g2['a']:
            return DialogoClave(0,"","",self,"No hay aristas en G₂.").exec()
        dlg = DialogoArista(self.g2['v'], self, self.g2['e'])
        if dlg.exec():
            a = dlg.get_arista()
            if a in self.g2['a']:
                self.g2['a'].remove(a)
                self.vis2.set_grafo(self.g2['v'], self.g2['a'], self.g2['e'])
                self._update_status()

    def guardar_g2(self):
        if not self.g2['v']:
            return
        p, _ = QFileDialog.getSaveFileName(self, "Guardar G₂", "", "JSON (*.json)")
        if p:
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"vertices":self.g2['v'],"aristas":self.g2['a'],
                           "etiquetas":self.g2['e']}, f, indent=2)

    def cargar_g2(self):
        p, _ = QFileDialog.getOpenFileName(self, "Cargar G₂", "", "JSON (*.json)")
        if p:
            try:
                with open(p, encoding="utf-8") as f: d = json.load(f)
                n = d["vertices"]
                a = [tuple(x) for x in d["aristas"]]
                e = {int(k): v for k, v in d.get("etiquetas",{}).items()}
                self.g2 = dict(v=n, a=a, e=e)
                self.sp2.setValue(n)
                self.vis2.set_grafo(n, a, e)
                self._update_status()
            except Exception as ex:
                DialogoClave(0,"Error","",self,str(ex)).exec()

    # ── LIMPIAR / CALCULAR ───────────────────────────────────────────────────
    def limpiar_todo(self):
        r = QMessageBox.question(self, "Confirmar",
            "¿Limpiar todos los grafos?",
            QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.Yes:
            self.g1 = dict(v=0, a=[], e={})
            self.g2 = dict(v=0, a=[], e={})
            for vis in (self.vis1, self.vis2, self.vis_r):
                vis.set_grafo(0, [], {})
            self.lbl_sr.setText("Resultado: —")
            self._update_status()

    def calcular(self):
        if not self.g1['v'] or not self.g2['v']:
            return DialogoClave(0,"Error","",self,"Crea ambos grafos primero.").exec()

        # Vértices comunes por etiqueta
        et1 = {v: k for k, v in self.g1['e'].items()}
        et2 = {v: k for k, v in self.g2['e'].items()}
        comun = set(et1) & set(et2)

        if not comun:
            self.vis_r.set_grafo(0, [], {})
            self.lbl_sr.setText("Resultado: grafos disjuntos — sin vértices comunes")
            return

        idx_r = {et: i for i, et in enumerate(sorted(comun))}
        et_r  = {i: et for et, i in idx_r.items()}
        n_r   = len(idx_r)

        norm1 = {tuple(sorted((self.g1['e'][a[0]], self.g1['e'][a[1]])))
                 for a in self.g1['a']
                 if self.g1['e'][a[0]] in comun and self.g1['e'][a[1]] in comun}
        norm2 = {tuple(sorted((self.g2['e'][a[0]], self.g2['e'][a[1]])))
                 for a in self.g2['a']
                 if self.g2['e'][a[0]] in comun and self.g2['e'][a[1]] in comun}
        shared = norm1 & norm2

        a_r = [(idx_r[e1], idx_r[e2]) for e1, e2 in shared]
        self.vis_r.set_grafo(n_r, a_r, et_r)
        self.lbl_sr.setText(
            f"Resultado:  {n_r} vértices · {len(a_r)} aristas")
