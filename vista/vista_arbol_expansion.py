"""
vista_arbol_expansion.py
Vista para Árbol de Expansión Mínima y Máxima.
Usa MinimaController / MaximaController para toda la lógica algorítmica.
Los atributos públicos expuestos para los controladores son:
  - vertices_spin     (QSpinBox)
  - visual_grafo      (VisualizadorGrafoNoDirigido) — grafo original
  - visual_arbol      (VisualizadorGrafoNoDirigido) — árbol resultante
  - info_text         (QTextEdit)
  - circuitos_text    (QTextEdit)
  - circuitos_fund_text (QTextEdit)
  - conjuntos_text    (QTextEdit)
  - matrices_text     (QTextEdit)
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSpinBox, QTextEdit, QTabWidget, QComboBox, QLineEdit
)
from PySide6.QtCore import Qt
from vista.visualizador_grafo_no_dirigido import VisualizadorGrafoNoDirigido


class VistaArbolExpansion(QWidget):

    def __init__(self, main_window, hub, modo="minimo"):
        super().__init__()
        self.main_window = main_window
        self.hub = hub
        self.modo = modo          # "minimo" | "maximo"

        # Instanciar el controlador correcto según el modo
        if modo == "minimo":
            from controlador.arboles.minimaController import MinimaController
            self.ctrl = MinimaController(self)
        else:
            from controlador.arboles.maximaController import MaximaController
            self.ctrl = MaximaController(self)

        self._build_ui()
        # Crear grafo inicial por defecto
        self.ctrl.crear_grafo()
        self._refresh_arista_combos()

    # ── Construcción de la UI ────────────────────────────────────────────────
    def _build_ui(self):
        titulo_str = "Mínima" if self.modo == "minimo" else "Máxima"
        color_acento = "#1b6a38" if self.modo == "minimo" else "#6a3b1b"

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 12, 15, 12)
        main_layout.setSpacing(10)

        ribbon = QFrame()
        ribbon.setFixedHeight(105)
        ribbon.setStyleSheet(f"""
            QFrame#ribbon {{ background-color: #f8faf9; border: 1px solid #d8e3dc; border-radius: 12px; }}
            QLabel {{ color: #1b4332; font-weight: bold; font-size: 10px; text-transform: uppercase; }}
            QSpinBox, QComboBox, QLineEdit {{
                background-color: white; color: #1b4332;
                border: 2px solid #e0e6e3; border-radius: 6px;
                padding: 4px; font-weight: bold; font-size: 12px;
            }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: black;
                selection-background-color: #2d6a4f;
                selection-color: white;
            }}
            QSpinBox:focus, QComboBox:focus, QLineEdit:focus {{ border-color: #2d6a4f; }}
            QPushButton {{
                background-color: #2d6a4f; color: white; font-weight: bold;
                border: none; border-radius: 8px; padding: 8px 15px; font-size: 11px;
            }}
            QPushButton:hover {{ background-color: #1b4332; }}
            QPushButton#btn_exec {{ 
                background-color: #1b4332; font-size: 13px; border-radius: 10px;
                padding: 10px 25px;
            }}
            QPushButton#btn_exec:hover {{ background-color: #081c15; }}
        """)
        ribbon.setObjectName("ribbon")
        r_lay = QHBoxLayout(ribbon)
        r_lay.setContentsMargins(30, 0, 30, 0); r_lay.setSpacing(20)

        # --- Definición de Widgets ---
        btn_back = QPushButton("⬅ VOLVER")
        btn_back.setFixedWidth(80); btn_back.clicked.connect(lambda: self.main_window.cambiar_pantalla(self.hub))
        
        self.vertices_spin = QSpinBox(); self.vertices_spin.setRange(2, 15); self.vertices_spin.setValue(4); self.vertices_spin.setFixedWidth(50)
        btn_crear = QPushButton("↺ CREAR"); btn_crear.setFixedWidth(100); btn_crear.clicked.connect(self._crear_grafo_inline)
        
        self.cb_nom = QComboBox(); self.cb_nom.setFixedWidth(60); self.cb_nom.addItems(["123", "ABC", "abc"])
        self.cb_nom.currentIndexChanged.connect(self._refresh_arista_combos)
        
        self.cb_orig = QComboBox(); self.cb_orig.setFixedWidth(70); self.cb_orig.setEditable(True)
        self.cb_dest = QComboBox(); self.cb_dest.setFixedWidth(70); self.cb_dest.setEditable(True)
        self.peso_edit = QLineEdit("1"); self.peso_edit.setFixedWidth(50)
        
        btn_add = QPushButton("➕ AGREGAR"); btn_add.setFixedWidth(100); btn_add.clicked.connect(self._add_arista_inline)
        self.btn_del = QPushButton("🗑️ ELIMINAR"); self.btn_del.setFixedWidth(100)
        self.btn_del.clicked.connect(self._del_seleccion_inline)
        
        btn_limpiar = QPushButton("🧹 LIMPIAR"); btn_limpiar.setFixedWidth(100); btn_limpiar.clicked.connect(self._limpiar_inline)
        
        btn_save_full = QPushButton("💾 GUARDAR"); btn_save_full.setFixedWidth(100); btn_save_full.clicked.connect(self.ctrl.guardar_grafo)
        btn_load_full = QPushButton("📂 RECUPERAR"); btn_load_full.setFixedWidth(100); btn_load_full.clicked.connect(self._cargar_grafo_inline)

        btn_exec = QPushButton(f"⚡ EXPANSIÓN {titulo_str.upper()}")
        btn_exec.setObjectName("btn_exec"); btn_exec.clicked.connect(self.ctrl.ejecutar_algoritmo)

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
        v_row = QHBoxLayout(); v_row.addWidget(lbl_ver); v_row.addWidget(self.vertices_spin)
        b_row = QHBoxLayout(); b_row.addWidget(btn_crear); b_row.addWidget(btn_limpiar)
        grafo_lay.addLayout(v_row); grafo_lay.addLayout(b_row)

        # 3. Grupo Edición
        edit_lay = QVBoxLayout()
        lbl_de = QLabel("📍 De"); lbl_de.setFixedWidth(40)
        lbl_a = QLabel("➜ A"); lbl_a.setFixedWidth(40)
        lbl_p = QLabel("⚖️ Peso"); lbl_p.setFixedWidth(50)
        edit_top = QHBoxLayout(); edit_top.addWidget(lbl_de); edit_top.addWidget(self.cb_orig)
        edit_top.addWidget(lbl_a); edit_top.addWidget(self.cb_dest)
        edit_top.addWidget(lbl_p); edit_top.addWidget(self.peso_edit)
        edit_bot = QHBoxLayout(); edit_bot.addWidget(btn_add); edit_bot.addWidget(self.btn_del)
        edit_lay.addLayout(edit_top); edit_lay.addLayout(edit_bot)

        # 4. Grupo Archivos
        file_lay = QVBoxLayout()
        file_lay.addWidget(btn_save_full); file_lay.addWidget(btn_load_full)

        r_lay.addStretch(1)
        r_lay.addLayout(nav_lay)
        r_lay.addStretch(1)
        r_lay.addWidget(create_sep())
        r_lay.addStretch(1)
        r_lay.addLayout(grafo_lay)
        r_lay.addStretch(1)
        r_lay.addWidget(create_sep())
        r_lay.addStretch(1)
        r_lay.addLayout(edit_lay)
        r_lay.addStretch(1)
        r_lay.addWidget(create_sep())
        r_lay.addStretch(1)
        r_lay.addLayout(file_lay)
        r_lay.addStretch(2)
        r_lay.addWidget(btn_exec)
        r_lay.addStretch(1)

        main_layout.addWidget(ribbon)

        # ── Cuerpo: grafos + resultados ──────────────────────────────────────
        body = QHBoxLayout()
        body.setSpacing(10)

        # Panel izquierdo: dos visualizadores apilados
        viz_frame = QFrame()
        viz_frame.setStyleSheet(
            "background:white; border:1px solid #d8e3dc; border-radius:10px;")
        viz_lay = QVBoxLayout(viz_frame)
        viz_lay.setContentsMargins(10, 10, 10, 10)
        viz_lay.setSpacing(6)

        lbl_orig = QLabel("🗺️  GRAFO ORIGINAL")
        lbl_orig.setStyleSheet("color:#1b4332; font-weight:bold; font-size:13px;")
        viz_lay.addWidget(lbl_orig)
        self.visual_grafo = VisualizadorGrafoNoDirigido("Original")
        viz_lay.addWidget(self.visual_grafo, stretch=1)

        sep_h = QFrame(); sep_h.setFrameShape(QFrame.HLine)
        sep_h.setStyleSheet("color:#d8e3dc;"); viz_lay.addWidget(sep_h)

        lbl_arb = QLabel(f"🌳  ÁRBOL DE EXPANSIÓN {titulo_str.upper()}")
        lbl_arb.setStyleSheet("color:#2d6a4f; font-weight:bold; font-size:13px;")
        viz_lay.addWidget(lbl_arb)
        self.visual_arbol = VisualizadorGrafoNoDirigido("Árbol")
        viz_lay.addWidget(self.visual_arbol, stretch=1)

        body.addWidget(viz_frame, stretch=2)

        # Panel derecho: tabs de resultados
        res_frame = QFrame()
        res_frame.setStyleSheet(
            "background:white; border:1px solid #d8e3dc; border-radius:10px;")
        res_lay = QVBoxLayout(res_frame)
        res_lay.setContentsMargins(8, 8, 8, 8)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border:1px solid #d8e3dc; background:white; }
            QTabBar::tab { background:#f0f7f4; padding:7px 11px;
                           color:#1b4332; font-weight:bold; border-top-left-radius:6px; }
            QTabBar::tab:selected { background:white; color:#2d6a4f; }
        """)

        self.info_text         = self._txt()
        self.circuitos_text    = self._txt()
        self.circuitos_fund_text = self._txt()
        self.conjuntos_text    = self._txt()
        self.matrices_text     = self._txt()

        self.tabs.addTab(self.info_text,          "📊 General")
        self.tabs.addTab(self.circuitos_text,     "🔄 Circuitos")
        self.tabs.addTab(self.circuitos_fund_text,"🔗 C. Fund.")
        self.tabs.addTab(self.conjuntos_text,     "✂️ Cortes")
        self.tabs.addTab(self.matrices_text,      "🔢 Matrices")

        res_lay.addWidget(self.tabs)
        body.addWidget(res_frame, stretch=1)

        main_layout.addLayout(body, stretch=1)

    # ── Helpers para el controlador ──────────────────────────────────────────
    def _txt(self):
        t = QTextEdit()
        t.setReadOnly(True)
        t.setStyleSheet("border:none; font-family:'Segoe UI',sans-serif; font-size:13px;")
        return t

    # ── Métodos inline de gestión de aristas ────────────────────────────────
    def _refresh_arista_combos(self):
        """Actualiza los combo boxes de origen/destino y las etiquetas del visualizador basándose en la nomenclatura."""
        self.cb_orig.clear(); self.cb_dest.clear()
        modo = self.cb_nom.currentText()
        n = self.ctrl.vertices
        self.ctrl.etiquetas = {}
        for i in range(n):
            if modo == "ABC":
                label, t = "", i
                while t >= 0: label = chr(65 + (t % 26)) + label; t = (t // 26) - 1
                self.ctrl.etiquetas[i] = label
            elif modo == "abc":
                label, t = "", i
                while t >= 0: label = chr(97 + (t % 26)) + label; t = (t // 26) - 1
                self.ctrl.etiquetas[i] = label
            else: self.ctrl.etiquetas[i] = str(i + 1)
        
        labs = [self.ctrl.etiquetas[i] for i in range(n)]
        self.cb_orig.addItems(labs); self.cb_dest.addItems(labs)
        self.ctrl._refresh_visual_grafo()

    def _crear_grafo_inline(self):
        self.ctrl.crear_grafo()
        self._refresh_arista_combos()

    def _add_arista_inline(self):
        if self.ctrl.vertices == 0:
            return
        u = self.cb_orig.currentIndex()
        v = self.cb_dest.currentIndex()
        if u < 0 or v < 0 or u == v:
            return
        try:
            peso = float(self.peso_edit.text().replace(',', '.'))
        except ValueError:
            peso = 1.0
        arista = tuple(sorted([u, v]))
        if arista not in self.ctrl.aristas:
            self.ctrl.aristas.append(arista)
        self.ctrl.ponderaciones[arista] = peso
        self.ctrl._refresh_visual_grafo()

    def _del_seleccion_inline(self):
        sel = self.visual_grafo.objeto_seleccionado
        if sel:
            tipo, idx = sel
            if tipo == 'vertice':
                if self.ctrl.vertices > 2:
                    self.vertices_spin.setValue(self.ctrl.vertices - 1)
                    self._crear_grafo_inline()
            elif tipo == 'arista':
                if 0 <= idx < len(self.ctrl.aristas):
                    a = self.ctrl.aristas.pop(idx)
                    self.ctrl.ponderaciones.pop(a, None)
                    self.visual_grafo.objeto_seleccionado = None
                    self.ctrl._refresh_visual_grafo()
        else:
            # Fallback a borrar por combos si no hay selección
            u = self.cb_orig.currentIndex()
            v = self.cb_dest.currentIndex()
            arista = tuple(sorted([u, v]))
            if arista in self.ctrl.aristas:
                self.ctrl.aristas.remove(arista)
                self.ctrl.ponderaciones.pop(arista, None)
                self.ctrl._refresh_visual_grafo()

    def _limpiar_inline(self):
        self.ctrl.limpiar_grafo()
        self._refresh_arista_combos()

    def _cargar_grafo_inline(self):
        self.ctrl.cargar_grafo()
        self._refresh_arista_combos()
