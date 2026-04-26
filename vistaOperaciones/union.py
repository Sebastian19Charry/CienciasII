import math
import json
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, 
    QGraphicsTextItem, QGraphicsLineItem, QGraphicsPathItem, 
    QInputDialog, QMessageBox, QFrame
)
from PySide6.QtGui import (
    QBrush, QPen, QColor, QPainter, QPainterPath, QPainterPathStroker
)
from PySide6.QtCore import Qt, QLineF, QPointF, QRectF

# --- Vértice Interactivo ---
class VerticeVisual(QGraphicsEllipseItem):
    def __init__(self, x, y, nombre, editor_parent, movible=True):
        self.radio = 20
        super().__init__(-self.radio, -self.radio, self.radio*2, self.radio*2)
        self.setPos(x, y)
        self.editor_parent = editor_parent
        self.nombre = nombre
        
        self.setBrush(QBrush(QColor("#2d6a4f")))
        self.setPen(QPen(Qt.black, 2))
        self.setZValue(2)
        
        flags = QGraphicsEllipseItem.ItemIsSelectable | QGraphicsEllipseItem.ItemSendsGeometryChanges
        if movible:
            flags |= QGraphicsEllipseItem.ItemIsMovable
        self.setFlags(flags)
        
        self.texto = QGraphicsTextItem(nombre, self)
        self.texto.setPos(-12, -10)
        self.texto.setDefaultTextColor(Qt.white)

    def mouseDoubleClickEvent(self, event):
        if self.flags() & QGraphicsEllipseItem.ItemIsMovable:
            nuevo_nombre, ok = QInputDialog.getText(None, "Renombrar", "Nuevo nombre:", text=self.nombre)
            if ok and nuevo_nombre:
                self.nombre = nuevo_nombre
                self.texto.setPlainText(nuevo_nombre)
                self.editor_parent.actualizar_aristas()

    def itemChange(self, change, value):
        if change == QGraphicsEllipseItem.ItemPositionHasChanged:
            self.editor_parent.actualizar_aristas()
        elif change == QGraphicsEllipseItem.ItemSelectedChange:
            if value:
                self.setPen(QPen(QColor("#fb8500"), 3)) # Naranja para selección
            else:
                self.setPen(QPen(Qt.black, 2))
        return super().itemChange(change, value)

# --- Arista Interactiva ---
class AristaVisual(QGraphicsPathItem): # <-- CAMBIAMOS LA HERENCIA: De QGraphicsLineItem a QGraphicsPathItem
    def __init__(self, v1, v2, nombre, editable=True):
        super().__init__()
        self.v1 = v1
        self.v2 = v2
        self.nombre = nombre
        self.editable = editable

        # Configuramos el estilo inicial de la línea
        # He puesto un gris por defecto, puedes usar el que tenías
        # Asegúrate de usar QPen(QColor("..."), grosor)
        self.setPen(QPen(QColor("#7f8c8d"), 1))
        # Esto hace que el borde sea suave
        self.setFlag(QGraphicsPathItem.ItemIsSelectable)
        self.setFlag(QGraphicsPathItem.ItemSendsGeometryChanges)

        self.texto_item = QGraphicsTextItem(self)
        self.texto_item.setPlainText(self.nombre)
        self.texto_item.setDefaultTextColor(Qt.black)
        # Hacemos que el texto sea un poco más grande
        # fuente = self.texto_item.font()
        # fuente.setPointSize(8)
        # self.texto_item.setFont(fuente)

        self.actualizar_posicion()

    def shape(self):
        # Facilita la selección de la arista dando un área de clic más ancha
        stroker = QPainterPathStroker()
        stroker.setWidth(10)
        return stroker.createStroke(self.path())

    def itemChange(self, change, value):
        if change == QGraphicsPathItem.ItemSelectedChange:
            if value:
                self.setPen(QPen(QColor("#fb8500"), 3)) # Naranja para selección
            else:
                self.setPen(QPen(QColor("#7f8c8d"), 1))
        return super().itemChange(change, value)

    # ESTA ES LA NUEVA LÓGICA DE DIBUJO QUE REEMPLAZA A LA ANTERIOR
    def actualizar_posicion(self):
        # Creamos un objeto QPainterPath para definir el dibujo
        path = QPainterPath()

        if self.v1 == self.v2:
            # --- LÓGICA PARA BUCLES (FUSIÓN) - AHORA ES UN CIRCULO VERDADERO ---
            v_x = self.v1.pos().x()
            v_y = self.v1.pos().y()
            radius = 15 # Radio del vértice
            
            # Definimos el rectángulo para el bucle
            # p1 y p2 definen la caja que contiene la elipse
            p1 = QPointF(v_x - 15, v_y - 45) # Caja desplazada hacia arriba
            p2 = QPointF(v_x + 15, v_y - 15) 
            # Esto dibuja una elipse dentro de ese rectángulo
            # que se ve como un círculo sobre el vértice
            path.addEllipse(QRectF(p1, p2))
            
            # Posicionamos el texto del bucle
            self.texto_item.setPos(v_x - 10, v_y - 65)

        else:
            # --- LÓGICA PARA ARISTAS NORMALES (INTACTA) ---
            # Aunque la implementamos de forma diferente, el resultado es el mismo
            # Una línea recta entre los vértices, respetando el margen de 20
            linea_total = QLineF(self.v1.pos(), self.v2.pos())
            if linea_total.length() > 0:
                ratio = 20 / linea_total.length()
                p1_x = self.v1.pos().x() + linea_total.dx() * ratio
                p1_y = self.v1.pos().y() + linea_total.dy() * ratio
                p2_x = self.v2.pos().x() - linea_total.dx() * ratio
                p2_y = self.v2.pos().y() - linea_total.dy() * ratio
                
                # Definimos la línea recta en el 'path'
                path.moveTo(p1_x, p1_y)
                path.lineTo(p2_x, p2_y)
                
                # Posicionamos el texto en el centro (lógica original)
                centro_x = (p1_x + p2_x) / 2
                centro_y = (p1_y + p2_y) / 2
                self.texto_item.setPos(centro_x + 5, centro_y - 20)

        # FINALMENTE: Aplicamos el 'path' dibujado al ítem visual
        self.setPath(path)

        # Mantenemos la lógica de añadir el texto a la escena si no está
        if self.scene() and self.texto_item.scene() is None:
            self.scene().addItem(self.texto_item)
# --- Lienzo ---
class GrafoView(QGraphicsView):
    def __init__(self, escena, parent_editor):
        super().__init__(escena)
        self.parent_editor = parent_editor
        self.setRenderHint(QPainter.Antialiasing)
        self.setFocusPolicy(Qt.StrongFocus)

    def keyPressEvent(self, event):
        if not self.parent_editor.modo_lectura:
            if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
                self.parent_editor.eliminar_seleccionado()
                return
        super().keyPressEvent(event)

# --- Contenedor del Grafo ---
class EditorGrafoContenedor(QWidget):
    def __init__(self, titulo, modo_lectura=False):
        super().__init__()
        self.vertices = []
        self.aristas = []
        self.modo_lectura = modo_lectura
        
        self.setStyleSheet("""
            EditorGrafoContenedor { 
                background-color: white; 
                border: 2px solid #e0e6e3; 
                border-radius: 12px;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Encabezado del contenedor
        self.header_frame = QFrame()
        self.header_frame.setFixedHeight(40)
        self.header_frame.setStyleSheet("""
            background-color: #f8faf9; border-bottom: 2px solid #e0e6e3; 
            border-top-left-radius: 12px; border-top-right-radius: 12px;
        """)
        h_lay = QHBoxLayout(self.header_frame)
        
        self.lbl_titulo = QLabel(titulo.upper())
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.lbl_titulo.setStyleSheet("color: #1b4332; font-weight: bold; font-size: 13px; border: none; letter-spacing: 1px;")
        h_lay.addWidget(self.lbl_titulo)
        layout.addWidget(self.header_frame)

        # Contenedor interno para los controles y la escena (con margenes)
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(12, 5, 12, 12)
        layout.addLayout(self.content_layout)
        
        # Redireccionamos los widgets al content_layout
        target_layout = self.content_layout
        
        # Solo mostrar botones de edición si NO es modo lectura
        if not self.modo_lectura:
            btns = QHBoxLayout()
            self.btn_v = QPushButton("➕ VÉRTICES")
            self.btn_a = QPushButton("🔗 ARISTA")
            self.btn_del = QPushButton("🗑️ BORRAR")
            self.btn_save = QPushButton("💾")
            self.btn_load = QPushButton("📂")
            
            estilo_edit = """
                QPushButton { background-color: #2d6a4f; color: white; font-weight: bold; height: 32px; border-radius: 8px; padding: 0 10px; }
                QPushButton:hover { background-color: #1b4332; }
            """
            self.btn_v.setStyleSheet(estilo_edit)
            self.btn_a.setStyleSheet(estilo_edit)
            self.btn_del.setStyleSheet("""
                QPushButton { background-color: #bc4749; color: white; font-weight: bold; height: 32px; border-radius: 8px; padding: 0 10px; }
                QPushButton:hover { background-color: #a4161a; }
            """)
            self.btn_save.setStyleSheet(estilo_edit)
            self.btn_load.setStyleSheet(estilo_edit)
            
            btns.addWidget(self.btn_v)
            btns.addWidget(self.btn_a)
            btns.addWidget(self.btn_del)
            btns.addStretch(1)
            btns.addWidget(self.btn_save)
            btns.addWidget(self.btn_load)
            target_layout.addLayout(btns)
            
            self.btn_v.clicked.connect(self.generar_nodos)
            self.btn_a.clicked.connect(self.crear_arista_dialogo)
            self.btn_del.clicked.connect(self.eliminar_seleccionado)
            self.btn_save.clicked.connect(self.guardar_individual)
            self.btn_load.clicked.connect(self.cargar_individual)

        self.escena = QGraphicsScene()
        self.canvas = GrafoView(self.escena, self)
        self.canvas.setStyleSheet("background-color: white; border: 1px solid #d8e3dc; border-radius: 8px;")
        target_layout.addWidget(self.canvas)

    def agregar_vertice_objetivo(self, x, y, nombre):
        nodo = VerticeVisual(x, y, nombre, self, movible=not self.modo_lectura)
        self.vertices.append(nodo)
        self.escena.addItem(nodo)
        return nodo

    def generar_nodos(self):
        num, ok = QInputDialog.getInt(self, "Vértices", "Cantidad:", 1, 1, 50)
        if ok:
            for i in range(num):
                self.agregar_vertice_objetivo(50 + (i*60), 50 + (i*60), f"V{len(self.vertices)}")

    def crear_arista_dialogo(self):
        if len(self.vertices) < 2: return
        nombres = [v.nombre for v in self.vertices]
        v1_n, ok1 = QInputDialog.getItem(self, "Origen", "Vértice 1:", nombres, 0, False)
        v2_n, ok2 = QInputDialog.getItem(self, "Destino", "Vértice 2:", nombres, 0, False)
        if ok1 and ok2:
            v1 = next(v for v in self.vertices if v.nombre == v1_n)
            v2 = next(v for v in self.vertices if v.nombre == v2_n)
            nombre_a, ok3 = QInputDialog.getText(self, "Arista", "Nombre:", text=f"e{len(self.aristas)}")
            if ok3:
                nueva = AristaVisual(v1, v2, nombre_a, editable=not self.modo_lectura)
                self.aristas.append(nueva); self.escena.addItem(nueva)

    def eliminar_seleccionado(self):
        if self.modo_lectura: return
        for item in self.escena.selectedItems():
            if isinstance(item, VerticeVisual):
                aristas_a_borrar = [a for a in self.aristas if a.v1 == item or a.v2 == item]
                for a in aristas_a_borrar:
                    if a.texto_item.scene(): self.escena.removeItem(a.texto_item)
                    self.escena.removeItem(a)
                    if a in self.aristas: self.aristas.remove(a)
                if item in self.vertices: self.vertices.remove(item)
            elif isinstance(item, AristaVisual):
                if item.texto_item.scene(): self.escena.removeItem(item.texto_item)
                if item in self.aristas: self.aristas.remove(item)
            self.escena.removeItem(item)

    def actualizar_aristas(self):
        for arista in self.aristas: arista.actualizar_posicion()

    def guardar_individual(self):
        path, _ = QFileDialog.getSaveFileName(self, "Guardar Grafo", "", "JSON Files (*.json)")
        if path:
            data = {
                "v": [{"n": v.nombre, "x": v.pos().x(), "y": v.pos().y()} for v in self.vertices],
                "a": [{"n": a.nombre, "v1": a.v1.nombre, "v2": a.v2.nombre} for a in self.aristas]
            }
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            QMessageBox.information(self, "Éxito", "Grafo guardado correctamente.")

    def cargar_individual(self):
        path, _ = QFileDialog.getOpenFileName(self, "Cargar Grafo", "", "JSON Files (*.json)")
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.escena.clear()
            self.vertices = []; self.aristas = []
            for v in data["v"]:
                self.agregar_vertice_objetivo(v["x"], v["y"], v["n"])
            for a in data["a"]:
                v1 = next((v for v in self.vertices if v.nombre == a["v1"]), None)
                v2 = next((v for v in self.vertices if v.nombre == a["v2"]), None)
                if v1 and v2:
                    nueva = AristaVisual(v1, v2, a["n"])
                    self.aristas.append(nueva); self.escena.addItem(nueva)
            self.actualizar_aristas()
            QMessageBox.information(self, "Éxito", "Grafo cargado correctamente.")

# --- Interfaz de Unión ---
class InterfazUnion(QWidget):
    def __init__(self, main_window):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # --- Ribbon de Operaciones ---
        self.ribbon = QFrame()
        self.ribbon.setFixedHeight(105)
        self.ribbon.setStyleSheet("""
            QFrame { background-color: #f8faf9; border: 1px solid #d8e3dc; border-radius: 12px; }
            QLabel { color: #1b4332; font-weight: bold; font-size: 10px; text-transform: uppercase; }
            QPushButton { 
                background-color: #2d6a4f; color: white; border-radius: 8px; 
                font-weight: bold; font-size: 12px; padding: 8px;
            }
            QPushButton:hover { background-color: #1b4332; }
            QComboBox, QLineEdit { 
                background: white; color: #1b4332; border: 2px solid #e0e6e3; 
                border-radius: 6px; padding: 4px; font-weight: bold;
            }
            QComboBox QAbstractItemView {
                background-color: white; color: black;
                selection-background-color: #2d6a4f; selection-color: white;
            }
        """)
        ribbon_lay = QHBoxLayout(self.ribbon)
        ribbon_lay.setContentsMargins(30, 0, 30, 0); ribbon_lay.setSpacing(20)

        def create_sep():
            line = QFrame(); line.setFrameShape(QFrame.VLine); line.setFrameShadow(QFrame.Plain)
            line.setStyleSheet("color: #d8e3dc; margin: 10px 0;"); return line

        # Grupo Archivos
        file_lay = QVBoxLayout()
        btn_g_save = QPushButton("💾 GUARDAR PROYECTO")
        btn_g_load = QPushButton("📂 RECUPERAR PROYECTO")
        btn_g_save.clicked.connect(self.guardar_todo)
        btn_g_load.clicked.connect(self.cargar_todo)
        file_lay.addWidget(btn_g_save); file_lay.addWidget(btn_g_load)

        # Grupo Acciones
        self.btn_resolver = QPushButton("⚡ CALCULAR UNIÓN (G1 ∪ G2)")
        self.btn_resolver.setFixedHeight(50); self.btn_resolver.setFixedWidth(280)
        self.btn_resolver.clicked.connect(self.resolver_union)

        ribbon_lay.addStretch(1)
        ribbon_lay.addLayout(file_lay)
        ribbon_lay.addStretch(1)
        ribbon_lay.addWidget(create_sep())
        ribbon_lay.addStretch(1)
        ribbon_lay.addWidget(self.btn_resolver)
        ribbon_lay.addStretch(2)

        layout.addWidget(self.ribbon)

        # TÍTULO
        self.main_title = QLabel("OPERACIÓN: UNIÓN DE GRAFOS")
        self.main_title.setStyleSheet("""
            color: #1b4332; font-size: 24px; font-weight: bold; 
            margin: 10px; text-transform: uppercase; letter-spacing: 1px;
        """)
        self.main_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.main_title)

        # CUERPO (Side by Side)
        self.cuerpo_editores = QHBoxLayout()
        self.cuerpo_editores.setSpacing(20)
        self.cuerpo_editores.setContentsMargins(15, 0, 15, 15)
        
        self.g1 = EditorGrafoContenedor("GRAFO G1")
        self.g2 = EditorGrafoContenedor("GRAFO G2")
        self.cuerpo_editores.addWidget(self.g1)
        self.cuerpo_editores.addWidget(self.g2)
        
        layout.addLayout(self.cuerpo_editores)

        # RESULTADO (Oculto inicialmente)
        self.g_res = EditorGrafoContenedor("RESULTADO DE LA UNIÓN", modo_lectura=True)
        self.g_res.hide()
        layout.addWidget(self.g_res)
        layout.setStretch(2, 1) # Dar peso al cuerpo de editores

    def resolver_union(self):
        self.g_res.show()
        self.g_res.escena.clear()
        self.g_res.vertices = []
        self.g_res.aristas = []
        
        nodos_resultado = {}

        # 1. Procesar vértices
        for v in self.g1.vertices + self.g2.vertices:
            if v.nombre not in nodos_resultado:
                # CAMBIO CLAVE: Forzamos movible=True directamente en la creación
                # para que el usuario pueda acomodar el resultado a su gusto.
                nuevo_v = VerticeVisual(v.pos().x(), v.pos().y(), v.nombre, self.g_res, movible=True)
                self.g_res.vertices.append(nuevo_v)
                self.g_res.escena.addItem(nuevo_v)
                nodos_resultado[v.nombre] = nuevo_v

        # 2. Procesar aristas
        aristas_unicas = {}
        for a in self.g1.aristas + self.g2.aristas:
            id_conexion = tuple(sorted((a.v1.nombre, a.v2.nombre)))
            clave_arista = (a.nombre, id_conexion)

            if clave_arista not in aristas_unicas:
                v_origen = nodos_resultado[a.v1.nombre]
                v_destino = nodos_resultado[a.v2.nombre]
                
                # Las aristas del resultado no son editables (doble click no hace nada)
                nueva_a = AristaVisual(v_origen, v_destino, a.nombre, editable=False)
                self.g_res.aristas.append(nueva_a)
                self.g_res.escena.addItem(nueva_a)
                
                aristas_unicas[clave_arista] = True
        
        self.g_res.actualizar_aristas()

    def guardar_todo(self):
        path, _ = QFileDialog.getSaveFileName(self, "Guardar Proyecto", "", "JSON Files (*.json)")
        if path:
            def serializar(grafo):
                return {
                    "v": [{"n": v.nombre, "x": v.pos().x(), "y": v.pos().y()} for v in grafo.vertices],
                    "a": [{"n": a.nombre, "v1": a.v1.nombre, "v2": a.v2.nombre} for a in grafo.aristas]
                }
            data = {"g1": serializar(self.g1), "g2": serializar(self.g2)}
            with open(path, 'w') as f: json.dump(data, f)

    def cargar_todo(self):
        path, _ = QFileDialog.getOpenFileName(self, "Cargar Proyecto", "", "JSON Files (*.json)")
        if path:
            with open(path, 'r') as f: data = json.load(f)
            for key, grafo_obj in [("g1", self.g1), ("g2", self.g2)]:
                grafo_obj.escena.clear()
                grafo_obj.vertices = []; grafo_obj.aristas = []
                for v in data[key]["v"]:
                    grafo_obj.agregar_vertice_objetivo(v["x"], v["y"], v["n"])
                for a in data[key]["a"]:
                    v1 = next((v for v in grafo_obj.vertices if v.nombre == a["v1"]), None)
                    v2 = next((v for v in grafo_obj.vertices if v.nombre == a["v2"]), None)
                    if v1 and v2:
                        nueva = AristaVisual(v1, v2, a["n"])
                        grafo_obj.aristas.append(nueva); grafo_obj.escena.addItem(nueva)
            self.g_res.hide()