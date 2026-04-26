from PySide6.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QVBoxLayout,
    QPushButton, QFrame, QStackedWidget
)
from PySide6.QtCore import Qt


_SIDEBAR_W = 260

_BTN_STYLE = """
QPushButton {
    background-color: #2d6a4f;
    color: white;
    padding-left: 25px;
    text-align: left;
    border: none;
    font-size: 15px;
    font-weight: 500;
}
QPushButton:hover { background-color: #40916c; }
"""
_BTN_ACTIVE = """
QPushButton {
    background-color: #52b788;
    color: white;
    padding-left: 25px;
    text-align: left;
    border-left: 5px solid #d8f3dc;
    font-size: 15px;
    font-weight: bold;
}
QPushButton:hover { background-color: #52b788; }
"""


class InterfazOperacionesGrafos(QWidget):
    """Submenú de Operaciones de Grafos con sidebar propio."""

    def __init__(self, main_window, anterior):
        super().__init__()
        self.main_window = main_window
        self.anterior = anterior
        self._btns = {}

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Sidebar ───────────────────────────────────────────────────────────
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setFixedWidth(_SIDEBAR_W)
        self.sidebar_frame.setStyleSheet(
            "background-color:#1b4332; border:none;")
        s = QVBoxLayout(self.sidebar_frame)
        s.setContentsMargins(0, 0, 0, 0)
        s.setSpacing(0)

        titulo = QLabel("OPERACIONES")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet(
            "color:white; font-size:19px; font-weight:bold; padding:28px 12px;")
        s.addWidget(titulo)

        sep = QFrame(); sep.setFixedHeight(2)
        sep.setStyleSheet("background:#2d6a4f;")
        s.addWidget(sep); s.addSpacing(4)

        items = [
            ("  ∩  Intersección",    self.abrir_int),
            ("  ∪  Unión",           self.abrir_uni),
            ("  +  Suma (Join)",     self.abrir_sum),
            ("  🤝  Fusión / Cont.", self.abrir_fus),
            ("  🛤️  Línea / Comp.", self.abrir_com),
            ("  □  Productos",       self.abrir_pro),
        ]
        for texto, func in items:
            btn = self._crear_boton(texto)
            btn.clicked.connect(
                lambda _, f=func, b=btn: (self._activar(b), f()))
            s.addWidget(btn)
            self._btns[texto] = btn

        s.addStretch()
        back = self._crear_boton("  ⬅  Volver")
        back.clicked.connect(self.regresar)
        s.addWidget(back)

        # ── Stack ─────────────────────────────────────────────────────────────
        self.local_stack = QStackedWidget()
        self.local_stack.setStyleSheet("background:#f0f7f4;")
        self.local_stack.addWidget(self._bienvenida())

        main_layout.addWidget(self.sidebar_frame)
        main_layout.addWidget(self.local_stack)

    # ── Helpers ──────────────────────────────────────────────────────────────
    def _crear_boton(self, texto):
        btn = QPushButton(texto)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(55)
        btn.setStyleSheet(_BTN_STYLE)
        return btn

    def _activar(self, btn):
        for b in self._btns.values():
            b.setStyleSheet(_BTN_STYLE)
        btn.setStyleSheet(_BTN_ACTIVE)

    def _bienvenida(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setAlignment(Qt.AlignCenter)
        v.setSpacing(16)
        lbl = QLabel("Operaciones sobre Grafos")
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-size:26px; font-weight:bold; color:#1b4332;")
        v.addWidget(lbl)
        desc = [
            "  ∩  Intersección de grafos",
            "  ∪  Unión de grafos",
            "  +  Suma (Join) de grafos",
            "  🤝  Fusión y Contracción",
            "  🛤️  Grafo Línea y Complemento",
            "  □  Productos y Composición",
        ]
        for d in desc:
            lbl2 = QLabel(d)
            lbl2.setAlignment(Qt.AlignCenter)
            lbl2.setStyleSheet("font-size:13px; color:#40916c;")
            v.addWidget(lbl2)
        return w

    def _cambiar_vista(self, widget):
        idx = self.local_stack.indexOf(widget)
        if idx == -1:
            idx = self.local_stack.addWidget(widget)
        self.local_stack.setCurrentIndex(idx)

    def regresar_a_menu(self):
        self.local_stack.setCurrentIndex(0)
        for b in self._btns.values():
            b.setStyleSheet(_BTN_STYLE)

    def regresar(self):
        self.main_window.cambiar_pantalla(self.anterior)

    # ── Abrir vistas ─────────────────────────────────────────────────────────
    def abrir_int(self):
        from .vista_interseccion import VistaInterseccion
        self._cambiar_vista(VistaInterseccion(self.main_window, self))

    def abrir_uni(self):
        from .vista_union import VistaUnion
        self._cambiar_vista(VistaUnion(self.main_window, self))

    def abrir_sum(self):
        from .vista_suma import VistaSuma
        self._cambiar_vista(VistaSuma(self.main_window, self))

    def abrir_fus(self):
        from .vista_fusion_contraccion import VistaFusionContraccion
        self._cambiar_vista(VistaFusionContraccion(self.main_window, self))

    def abrir_com(self):
        from .vista_linea_complemento import VistaLineaComplemento
        self._cambiar_vista(VistaLineaComplemento(self.main_window, self))

    def abrir_pro(self):
        from .vista_productos_composicion import VistaProductosComposicion
        self._cambiar_vista(VistaProductosComposicion(self.main_window, self))
