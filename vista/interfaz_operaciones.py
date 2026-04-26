from PySide6.QtGui import QPainter, QPen, QColor, QFont, QBrush, QPainterPath
import math
import json
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QGroupBox, QTextEdit, QInputDialog, QComboBox,
    QGridLayout, QFileDialog, QMessageBox, QScrollArea, QFrame
)
from PySide6.QtCore import Qt, QPointF

# --- Clases LienzoGrafo y GrafoInteractivo se mantienen igual ---

class LienzoGrafo(QWidget):
    def __init__(self, color_tema="#2d6a4f"):
        super().__init__()
        self.nodos = []
        self.aristas = {} 
        self.posiciones = {}
        self.color_tema = color_tema
        self.nodo_arrastrando = None
        self.objeto_seleccionado = None # ('vertice', nombre) o ('arista', key)
        self.setMouseTracking(True)

    def actualizar(self, nodos, aristas):
        nuevos_nodos = [str(n) for n in nodos]
        cambio = (nuevos_nodos != self.nodos)
        self.nodos = nuevos_nodos
        self.aristas = {}
        for k, v in aristas.items():
            if len(k) >= 2:
                self.aristas[(str(k[0]), str(k[1]), k[2] if len(k)>2 else v)] = v
        
        if cambio or not self.posiciones:
            self.inicializar_posiciones()
        self.update()

    def inicializar_posiciones(self):
        if not self.nodos: return
        centro = QPointF(self.width() / 2, self.height() / 2)
        if centro.x() < 50: centro = QPointF(300, 200)
        radio = min(self.width(), self.height()) * 0.38
        if radio < 50: radio = 150
        
        angulo_paso = 2 * math.pi / len(self.nodos)
        for i, nombre in enumerate(self.nodos):
            x = centro.x() + radio * math.cos(i * angulo_paso)
            y = centro.y() + radio * math.sin(i * angulo_paso)
            self.posiciones[nombre] = QPointF(x, y)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos_mouse = event.position()
            # 1. Detectar Vértices
            for nombre, pos in self.posiciones.items():
                if (pos - pos_mouse).manhattanLength() < 25:
                    self.nodo_arrastrando = nombre
                    self.objeto_seleccionado = ('vertice', nombre)
                    self.setCursor(Qt.ClosedHandCursor)
                    self.update()
                    return

            # 2. Detectar Aristas
            for key in self.aristas.keys():
                n1, n2 = key[0], key[1]
                if n1 in self.posiciones and n2 in self.posiciones:
                    p1, p2 = self.posiciones[n1], self.posiciones[n2]
                    if self._distancia_punto_segmento(pos_mouse, p1, p2) < 10:
                        self.objeto_seleccionado = ('arista', key)
                        self.update()
                        return

            # 3. Click en vacío
            self.objeto_seleccionado = None
            self.update()

    def _distancia_punto_segmento(self, p, a, b):
        px, py = p.x(), p.y()
        ax, ay = a.x(), a.y()
        bx, by = b.x(), b.y()
        l2 = (ax - bx)**2 + (ay - by)**2
        if l2 == 0: return math.sqrt((px-ax)**2 + (py-ay)**2)
        t = max(0, min(1, ((px - ax) * (bx - ax) + (py - ay) * (by - ay)) / l2))
        proj_x = ax + t * (bx - ax)
        proj_y = ay + t * (by - ay)
        return math.sqrt((px - proj_x)**2 + (py - proj_y)**2)

    def mouseMoveEvent(self, event):
        if self.nodo_arrastrando:
            self.posiciones[self.nodo_arrastrando] = event.position()
            self.update()
        else:
            sobre = False
            for pos in self.posiciones.values():
                if (pos - event.position()).manhattanLength() < 20:
                    sobre = True; break
            if sobre: self.setCursor(Qt.PointingHandCursor)
            else: self.unsetCursor()

    def mouseReleaseEvent(self, event):
        self.nodo_arrastrando = None
        self.unsetCursor()

    def paintEvent(self, event):
        if not self.posiciones and self.nodos:
            self.inicializar_posiciones()
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor("#f8faf9"))

        if not self.nodos: return
        
        aristas_dibujadas = {} 
        for key, nombre_e in self.aristas.items():
            n1, n2 = key[0], key[1]
            if n1 in self.posiciones and n2 in self.posiciones:
                p1, p2 = self.posiciones[n1], self.posiciones[n2]
                painter.setPen(QPen(QColor(self.color_tema), 2))
                
                if n1 == n2:
                    painter.drawEllipse(p1.x() - 15, p1.y() - 40, 30, 30)
                else:
                    par = tuple(sorted((n1, n2)))
                    aristas_dibujadas[par] = aristas_dibujadas.get(par, 0) + 1
                    num = aristas_dibujadas[par]
                    
                    es_sel = (self.objeto_seleccionado == ('arista', key))
                    color = QColor("#ff4d4d") if es_sel else QColor(self.color_tema)
                    ancho = 4 if es_sel else 2
                    painter.setPen(QPen(color, ancho))

                    path = QPainterPath()
                    path.moveTo(p1)
                    if num > 1:
                        mid = (p1 + p2) / 2
                        dx, dy = p2.x() - p1.x(), p2.y() - p1.y()
                        dist = math.sqrt(dx**2 + dy**2) or 1
                        offset = 25 * (num - 1) 
                        path.quadTo(QPointF(mid.x() - (dy/dist)*offset, mid.y() + (dx/dist)*offset), p2)
                    else:
                        path.lineTo(p2)
                    painter.drawPath(path)

        painter.setFont(QFont("Arial", 8, QFont.Bold))
        for nombre, pos in self.posiciones.items():
            es_sel = (self.objeto_seleccionado == ('vertice', nombre))
            color_borde = QColor("#ff4d4d") if es_sel else QColor("#1b4332")
            ancho_borde = 4 if es_sel else 2

            r = 18 if len(nombre) > 2 else 14
            painter.setPen(QPen(color_borde, ancho_borde))
            painter.setBrush(QBrush(QColor("white")))
            painter.drawEllipse(pos, r, r)
            painter.setPen(QColor("black"))
            painter.drawText(pos.x() - (len(nombre)*3), pos.y() + 4, nombre)

class GrafoInteractivo(QGroupBox):
    def __init__(self, titulo):
        super().__init__(titulo)
        self.setStyleSheet("""
            QGroupBox { color: #1b4332; font-weight: bold; border: 2px solid #2d6a4f; margin-top: 5px; background: white; border-radius: 8px; }
            QPushButton { border-radius: 4px; font-weight: bold; padding: 4px; background-color: #2d6a4f; color: white; }
            QPushButton:hover { background-color: #1b4332; }
            QComboBox QAbstractItemView {
                background-color: white; color: black;
                selection-background-color: #2d6a4f; selection-color: white;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 15, 5, 5); layout.setSpacing(10)
        grid = QGridLayout()
        grid.setSpacing(5)

        self.txt_cant = QLineEdit(); self.txt_cant.setPlaceholderText("Cant."); self.txt_cant.setFixedWidth(50)
        btn_gen = QPushButton("⚡ GEN"); btn_gen.clicked.connect(self.generar_auto)
        btn_gen.setFixedWidth(60); btn_gen.setStyleSheet("background-color: #1b4332; color: white;")
        
        self.cb_nom = QComboBox(); self.cb_nom.setFixedWidth(60)
        self.cb_nom.addItems(["123", "ABC", "abc"])
        self.cb_nom.currentIndexChanged.connect(self.actualizar_nomenclatura)

        self.cb_n1 = QComboBox(); self.cb_n1.setMinimumWidth(55)
        self.cb_n2 = QComboBox(); self.cb_n2.setMinimumWidth(55)
        btn_con = QPushButton("➕"); btn_con.clicked.connect(self.conectar)
        btn_con.setStyleSheet("background-color: #2d6a4f; color: white; border-radius: 4px; padding: 4px;")
        
        btn_del = QPushButton("🗑️ ELIMINAR SELECCION"); btn_del.setObjectName("btn_delete")
        btn_del.setStyleSheet("background-color: #2d6a4f; color: white; font-size: 10px;")
        btn_del.clicked.connect(self.eliminar_seleccionado)
        
        grid.addWidget(QLabel("📏"), 0, 0); grid.addWidget(self.txt_cant, 0, 1); grid.addWidget(btn_gen, 0, 2)
        grid.addWidget(QLabel("🔤"), 0, 3); grid.addWidget(self.cb_nom, 0, 4)
        
        grid.addWidget(QLabel("📍"), 1, 0); grid.addWidget(self.cb_n1, 1, 1); grid.addWidget(self.cb_n2, 1, 2)
        grid.addWidget(btn_con, 1, 3); grid.addWidget(btn_del, 1, 4)
        
        layout.addLayout(grid)
        self.lienzo = LienzoGrafo(); layout.addWidget(self.lienzo, stretch=1)
        self.nodos = []; self.aristas = {}

    def generar_auto(self):
        try:
            n = int(self.txt_cant.text())
            self.nodos = [str(i+1) for i in range(n)] # Temporales, se cambian en actualizar_nomenclatura
            self.aristas = {}; self.actualizar_nomenclatura()
        except: pass

    def actualizar_nomenclatura(self):
        modo = self.cb_nom.currentText()
        num = len(self.nodos)
        nuevos_nodos = []
        mapping = {}
        for i in range(num):
            if modo == "ABC":
                label, t = "", i
                while t >= 0: label = chr(65 + (t % 26)) + label; t = (t // 26) - 1
                mapping[self.nodos[i]] = label
                nuevos_nodos.append(label)
            elif modo == "abc":
                label, t = "", i
                while t >= 0: label = chr(97 + (t % 26)) + label; t = (t // 26) - 1
                mapping[self.nodos[i]] = label
                nuevos_nodos.append(label)
            else:
                label = str(i+1)
                mapping[self.nodos[i]] = label
                nuevos_nodos.append(label)
        
        # Actualizar aristas con nuevo mapeo
        nuevas_aristas = {}
        for k, v in self.aristas.items():
            u, v_old, e_lbl = k[0], k[1], k[2]
            nuevas_aristas[(mapping.get(u, u), mapping.get(v_old, v_old), e_lbl)] = v
        
        self.nodos = nuevos_nodos
        self.aristas = nuevas_aristas
        self.actualizar()

    def conectar(self):
        n1, n2 = self.cb_n1.currentText(), self.cb_n2.currentText()
        if n1 and n2:
            key = (n1, n2, f"e{len(self.aristas)+1}")
            self.aristas[key] = f"e{len(self.aristas)+1}"
            self.actualizar()

    def eliminar_seleccionado(self):
        sel = self.lienzo.objeto_seleccionado
        if not sel: return
        tipo, id_obj = sel
        if tipo == 'vertice':
            if id_obj in self.nodos:
                self.nodos.remove(id_obj)
                # Eliminar aristas conectadas
                self.aristas = {k: v for k, v in self.aristas.items() if k[0] != id_obj and k[1] != id_obj}
                self.lienzo.objeto_seleccionado = None
                self.actualizar()
        elif tipo == 'arista':
            if id_obj in self.aristas:
                del self.aristas[id_obj]
                self.lienzo.objeto_seleccionado = None
                self.actualizar()

    def actualizar(self):
        self.cb_n1.clear(); self.cb_n2.clear()
        self.cb_n1.addItems(self.nodos); self.cb_n2.addItems(self.nodos)
        self.lienzo.actualizar(self.nodos, self.aristas)

class InterfazOperaciones(QWidget):
    def __init__(self, main_window, anterior):
        super().__init__()
        self.main_window = main_window
        self.anterior = anterior

        self.layout_principal = QHBoxLayout(self)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)

        # ---------- SIDEBAR ----------
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(330)
        self.sidebar.setStyleSheet("background-color: #1b4332;")
        s_layout = QVBoxLayout(self.sidebar)
        s_layout.setContentsMargins(0, 0, 0, 0); s_layout.setSpacing(0)

        titulo_sidebar = QLabel("OPERACIONES")
        titulo_sidebar.setAlignment(Qt.AlignCenter)
        titulo_sidebar.setStyleSheet("color:white; font-size:24px; font-weight:bold; padding:40px 20px;")
        s_layout.addWidget(titulo_sidebar)

        # Scroll Area para botones si hay muchos
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("background: transparent;")
        self.botones_layout = QVBoxLayout(scroll_widget)
        self.botones_layout.setContentsMargins(10, 10, 10, 10); self.botones_layout.setSpacing(8)

        opciones = [
            "Intersección", "Unión", "Suma de anillos", "Fusión de vertices", 
            "Eliminación de vértices", "Contracción de aristas",
            "Grafo Complementario", "Grafo Línea", "Producto Cartesiano",
            "Producto Tensorial", "Composición"
        ]
        for op in opciones:
            btn = self.crear_boton(f"🧩  {op}")
            btn.clicked.connect(lambda checked=False, name=op: self.cambiar_contenido(name))
            self.botones_layout.addWidget(btn)

        scroll.setWidget(scroll_widget)
        s_layout.addWidget(scroll)

        btn_volver = self.crear_boton("⬅  Volver")
        btn_volver.clicked.connect(self.regresar)
        s_layout.addSpacing(20); s_layout.addWidget(btn_volver); s_layout.addStretch()

        # ---------- CONTENIDO DERECHA ----------
        self.contenido = QWidget()
        self.contenido.setStyleSheet("background-color: #f0f7f4;")
        layout_cont = QVBoxLayout(self.contenido)
        layout_cont.setContentsMargins(20, 20, 20, 20); layout_cont.setSpacing(10)

        header = QHBoxLayout()
        self.lbl_titulo = QLabel("Seleccione una operación")
        self.lbl_titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #1b4332;")
        header.addWidget(self.lbl_titulo); header.addStretch()
        layout_cont.addLayout(header)

        self.row_grafos = QHBoxLayout()
        self.g1 = GrafoInteractivo("G1")
        self.g2 = GrafoInteractivo("G2")
        self.row_grafos.addWidget(self.g1); self.row_grafos.addWidget(self.g2)
        layout_cont.addLayout(self.row_grafos, stretch=3)

        self.btn_calc = QPushButton("⚡ SELECCIONE OPERACIÓN")
        self.btn_calc.setFixedHeight(55)
        self.btn_calc.setStyleSheet("""
            QPushButton { 
                background: #1b4332; color: white; font-size: 14px; 
                font-weight: bold; border-radius: 12px; border: 2px solid #2d6a4f;
            }
            QPushButton:hover { background: #081c15; border-color: #40916c; }
            QComboBox QAbstractItemView {
                background-color: white; color: black;
                selection-background-color: #2d6a4f; selection-color: white;
            }
        """)
        self.btn_calc.clicked.connect(self.ejecutar)
        layout_cont.addWidget(self.btn_calc)

        res_lay = QHBoxLayout()
        self.g_res = LienzoGrafo(color_tema="#40916c")
        self.res_txt = QTextEdit(); self.res_txt.setReadOnly(True); self.res_txt.setMaximumWidth(250)
        res_lay.addWidget(self.g_res, stretch=2); res_lay.addWidget(self.res_txt, stretch=1)
        layout_cont.addLayout(res_lay, stretch=2)

        self.layout_principal.addWidget(self.sidebar)
        self.layout_principal.addWidget(self.contenido)

    def crear_boton(self, texto):
        btn = QPushButton(texto)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(50)
        btn.setStyleSheet("""
            QPushButton { 
                background-color: #2d6a4f; color: white; padding-left: 20px; 
                text-align: left; border: none; font-size: 13px; font-weight: bold;
                border-radius: 8px; margin: 0 5px;
            }
            QPushButton:hover { background-color: #40916c; margin-left: 10px; }
        """)
        return btn

    def regresar(self):
        self.main_window.cambiar_pantalla(self.anterior)

    def cambiar_contenido(self, nombre):
        self.lbl_titulo.setText(f"Operación: {nombre}")
        self.btn_calc.setText(f"⚡ CALCULAR {nombre.upper()}")
        single = ["complement", "línea", "linea", "fusión", "fusion", "eliminación", "eliminacion", "contracción", "contraccion"]
        is_single = any(x in nombre.lower() for x in single)
        self.g2.setVisible(not is_single)
        self.g_res.actualizar([], {})
        self.res_txt.clear()

    def ejecutar(self):
        tipo = self.lbl_titulo.text().lower()
        if "seleccione" in tipo: return
        
        self.btn_calc.setStyleSheet("background: #1b4332; color: white; font-size: 16px; font-weight: bold; border-radius: 8px;") # Cambio a verde oscuro al presionar? o solo fijo
        # En realidad btn_calc ya tiene estilo en el init.
        
        v1, e1 = self.g1.nodos, self.g1.aristas
        v2, e2 = self.g2.nodos, self.g2.aristas
        
        v_res, e_res, msg = [], {}, ""

        if "intersección" in tipo or "interseccion" in tipo:
            v_res = sorted(list(set(v1) & set(v2)))
            set_e2 = set((k[0], k[1]) for k in e2.keys())
            for k, v in e1.items():
                if (k[0], k[1]) in set_e2 and k[0] in v_res and k[1] in v_res:
                    e_res[k] = v
            msg = "Intersección realizada."

        elif "unión" in tipo or "union" in tipo:
            v_res = sorted(list(set(v1) | set(v2)))
            e_res = {**e1, **e2}
            msg = "Unión realizada."

        elif "suma de anillos" in tipo:
            v_res = sorted(list(set(v1) | set(v2)))
            set_e1 = set((k[0], k[1]) for k in e1.keys())
            set_e2 = set((k[0], k[1]) for k in e2.keys())
            diff = (set_e1 | set_e2) - (set_e1 & set_e2)
            for k, v in {**e1, **e2}.items():
                if (k[0], k[1]) in diff: e_res[k] = v
            msg = "Suma de anillos."

        elif "complement" in tipo:
            v_res = v1
            exist = set()
            for k in e1.keys(): exist.add(tuple(sorted((k[0], k[1]))))
            idx = 1
            for i in range(len(v1)):
                for j in range(i+1, len(v1)):
                    if tuple(sorted((v1[i], v1[j]))) not in exist:
                        e_res[(v1[i], v1[j], f"ec{idx}")] = f"ec{idx}"; idx += 1
            msg = "Grafo Complementario."

        elif "línea" in tipo or "linea" in tipo:
            v_res = [f"{k[0]}-{k[1]}" for k in e1.keys()]
            keys = list(e1.keys())
            for i in range(len(keys)):
                for j in range(i+1, len(keys)):
                    k1, k2 = keys[i], keys[j]
                    if k1[0] in [k2[0], k2[1]] or k1[1] in [k2[0], k2[1]]:
                        e_res[(v_res[i], v_res[j], f"el{i}-{j}")] = ""
            msg = "Grafo de Línea."

        elif "cartesiano" in tipo:
            v_res = [f"({u},{v})" for u in v1 for v in v2]
            for u in v1:
                for k2 in e2.keys(): e_res[(f"({u},{k2[0]})", f"({u},{k2[1]})", "")] = ""
            for v in v2:
                for k1 in e1.keys(): e_res[(f"({k1[0]},{v})", f"({k1[1]},{v})", "")] = ""
            msg = "Producto Cartesiano."

        elif "tensorial" in tipo:
            v_res = [f"({u},{v})" for u in v1 for v in v2]
            for k1 in e1.keys():
                for k2 in e2.keys():
                    e_res[(f"({k1[0]},{k2[0]})", f"({k1[1]},{k2[1]})", "")] = ""
                    e_res[(f"({k1[0]},{k2[1]})", f"({k1[1]},{k2[0]})", "")] = ""
            msg = "Producto Tensorial."

        elif "composición" in tipo or "composicion" in tipo:
            v_res = [f"({u},{v})" for u in v1 for v in v2]
            for k1 in e1.keys():
                for v_a in v2:
                    for v_b in v2: e_res[(f"({k1[0]},{v_a})", f"({k1[1]},{v_b})", "")] = ""
            for u in v1:
                for k2 in e2.keys(): e_res[(f"({u},{k2[0]})", f"({u},{k2[1]})", "")] = ""
            msg = "Composición."

        self.g_res.actualizar(v_res, e_res)
        self.res_txt.setText(f"{msg}\n\nV: {len(v_res)}\nE: {len(e_res)}\n\nNodos: {v_res}")