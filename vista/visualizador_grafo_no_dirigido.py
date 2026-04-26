from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPointF, Signal
from PySide6.QtGui import QPainter, QPen, QColor, QFont
import math

class VisualizadorGrafoNoDirigido(QWidget):
    solicitud_eliminacion = Signal()

    def __init__(self, titulo="Grafo", parent=None, ancho=500, alto=500):
        super().__init__(parent)
        self.titulo = titulo
        self.aristas = []
        self.num_vertices = 0
        self.etiquetas = {}
        self.ponderaciones_lista = []
        self.setMinimumSize(300, 300)
        self.setFocusPolicy(Qt.StrongFocus)
        
        self.pos_vertices = []  # Almacena QPointF
        self.nodo_arrastrando = None
        self.objeto_seleccionado = None # ('vertice', index) o ('arista', index)
        self.setMouseTracking(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            self.solicitud_eliminacion.emit()
        super().keyPressEvent(event)

    def set_grafo(self, num_vertices, aristas, etiquetas=None, ponderaciones=None):
        cambio_estructura = (num_vertices != self.num_vertices)
        self.num_vertices = num_vertices
        self.aristas = aristas
        if etiquetas:
            self.etiquetas = etiquetas.copy()
        else:
            self.etiquetas = {i: str(i + 1) for i in range(num_vertices)}

        # Acepta ponderaciones como dict {arista: peso} O como lista [peso,...]
        if isinstance(ponderaciones, dict):
            self.ponderaciones_lista = [
                str(ponderaciones.get(a, ponderaciones.get((a[1], a[0]), "")))
                for a in aristas
            ]
        elif ponderaciones:
            self.ponderaciones_lista = [str(p) for p in ponderaciones]
        else:
            self.ponderaciones_lista = [""] * len(aristas)

        if cambio_estructura:
            self.inicializar_posiciones()
        self.update()


    def inicializar_posiciones(self):
        self.pos_vertices = []
        if self.num_vertices == 0: return
        w, h = self.width(), self.height()
        if w < 100: w = 600 # Fallback si no ha cargado el layout
        if h < 100: h = 400
        
        centro_x, centro_y = w / 2, h / 2
        radio = min(centro_x, centro_y) - 60
        for i in range(self.num_vertices):
            angulo = 2 * math.pi * i / self.num_vertices - math.pi / 2
            x = centro_x + radio * math.cos(angulo)
            y = centro_y + radio * math.sin(angulo)
            self.pos_vertices.append(QPointF(x, y))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos_mouse = event.position()
            
            # 1. Detectar Vértices
            for i, p_vert in enumerate(self.pos_vertices):
                dist = (p_vert - pos_mouse).manhattanLength()
                if dist < 25:
                    self.nodo_arrastrando = i
                    self.objeto_seleccionado = ('vertice', i)
                    self.setCursor(Qt.ClosedHandCursor)
                    self.update()
                    return

            # 2. Detectar Aristas (distancia punto a segmento)
            for i, (u, v) in enumerate(self.aristas):
                if u < len(self.pos_vertices) and v < len(self.pos_vertices):
                    p1, p2 = self.pos_vertices[u], self.pos_vertices[v]
                    if self._distancia_punto_segmento(pos_mouse, p1, p2) < 10:
                        self.objeto_seleccionado = ('arista', i)
                        self.update()
                        return
            
            # 3. Click en el vacío
            self.objeto_seleccionado = None
            self.update()

    def _distancia_punto_segmento(self, p, a, b):
        # Distancia mínima entre punto p y segmento ab
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
        if self.nodo_arrastrando is not None:
            self.pos_vertices[self.nodo_arrastrando] = event.position()
            self.update()
        else:
            # Cambiar cursor si pasa por encima de un nodo
            sobre_nodo = False
            for p_vert in self.pos_vertices:
                if (p_vert - event.position()).manhattanLength() < 25:
                    sobre_nodo = True
                    break
            if sobre_nodo: self.setCursor(Qt.PointingHandCursor)
            else: self.unsetCursor()

    def mouseReleaseEvent(self, event):
        self.nodo_arrastrando = None
        self.unsetCursor()

    def resizeEvent(self, event):
        if not self.pos_vertices and self.num_vertices > 0:
            self.inicializar_posiciones()
        super().resizeEvent(event)

    def paintEvent(self, event):
        if not self.pos_vertices and self.num_vertices > 0:
            self.inicializar_posiciones()
            
        painter = QPainter(self); painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor("#f0f7f4"))
        if self.num_vertices == 0: return

        # Dibujar aristas
        for i, (u, v) in enumerate(self.aristas):
            if u < len(self.pos_vertices) and v < len(self.pos_vertices):
                p1, p2 = self.pos_vertices[u], self.pos_vertices[v]
                
                es_sel = (self.objeto_seleccionado == ('arista', i))
                color = QColor("#ff4d4d") if es_sel else QColor("#1b4332")
                ancho = 4 if es_sel else 2
                
                painter.setPen(QPen(color, ancho))
                painter.drawLine(p1, p2)
                
                pond = self.ponderaciones_lista[i] if i < len(self.ponderaciones_lista) else ""
                if pond:
                    mx, my = (p1.x() + p2.x())/2, (p1.y() + p2.y())/2
                    dx, dy = p2.x() - p1.x(), p2.y() - p1.y()
                    dist = math.sqrt(dx*dx + dy*dy) or 1
                    offset_x, offset_y = -dy/dist*15, dx/dist*15
                    painter.setPen(QPen(QColor("#d9534f"), 1))
                    painter.setFont(QFont("Arial", 9, QFont.Bold))
                    painter.drawText(int(mx + offset_x), int(my + offset_y), str(pond))

        # Dibujar vértices
        for i, pos in enumerate(self.pos_vertices):
            es_sel = (self.objeto_seleccionado == ('vertice', i))
            color_borde = QColor("#ff4d4d") if es_sel else QColor("#1b4332")
            ancho_borde = 4 if es_sel else 2
            
            painter.setBrush(QColor("#2d6a4f"))
            painter.setPen(QPen(color_borde, ancho_borde))
            painter.drawEllipse(pos, 22, 22)
            painter.setPen(QColor("white")); painter.setFont(QFont("Arial", 11, QFont.Bold))
            txt = self.etiquetas.get(i, str(i+1)); rect = painter.fontMetrics().boundingRect(txt)
            painter.drawText(int(pos.x()-rect.width()/2), int(pos.y()+rect.height()/4), txt)
