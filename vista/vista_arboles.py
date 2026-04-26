from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPen, QBrush, QColor, QFont
from controlador.controlador_arboles import ControladorArboles

class VistaArboles(QWidget):
    def __init__(self, main_window, metodo):
        super().__init__()
        self.camino_resaltado = None
        self.main_window = main_window
        self.metodo = metodo
        self.historial_logs = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        # === TÍTULO ===
        lbl_titulo = QLabel(metodo)
        lbl_titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #1b4332;")
        layout.addWidget(lbl_titulo)

        # === CONTROLES ===
        ctrl_panel = QFrame()
        ctrl_panel.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #d8e3dc;")
        ctrl_layout = QHBoxLayout(ctrl_panel)
        
        self.input_clave = QLineEdit()
        self.input_clave.setPlaceholderText("Clave/Texto...")
        self.input_clave.setFixedWidth(200)
        self.input_clave.setStyleSheet("padding: 8px; border: 1px solid #40916c; border-radius: 5px;")
        
        btn_ins = self.boton_accion("➕ Insertar")
        btn_bus = self.boton_accion("🔍 Buscar")
        btn_eli = self.boton_accion("🗑️ Eliminar")
        btn_clr = self.boton_accion("♻️ Limpiar")
        
        btn_sav = self.boton_accion("💾 Guardar")
        btn_lod = self.boton_accion("📂 Recuperar")
        
        ctrl_layout.addWidget(QLabel("Entrada:"))
        ctrl_layout.addWidget(self.input_clave)
        ctrl_layout.addWidget(btn_ins)
        ctrl_layout.addWidget(btn_bus)

        if metodo != "Árboles de Huffman":
            ctrl_layout.addWidget(btn_eli)
        
        self.huffman_btns = QWidget()
        h_layout = QHBoxLayout(self.huffman_btns)
        h_layout.setContentsMargins(0,0,0,0)

        ctrl_layout.addWidget(self.huffman_btns)
        self.huffman_btns.setVisible(metodo == "Árboles de Huffman")

        ctrl_layout.addWidget(btn_clr)
        ctrl_layout.addWidget(btn_sav)
        ctrl_layout.addWidget(btn_lod)
        ctrl_layout.addStretch()
        layout.addWidget(ctrl_panel)

        # === ÁREA GRÁFICA Y LOG ===
        split_layout = QHBoxLayout()
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(self.view.renderHints().Antialiasing)
        self.view.setStyleSheet("background: #f8fcf9; border: 1px solid #d8e3dc; border-radius: 10px;")
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        
        self.salida = QTextEdit()
        self.salida.setReadOnly(True)
        self.salida.setFixedWidth(250)
        self.salida.setStyleSheet("background: white; border-radius: 10px; padding: 10px; color: #2d6a4f; border: 1px solid #d8e3dc;")

        split_layout.addWidget(self.view, 3)
        split_layout.addWidget(self.salida, 1)
        layout.addLayout(split_layout)

        self.controlador = ControladorArboles(self, metodo)
        self.controlador.cargar()
        
        btn_ins.clicked.connect(lambda: self.controlador.insertar(self.input_clave.text()))
        btn_bus.clicked.connect(lambda: self.controlador.buscar(self.input_clave.text()))
        btn_eli.clicked.connect(lambda: self.controlador.eliminar(self.input_clave.text()))
        btn_clr.clicked.connect(self.controlador.eliminar_todo)
        btn_sav.clicked.connect(self.manual_save)
        btn_lod.clicked.connect(self.manual_load)
        

    def boton_accion(self, t):
        btn = QPushButton(t)
        btn.setStyleSheet("QPushButton { background: #2d6a4f; color: white; font-weight: bold; border-radius: 8px; padding: 5px 12px; font-size: 11px; } QPushButton:hover { background: #40916c; }")
        return btn

    def mensaje(self, texto):
    # Reemplaza todo el contenido anterior con el nuevo mensaje
        formato = f"""
        <div style='text-align: center;'>
            <hr style='border: 0; border-top: 1px solid #d8e3dc;'>
            <p style='font-size: 14px; color: #1b4332; margin-top: 10px;'>{texto}</p>
        </div>
        """
        self.salida.setHtml(formato)

    def prompt_codificar(self):
        text, ok = QInputDialog.getText(self, "Huffman", "Texto a codificar:")
        if ok: self.controlador.codificar(text)

    def prompt_decodificar(self):
        text, ok = QInputDialog.getText(self, "Huffman", "Binario a decodificar:")
        if ok: self.controlador.decodificar(text)

    def manual_save(self):
        path, _ = QFileDialog.getSaveFileName(self, "Guardar Estructura", "", "JSON Files (*.json)")
        if path:
            from modelo.manejador_archivos import ManejadorArchivos
            ManejadorArchivos.guardar_json(path, self.controlador.modelo.to_dict())
            self.mensaje(f"Estructura guardada en {path}")

    def manual_load(self):
        path, _ = QFileDialog.getOpenFileName(self, "Abrir Estructura", "", "JSON Files (*.json)")
        if path:
            from modelo.manejador_archivos import ManejadorArchivos
            datos = ManejadorArchivos.leer_json(path)
            if datos:
                old_path = self.controlador.ruta_archivo
                self.controlador.ruta_archivo = path
                self.controlador.cargar()
                self.controlador.ruta_archivo = old_path
                self.mensaje(f"Estructura cargada desde {path}")

    # =========================================================
    # LÓGICA DE DIBUJO CON RESALTADO
    # =========================================================

    def actualizar_dibujo(self):
        self.scene.clear()
        m = self.controlador.modelo
        if not m: return

        # Estilos base
        self.pen_linea = QPen(QColor("#1b4332"), 2)
        self.brush_nodo = QBrush(QColor("#2d6a4f"))
        self.brush_hoja = QBrush(QColor("#40916c"))
        self.pen_resaltado = QPen(QColor("#e63946"), 3)
        self.brush_resaltado = QBrush(QColor("#e63946"))
        
        # Dibujar según el método (Ajustamos los offsets para mayor claridad)
        if self.metodo == "Árboles Digitales":
            self._dibujar_digital(m.raiz, 0, 0, 350, 90, "")
        elif self.metodo == "Árboles de Huffman":
            self._dibujar_huffman(m.raiz, 0, 0, 300, 90, "")
        elif self.metodo in ["Tries de Residuos", "Múltiples Residuos"]:
            self._dibujar_trie(m.raiz, 0, 0, 400, 100, "")

        # === AJUSTE DE PANTALLA (Para todos los árboles) ===
        rect_contenido = self.scene.itemsBoundingRect()
        if not rect_contenido.isEmpty():
            # Añadimos un margen de 50px alrededor para que no toque los bordes
            rect_con_margen = rect_contenido.adjusted(-50, -50, 50, 50)
            self.scene.setSceneRect(rect_con_margen)
            self.view.fitInView(rect_con_margen, Qt.KeepAspectRatio)

    def _dibujar_nodo(self, x, y, texto, es_hoja=False, resaltado=False):
        radio = 20
        pen = self.pen_resaltado if resaltado else self.pen_linea
        brush = self.brush_resaltado if resaltado else (self.brush_hoja if es_hoja else self.brush_nodo)

        circulo = self.scene.addEllipse(x - radio, y - radio, 2*radio, 2*radio, pen, brush)
        
        txt_item = self.scene.addText(texto)
        txt_item.setDefaultTextColor(Qt.white)
        txt_item.setFont(QFont("Segoe UI", 8, QFont.Bold))
        rect = txt_item.boundingRect()
        txt_item.setPos(x - rect.width()/2, y - rect.height()/2)
        return circulo

    def _dibujar_etiqueta_rama(self, x, y, texto):
        radio = 10
        fnd = self.scene.addEllipse(x - radio, y - radio, 2*radio, 2*radio, QPen(Qt.black, 1), QBrush(Qt.white))
        txt = self.scene.addText(texto, QFont("Consolas", 9, QFont.Bold))
        txt.setDefaultTextColor(Qt.black)
        rect = txt.boundingRect()
        txt.setPos(x - rect.width()/2, y - rect.height()/2)
        return fnd

    def _dibujar_digital(self, nodo, x, y, offset, gap, ruta_actual):
        if not nodo: return
        
        # Resaltar si es parte del camino
        resaltado = self.camino_resaltado is not None and self.camino_resaltado.startswith(ruta_actual)
        txt = ",".join(nodo.letras) if nodo.letras else ("R" if nodo == self.controlador.modelo.raiz else "")
        self._dibujar_nodo(x, y, txt, nodo.es_fin, resaltado)
        
        for bit in ["0", "1"]:
            h = nodo.hijos.get(bit)
            if h:
                proxima_ruta = ruta_actual + bit
                nx, ny = (x - offset if bit == "0" else x + offset), (y + gap)
                
                # Línea resaltada si la ruta buscada sigue por aquí
                linea_res = self.camino_resaltado is not None and self.camino_resaltado.startswith(proxima_ruta)
                self.scene.addLine(x, y + 20, nx, ny - 20, self.pen_resaltado if linea_res else self.pen_linea)
                self._dibujar_etiqueta_rama((x+nx)/2, (y+ny)/2 - 5, bit)
                self._dibujar_digital(h, nx, ny, offset/2, gap, proxima_ruta)

    def _dibujar_huffman(self, nodo, x, y, offset, gap, ruta_actual):
        if not nodo: return
        
        # Validación estricta para el resaltado
        resaltado = False
        if self.camino_resaltado is not None:
            resaltado = self.camino_resaltado.startswith(ruta_actual)
        
        txt = f"{nodo.char}:{nodo.freq}" if nodo.char else str(nodo.freq)
        self._dibujar_nodo(x, y, txt, nodo.char is not None, resaltado)
        
        for bit, hijo in [("0", nodo.izq), ("1", nodo.der)]:
            if hijo:
                prox_ruta = ruta_actual + bit
                nx, ny = (x - offset if bit == "0" else x + offset), (y + gap)
                
                linea_res = False
                if self.camino_resaltado is not None:
                    linea_res = self.camino_resaltado.startswith(prox_ruta)
                
                self.scene.addLine(x, y + 20, nx, ny - 20, self.pen_resaltado if linea_res else self.pen_linea)
                self._dibujar_huffman(hijo, nx, ny, offset/2, gap, prox_ruta)

    def _dibujar_trie(self, nodo, x, y, offset, gap, ruta_actual):
        if not nodo: return
        
        # Lógica de resaltado (se mantiene igual)
        resaltado = False
        if self.camino_resaltado:
            comp_actual = ruta_actual.replace("-", "")
            comp_buscada = self.camino_resaltado.replace("-", "")
            resaltado = comp_buscada.startswith(comp_actual)

        lbl = ""
        is_h = False
        if hasattr(nodo, 'es_enlace'): 
            lbl, is_h = ("*" if nodo.es_enlace else (nodo.letra or "")), not nodo.es_enlace
        else:
            lbl, is_h = (nodo.letra or ""), nodo.letra is not None

        self._dibujar_nodo(x, y, lbl, is_h, resaltado)
        
        hijos_keys = sorted(nodo.hijos.keys())
        n_hijos = len(hijos_keys)
        if n_hijos == 0: return
        
        # --- CAMBIO AQUÍ: Distribución simétrica real ---
        # Calculamos el ancho total que ocuparán los hijos
        ancho_total = (n_hijos - 1) * offset
        inicio_x = x - ancho_total / 2 # Centramos los hijos bajo el padre
        
        for i, k in enumerate(hijos_keys):
            proxima_ruta = (ruta_actual + ("-" if ruta_actual else "") + k)
            nx = inicio_x + (i * offset)
            ny = y + gap
            
            linea_res = False
            if self.camino_resaltado:
                linea_res = self.camino_resaltado.replace("-", "").startswith(proxima_ruta.replace("-", ""))

            # Dibujar línea y etiqueta
            self.scene.addLine(x, y + 20, nx, ny - 20, self.pen_resaltado if linea_res else self.pen_linea)
            self._dibujar_etiqueta_rama((x + nx) / 2, (y + ny) / 2 - 10, k)
            
            # Llamada recursiva con offset reducido para el siguiente nivel
            self._dibujar_trie(nodo.hijos[k], nx, ny, offset * 0.7, gap, proxima_ruta)

    def resaltar_camino(self, ruta):
        self.camino_resaltado = ruta
        self.actualizar_dibujo()