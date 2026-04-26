from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

class VistaCubetasTotal(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        # 1. Importación e instancia del controlador
        from controlador.ControladorCubetasTotal import ControladorCubetasTotal
        self.controlador = ControladorCubetasTotal(self)
        
        # 2. Construir la interfaz
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        # --- TÍTULO ---
        lbl_titulo = QLabel("Expansión y Reducción Total (Cubetas)")
        lbl_titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #1b4332;")
        layout.addWidget(lbl_titulo)

        # --- PANEL SUPERIOR (SpinBox) ---
        top_panel = QFrame()
        t_layout = QHBoxLayout(top_panel)
        
        t_layout.addWidget(QLabel("Registros por Cubeta (K):"))
        self.spin_reg_cubeta = QSpinBox()
        self.spin_reg_cubeta.setRange(1, 20)
        self.spin_reg_cubeta.setValue(3)
        t_layout.addWidget(self.spin_reg_cubeta)
        t_layout.addStretch()
        layout.addWidget(top_panel)

        # --- BOTONES (Primero se crean) ---
        btn_layout = QHBoxLayout()
        self.btn_crear = self.boton_estilo("➕ Inicializar", "#2d6a4f")
        self.btn_insertar = self.boton_estilo("📥 Insertar", "#2d6a4f")
        self.btn_eliminar = self.boton_estilo("🗑️ Eliminar", "#2d6a4f")
        self.btn_buscar = self.boton_estilo("🔍 Buscar", "#2d6a4f")
        self.btn_limpiar = self.boton_estilo("🧹 Limpiar", "#52796f")
        self.btn_guardar = self.boton_estilo("💾 Guardar", "#1b4332")
        self.btn_recuperar = self.boton_estilo("📂 Recuperar", "#1b4332")

        # Se añaden al layout
        for b in [self.btn_crear, self.btn_insertar, self.btn_eliminar, 
                  self.btn_buscar, self.btn_limpiar, self.btn_guardar, self.btn_recuperar]:
            btn_layout.addWidget(b)
        layout.addLayout(btn_layout)

        # --- TABLA Y CONSOLA ---
        display_layout = QHBoxLayout()
        self.tabla = QTableWidget()
        self.salida = QTextEdit()
        self.salida.setReadOnly(True)
        self.salida.setStyleSheet("background: #f8fcf9; font-family: Consolas;")
        
        display_layout.addWidget(self.tabla, 3)
        display_layout.addWidget(self.salida, 2)
        layout.addLayout(display_layout)

        # --- CONEXIONES (Después de crear los objetos) ---
        self.btn_crear.clicked.connect(self.controlador.crear)
        self.btn_insertar.clicked.connect(self.controlador.insertar)
        self.btn_eliminar.clicked.connect(self.controlador.eliminar)
        self.btn_buscar.clicked.connect(self.controlador.buscar)
        self.btn_limpiar.clicked.connect(self.controlador.limpiar)
        self.btn_guardar.clicked.connect(self.controlador.guardar)
        self.btn_recuperar.clicked.connect(self.controlador.recuperar)

    def boton_estilo(self, texto, color):
        btn = QPushButton(texto)
        btn.setStyleSheet(f"background: {color}; color: white; font-weight: bold; border-radius: 5px; padding: 5px;")
        return btn

    def crear_tabla(self, num_cubetas):
        k = self.spin_reg_cubeta.value()
        self.tabla.setColumnCount(num_cubetas)
        self.tabla.setRowCount(k)
        self.tabla.setHorizontalHeaderLabels([f"Cubeta {i}" for i in range(num_cubetas)])
        for c in range(num_cubetas):
            self.tabla.horizontalHeader().setSectionResizeMode(c, QHeaderView.Stretch)
            for f in range(k):
                self.tabla.setItem(f, c, QTableWidgetItem("-"))

    def actualizar_tabla(self, datos_dict, colisiones, num_cubetas, k):
        self.crear_tabla(num_cubetas)
        for cubeta_idx, registros in datos_dict.items():
            for i, valor in enumerate(registros):
                if i < k:
                    item = QTableWidgetItem(str(valor))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QColor("#d8e3dc"))
                    self.tabla.setItem(i, cubeta_idx, item)
        if colisiones:
            self.mensaje(f"⚠️ <b>COLISIONES:</b> {colisiones}")

    def resaltar_celda(self, col, fila):
        item = self.tabla.item(fila, col)
        if item:
            item.setBackground(QColor("#ffeb3b"))
            self.tabla.scrollToItem(item)

    def mensaje(self, texto):
        self.salida.setHtml(f"<b>Estado:</b><br>{texto}")