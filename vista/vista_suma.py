from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame,
    QHBoxLayout, QPushButton, QSpinBox, QFileDialog, QSplitter
)
from PySide6.QtCore import Qt
from vista.visualizador_grafo import VisualizadorGrafo
from vista.dialogo_arista import DialogoArista
from vista.dialogo_clave import DialogoClave
import json


class VistaSuma(QWidget):
    """
    Suma de Grafos (Join): G₁ + G₂
    Vértices = V(G₁) ∪ V(G₂)  (renombrando para diferenciarlos)
    Aristas  = E(G₁) ∪ E(G₂) ∪ {todas las aristas entre V(G₁) y V(G₂)}
    """

    def __init__(self, main_window, parent_nav):
        super().__init__()
        self.main_window = main_window
        self.parent_nav = parent_nav

        self.grafo1_vertices = 0
        self.grafo1_aristas = []
        self.grafo1_etiquetas = {}
        self.grafo2_vertices = 0
        self.grafo2_aristas = []
        self.grafo2_etiquetas = {}

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

        titulo = QLabel("Suma de Grafos  (G₁ + G₂) — Join")
        titulo.setStyleSheet("font-size:22px; font-weight:bold; color:#1b4332;")
        header.addWidget(titulo)
        header.addStretch()
        layout.addLayout(header)

        # Nota informativa
        nota = QLabel("  📌  Conecta todos los vértices de G₁ con todos los de G₂")
        nota.setStyleSheet(
            "background:#e9f5ef; color:#1b4332; border-radius:6px; "
            "padding:4px 10px; font-size:11px;")
        layout.addWidget(nota)

        # ── Ribbon de controles ─────────────────────────────────────────────
        ctrls = QFrame()
        ctrls.setStyleSheet(
            "background:#f8fcf9; border:1px solid #d8e3dc; border-radius:8px;")
        l_ctrls = QHBoxLayout(ctrls)
        l_ctrls.setContentsMargins(10, 5, 10, 5)
        l_ctrls.setSpacing(6)

        # — G1 —
        lbl_g1 = QLabel("<b>G₁</b>")
        lbl_g1.setStyleSheet("color:#1b4332; font-size:14px;")
        l_ctrls.addWidget(lbl_g1)
        l_ctrls.addWidget(QLabel("V:"))
        self.sp1 = QSpinBox()
        self.sp1.setRange(1, 10)
        self.sp1.setValue(3)
        l_ctrls.addWidget(self.sp1)
        btn_c1 = self.boton_accion("Reiniciar")
        btn_c1.clicked.connect(self.crear_g1)
        l_ctrls.addWidget(btn_c1)
        btn_a1 = self.boton_accion("+ Arista")
        btn_a1.clicked.connect(self.agregar_a1)
        l_ctrls.addWidget(btn_a1)
        btn_d1 = self.boton_accion("− Arista")
        btn_d1.clicked.connect(self.eliminar_a1)
        l_ctrls.addWidget(btn_d1)
        btn_s1 = self.boton_accion("💾")
        btn_s1.setToolTip("Guardar G₁")
        btn_s1.clicked.connect(self.guardar_g1)
        l_ctrls.addWidget(btn_s1)
        btn_l1 = self.boton_accion("📂")
        btn_l1.setToolTip("Cargar G₁")
        btn_l1.clicked.connect(self.cargar_g1)
        l_ctrls.addWidget(btn_l1)

        l_ctrls.addSpacing(10)

        self.btn_calc = self.boton_accion("+ SUMAR")
        self.btn_calc.setStyleSheet(
            self.btn_calc.styleSheet() +
            "QPushButton { background:#1b4332; min-width:100px; }")
        self.btn_calc.clicked.connect(self.calcular)
        l_ctrls.addWidget(self.btn_calc)

        btn_limpiar = self.boton_accion("🗑 Limpiar")
        btn_limpiar.clicked.connect(self.limpiar_todo)
        l_ctrls.addWidget(btn_limpiar)

        l_ctrls.addSpacing(10)

        # — G2 —
        lbl_g2 = QLabel("<b>G₂</b>")
        lbl_g2.setStyleSheet("color:#1b4332; font-size:14px;")
        l_ctrls.addWidget(lbl_g2)
        l_ctrls.addWidget(QLabel("V:"))
        self.sp2 = QSpinBox()
        self.sp2.setRange(1, 10)
        self.sp2.setValue(3)
        l_ctrls.addWidget(self.sp2)
        btn_c2 = self.boton_accion("Reiniciar")
        btn_c2.clicked.connect(self.crear_g2)
        l_ctrls.addWidget(btn_c2)
        btn_a2 = self.boton_accion("+ Arista")
        btn_a2.clicked.connect(self.agregar_a2)
        l_ctrls.addWidget(btn_a2)
        btn_d2 = self.boton_accion("− Arista")
        btn_d2.clicked.connect(self.eliminar_a2)
        l_ctrls.addWidget(btn_d2)
        btn_s2 = self.boton_accion("💾")
        btn_s2.setToolTip("Guardar G₂")
        btn_s2.clicked.connect(self.guardar_g2)
        l_ctrls.addWidget(btn_s2)
        btn_l2 = self.boton_accion("📂")
        btn_l2.setToolTip("Cargar G₂")
        btn_l2.clicked.connect(self.cargar_g2)
        l_ctrls.addWidget(btn_l2)

        l_ctrls.addStretch()
        layout.addWidget(ctrls)

        # ── Visualizadores ──────────────────────────────────────────────────
        self.vis_splitter = QSplitter(Qt.Horizontal)
        self.vis_splitter.setStyleSheet(
            "QSplitter::handle { background: #d8e3dc; width: 2px; }")

        self.vis1 = VisualizadorGrafo("Grafo G₁", self)
        self.vis2 = VisualizadorGrafo("Grafo G₂", self)
        self.vis_res = VisualizadorGrafo(
            "Resultado  G₁ + G₂", self, es_editable=False)

        for v in (self.vis1, self.vis2, self.vis_res):
            v.setStyleSheet(
                "background-color: white; border: 1px solid #d8e3dc; "
                "border-radius: 10px;")
            self.vis_splitter.addWidget(v)

        layout.addWidget(self.vis_splitter)

    # ── Estilo ───────────────────────────────────────────────────────────────
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

    # ── Crear grafos ─────────────────────────────────────────────────────────
    def crear_g1(self):
        self.grafo1_vertices = self.sp1.value()
        self.grafo1_aristas = []
        self.grafo1_etiquetas = {i: str(i + 1)
                                  for i in range(self.grafo1_vertices)}
        self.vis1.set_grafo(self.grafo1_vertices, [], self.grafo1_etiquetas)
        self.vis_res.set_grafo(0, [], {})

    def crear_g2(self):
        self.grafo2_vertices = self.sp2.value()
        self.grafo2_aristas = []
        self.grafo2_etiquetas = {i: str(i + 1)
                                  for i in range(self.grafo2_vertices)}
        self.vis2.set_grafo(self.grafo2_vertices, [], self.grafo2_etiquetas)
        self.vis_res.set_grafo(0, [], {})

    # ── Agregar aristas ──────────────────────────────────────────────────────
    def agregar_a1(self):
        if self.grafo1_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "Primero crea G₁.").exec()
            return
        dlg = DialogoArista(self.grafo1_vertices, self, self.grafo1_etiquetas)
        if dlg.exec():
            a = tuple(sorted(dlg.get_arista()))
            if a not in [tuple(sorted(x)) for x in self.grafo1_aristas]:
                self.grafo1_aristas.append(a)
                self.vis1.set_grafo(self.grafo1_vertices,
                                    self.grafo1_aristas, self.grafo1_etiquetas)

    def agregar_a2(self):
        if self.grafo2_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "Primero crea G₂.").exec()
            return
        dlg = DialogoArista(self.grafo2_vertices, self, self.grafo2_etiquetas)
        if dlg.exec():
            a = tuple(sorted(dlg.get_arista()))
            if a not in [tuple(sorted(x)) for x in self.grafo2_aristas]:
                self.grafo2_aristas.append(a)
                self.vis2.set_grafo(self.grafo2_vertices,
                                    self.grafo2_aristas, self.grafo2_etiquetas)

    # ── Eliminar aristas ─────────────────────────────────────────────────────
    def eliminar_a1(self):
        if not self.grafo1_aristas:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay aristas en G₁.").exec()
            return
        dlg = DialogoArista(self.grafo1_vertices, self, self.grafo1_etiquetas)
        if dlg.exec():
            a = tuple(sorted(dlg.get_arista()))
            norm = [tuple(sorted(x)) for x in self.grafo1_aristas]
            if a in norm:
                self.grafo1_aristas.pop(norm.index(a))
                self.vis1.set_grafo(self.grafo1_vertices,
                                    self.grafo1_aristas, self.grafo1_etiquetas)

    def eliminar_a2(self):
        if not self.grafo2_aristas:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay aristas en G₂.").exec()
            return
        dlg = DialogoArista(self.grafo2_vertices, self, self.grafo2_etiquetas)
        if dlg.exec():
            a = tuple(sorted(dlg.get_arista()))
            norm = [tuple(sorted(x)) for x in self.grafo2_aristas]
            if a in norm:
                self.grafo2_aristas.pop(norm.index(a))
                self.vis2.set_grafo(self.grafo2_vertices,
                                    self.grafo2_aristas, self.grafo2_etiquetas)

    # ── Guardar / Cargar ─────────────────────────────────────────────────────
    def _guardar(self, n, aristas, etiquetas, nombre):
        path, _ = QFileDialog.getSaveFileName(
            self, f"Guardar {nombre}", "", "JSON (*.json)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"vertices": n, "aristas": aristas,
                           "etiquetas": etiquetas}, f, indent=2)

    def _cargar(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Cargar grafo", "", "JSON (*.json)")
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

    def guardar_g1(self):
        if self.grafo1_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self, "G₁ está vacío.").exec()
            return
        self._guardar(self.grafo1_vertices, self.grafo1_aristas,
                      self.grafo1_etiquetas, "G₁")

    def cargar_g1(self):
        res = self._cargar()
        if res:
            self.grafo1_vertices, self.grafo1_aristas, self.grafo1_etiquetas = res
            self.sp1.setValue(self.grafo1_vertices)
            self.vis1.set_grafo(self.grafo1_vertices,
                                self.grafo1_aristas, self.grafo1_etiquetas)

    def guardar_g2(self):
        if self.grafo2_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self, "G₂ está vacío.").exec()
            return
        self._guardar(self.grafo2_vertices, self.grafo2_aristas,
                      self.grafo2_etiquetas, "G₂")

    def cargar_g2(self):
        res = self._cargar()
        if res:
            self.grafo2_vertices, self.grafo2_aristas, self.grafo2_etiquetas = res
            self.sp2.setValue(self.grafo2_vertices)
            self.vis2.set_grafo(self.grafo2_vertices,
                                self.grafo2_aristas, self.grafo2_etiquetas)

    # ── Limpiar ──────────────────────────────────────────────────────────────
    def limpiar_todo(self):
        self.grafo1_vertices = 0; self.grafo1_aristas = []; self.grafo1_etiquetas = {}
        self.grafo2_vertices = 0; self.grafo2_aristas = []; self.grafo2_etiquetas = {}
        self.vis1.set_grafo(0, [], {})
        self.vis2.set_grafo(0, [], {})
        self.vis_res.set_grafo(0, [], {})

    # ── Calcular Suma (Join) correcto ────────────────────────────────────────
    def calcular(self):
        if self.grafo1_vertices == 0 or self.grafo2_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "Crea ambos grafos antes de calcular.").exec()
            return

        n1 = self.grafo1_vertices
        n2 = self.grafo2_vertices
        n_res = n1 + n2

        # Construir etiquetas del resultado:
        # G1 conserva sus etiquetas con prefijo "G1:"
        # G2 obtiene índices desplazados, con prefijo "G2:"
        etiq_res = {}
        for i in range(n1):
            etiq_res[i] = self.grafo1_etiquetas.get(i, str(i + 1))
        for j in range(n2):
            etiq_res[n1 + j] = self.grafo2_etiquetas.get(j, str(j + 1)) + "'"

        aristas_res = set()

        # Aristas internas G1 (índices sin cambio)
        for a in self.grafo1_aristas:
            aristas_res.add(tuple(sorted([a[0], a[1]])))

        # Aristas internas G2 (índices desplazados +n1)
        for a in self.grafo2_aristas:
            aristas_res.add(tuple(sorted([n1 + a[0], n1 + a[1]])))

        # Aristas cruzadas: todos los V(G1) con todos los V(G2)
        for i in range(n1):
            for j in range(n2):
                aristas_res.add((i, n1 + j))

        self.vis_res.set_grafo(n_res, list(aristas_res), etiq_res)
        DialogoClave(0, "Suma calculada", "mensaje", self,
                     f"G₁ + G₂ — Join\n\n"
                     f"Vértices: {n_res}  ({n1} de G₁ + {n2} de G₂)\n"
                     f"Aristas: {len(aristas_res)}\n\n"
                     "Los vértices de G₂ llevan prima (') para diferenciarlos.").exec()
