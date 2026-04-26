from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QTableWidget, QTableWidgetItem, QSpinBox,
    QScrollArea, QHeaderView, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from controlador.algoritmos.floyd_controller import FloydController

class VistaFloyd(QWidget):
    def __init__(self):
        super().__init__()
        self.num_vertices = 4
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15); main_layout.setSpacing(15)
        
        # --- Ribbon Estilizado ---
        self.ribbon = QFrame()
        self.ribbon.setFixedHeight(105)
        self.ribbon.setStyleSheet("""
            QFrame#ribbon { background-color: #f8faf9; border: 1px solid #d8e3dc; border-radius: 12px; }
            QLabel { color: #1b4332; font-weight: bold; font-size: 10px; text-transform: uppercase; }
            QSpinBox, QComboBox {
                background-color: white; color: #1b4332;
                border: 2px solid #e0e6e3; border-radius: 6px;
                padding: 4px; font-weight: bold; font-size: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                selection-background-color: #2d6a4f;
                selection-color: white;
            }
            QSpinBox:focus, QComboBox:focus { border-color: #2d6a4f; }
            QPushButton {
                background-color: #2d6a4f; color: white; font-weight: bold;
                border: none; border-radius: 8px; padding: 8px 15px; font-size: 11px;
            }
            QPushButton:hover { background-color: #1b4332; }
            QPushButton#btn_calc { 
                background-color: #1b4332; font-size: 13px; border-radius: 10px;
                padding: 10px 25px;
            }
            QPushButton#btn_calc:hover { background-color: #081c15; }
        """)
        self.ribbon.setObjectName("ribbon")
        ribbon_layout = QHBoxLayout(self.ribbon)
        ribbon_layout.setContentsMargins(30, 0, 30, 0); ribbon_layout.setSpacing(20)

        # --- Definición de Widgets ---
        self.spin = QSpinBox(); self.spin.setRange(2, 8); self.spin.setValue(4); self.spin.setFixedWidth(50)
        btn_set = QPushButton("↺ REINICIAR"); btn_set.setFixedWidth(100); btn_set.clicked.connect(self.preparar_tabla)

        self.cb_nom = QComboBox(); self.cb_nom.setFixedWidth(60); self.cb_nom.addItems(["123", "ABC", "abc"])
        self.cb_nom.currentIndexChanged.connect(self.preparar_tabla)
        
        self.cb_k = QComboBox(); self.cb_k.setFixedWidth(70)
        
        self.btn_calc = QPushButton("⚡ EJECUTAR FLOYD"); self.btn_calc.setObjectName("btn_calc")
        self.btn_calc.clicked.connect(self.ejecutar)

        self.btn_save = QPushButton("💾 GUARDAR"); self.btn_save.setFixedWidth(100); self.btn_save.clicked.connect(self.guardar_matriz)
        self.btn_load = QPushButton("📂 RECUPERAR"); self.btn_load.setFixedWidth(100); self.btn_load.clicked.connect(self.cargar_matriz)

        # --- Grupos ---
        def create_sep():
            line = QFrame(); line.setFrameShape(QFrame.VLine); line.setFrameShadow(QFrame.Plain)
            line.setStyleSheet("color: #d8e3dc; margin: 10px 0;"); return line

        # 1. Grupo Configuración
        config_lay = QVBoxLayout()
        lbl_tam = QLabel("📏 Tamaño"); lbl_tam.setFixedWidth(70)
        lbl_nom = QLabel("🔤 Nom."); lbl_nom.setFixedWidth(70)
        config_top = QHBoxLayout(); config_top.addWidget(lbl_tam); config_top.addWidget(self.spin)
        config_bot = QHBoxLayout(); config_bot.addWidget(lbl_nom); config_bot.addWidget(self.cb_nom)
        config_lay.addLayout(config_top); config_lay.addLayout(config_bot)
        
        # 2. Grupo Intermediario
        inter_lay = QVBoxLayout()
        lbl_k = QLabel("📍 Intermediario (K)"); lbl_k.setFixedWidth(120)
        inter_lay.addWidget(lbl_k)
        inter_lay.addWidget(self.cb_k)
        inter_lay.addWidget(btn_set)

        # 3. Grupo Archivos
        file_lay = QVBoxLayout()
        file_lay.addWidget(self.btn_save); file_lay.addWidget(self.btn_load)

        ribbon_layout.addStretch(1)
        ribbon_layout.addLayout(config_lay)
        ribbon_layout.addStretch(1)
        ribbon_layout.addWidget(create_sep())
        ribbon_layout.addStretch(1)
        ribbon_layout.addLayout(inter_lay)
        ribbon_layout.addStretch(1)
        ribbon_layout.addWidget(create_sep())
        ribbon_layout.addStretch(1)
        ribbon_layout.addLayout(file_lay)
        ribbon_layout.addStretch(2)
        ribbon_layout.addWidget(self.btn_calc)
        ribbon_layout.addStretch(1)
        
        main_layout.addWidget(self.ribbon)
        
        # --- Cuerpo ---
        body = QHBoxLayout()
        
        input_wrap = QFrame()
        input_wrap.setStyleSheet("background: white; border: 1px solid #d8e3dc; border-radius: 10px;")
        input_lay = QVBoxLayout(input_wrap)
        lbl_in = QLabel("📥 MATRIZ DE ADYACENCIA (ENTRADA)")
        lbl_in.setStyleSheet("color: #1b4332; font-weight: bold; font-size: 14px; padding: 5px;")
        input_lay.addWidget(lbl_in)
        lbl_hint = QLabel("💡 Doble clic para editar. Usa '∞' para sin conexión.")
        lbl_hint.setStyleSheet("color: #666; font-size: 10px; border: none; padding-left: 5px;")
        input_lay.addWidget(lbl_hint)
        
        self.tabla = QTableWidget()
        self.tabla.setStyleSheet("color: #1b4332; border: none; gridline-color: #d8e3dc; font-size: 11px;")
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        input_lay.addWidget(self.tabla)
        body.addWidget(input_wrap, stretch=2) # Ajustado a 2 para balance
        
        res_wrap = QFrame()
        res_wrap.setStyleSheet("background: white; border: 1px solid #d8e3dc; border-radius: 10px;")
        res_lay = QVBoxLayout(res_wrap)
        lbl_res = QLabel("📈 RESULTADO SELECCIONADO")
        lbl_res.setStyleSheet("color: #1b4332; font-weight: bold; padding: 5px; border-bottom: 1px solid #f0f7f4;")
        res_lay.addWidget(lbl_res)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True); self.scroll.setStyleSheet("background: transparent; border: none;")
        self.res_container = QWidget(); self.res_container.setStyleSheet("background: transparent;")
        self.res_layout = QVBoxLayout(self.res_container); self.scroll.setWidget(self.res_container)
        res_lay.addWidget(self.scroll)
        body.addWidget(res_wrap, stretch=1)
        
        main_layout.addLayout(body)
        self.preparar_tabla()

    def preparar_tabla(self):
        n = self.spin.value(); self.num_vertices = n
        self.tabla.setRowCount(n); self.tabla.setColumnCount(n)
        
        modo = self.cb_nom.currentText()
        self.etiquetas = {}
        headers = []
        for i in range(n):
            if modo == "ABC":
                label, t = "", i
                while t >= 0: label = chr(65 + (t % 26)) + label; t = (t // 26) - 1
                self.etiquetas[i] = label
            elif modo == "abc":
                label, t = "", i
                while t >= 0: label = chr(97 + (t % 26)) + label; t = (t // 26) - 1
                self.etiquetas[i] = label
            else: self.etiquetas[i] = str(i+1)
            headers.append(self.etiquetas[i])

        self.tabla.setHorizontalHeaderLabels(headers); self.tabla.setVerticalHeaderLabels(headers)
        self.cb_k.clear(); self.cb_k.addItems(headers)
        
        for i in range(n):
            for j in range(n):
                item = QTableWidgetItem("0" if i==j else "∞")
                item.setTextAlignment(Qt.AlignCenter); self.tabla.setItem(i, j, item)

    def guardar_matriz(self):
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        import json
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Matriz Floyd", "", "JSON Files (*.json)")
        if archivo:
            filas = self.tabla.rowCount()
            matriz = []
            for i in range(filas):
                fila = []
                for j in range(filas):
                    item = self.tabla.item(i, j)
                    fila.append(item.text() if item else "0")
                matriz.append(fila)
            datos = {
                'tam': filas,
                'matriz': matriz,
                'nom': self.cb_nom.currentIndex()
            }
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4)
            QMessageBox.information(self, "Éxito", "Matriz guardada correctamente.")

    def cargar_matriz(self):
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        import json
        archivo, _ = QFileDialog.getOpenFileName(self, "Cargar Matriz Floyd", "", "JSON Files (*.json)")
        if archivo:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            self.spin.setValue(datos['tam'])
            self.preparar_tabla() 
            self.cb_nom.setCurrentIndex(datos.get('nom', 0))
            for i in range(datos['tam']):
                for j in range(datos['tam']):
                    val = datos['matriz'][i][j]
                    self.tabla.setItem(i, j, QTableWidgetItem(val))
            QMessageBox.information(self, "Éxito", "Matriz cargada correctamente.")

    def ejecutar(self):
        n = self.num_vertices; aristas = []; ponderaciones = {}
        target_k = self.cb_k.currentIndex()
        
        for i in range(n):
            for j in range(n):
                val = self.tabla.item(i, j).text()
                if val not in ["∞", "inf", "INF"] and i != j:
                    try: ponderaciones[(i, j)] = val; aristas.append((i, j))
                    except: pass
        
        ctrl = FloydController(n, aristas, self.etiquetas.copy(), ponderaciones)
        iteraciones = ctrl.ejecutar()
        
        # Limpiar anterior
        for i in reversed(range(self.res_layout.count())): 
            w = self.res_layout.itemAt(i).widget()
            if w: w.setParent(None)
            
        # Solo mostrar Inicial e Intermediario Seleccionado
        indices_a_mostrar = [0, target_k + 1]
        
        for idx in indices_a_mostrar:
            if idx >= len(iteraciones): continue
            it = iteraciones[idx]
            
            card = QFrame()
            card.setStyleSheet("background: white; border: 1px solid #d8e3dc; border-radius: 6px; margin-bottom: 8px; padding: 5px;")
            card_lay = QVBoxLayout(card)
            lbl = QLabel(f"📍 {it['info'].upper()}")
            lbl.setStyleSheet("color: #1b4332; border: none; font-size: 12px; font-weight: bold; margin-bottom: 5px;")
            card_lay.addWidget(lbl)
            
            t = QTableWidget(n, n)
            t.setFixedHeight(140 + (n*10)); t.setMinimumHeight(150)
            t.setStyleSheet("""
                QTableWidget {
                    font-size: 11px;
                    color: #1b4332;
                    border: 1px solid #e9f3ef;
                    gridline-color: #f0f7f4;
                    background-color: white;
                }
                QHeaderView::section {
                    background-color: #2d6a4f;
                    color: white;
                    font-weight: bold;
                    padding: 4px;
                    border: 1px solid #1b4332;
                }
            """)
            t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            t.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
            t.setHorizontalHeaderLabels([chr(65+i) for i in range(n)])
            t.setVerticalHeaderLabels([chr(65+i) for i in range(n)])
            
            for r in range(n):
                for c in range(n):
                    val = it['matriz_distancias'][r][c]
                    str_val = str(val) if val != float('inf') else "∞"
                    item = QTableWidgetItem(str_val)
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setFlags(Qt.ItemIsEnabled) # No editable
                    
                    # Coloreo lógico
                    if str_val == "∞":
                        item.setForeground(QColor("#d9534f")) # Rojo suave
                    elif str_val == "0":
                        item.setForeground(QColor("#adb5bd")) # Gris
                    else:
                        item.setForeground(QColor("#1b4332")) # Verde oscuro
                        
                    t.setItem(r, c, item)
            card_lay.addWidget(t); self.res_layout.addWidget(card)
