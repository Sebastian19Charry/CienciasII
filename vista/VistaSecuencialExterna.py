from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from controlador.ControladorSecuencialExterna import ControladorSecuencialExterna

class VistaSecuencialExterna(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        # === TÍTULO ===
        lbl_titulo = QLabel("Búsqueda Secuencial Externa (Por Bloques)")
        lbl_titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #1b4332;")
        layout.addWidget(lbl_titulo)

        # === CONFIGURACIÓN ===
        top_panel = QFrame()
        top_panel.setStyleSheet("background: white; border-radius: 15px; border: 1px solid #d8e3dc;")
        t_layout = QHBoxLayout(top_panel)
        
        self.input_rango = QLineEdit("20")
        self.input_rango.setFixedWidth(50)
        
        self.spin_digitos = QSpinBox()
        self.spin_digitos.setRange(1, 10)
        self.spin_digitos.setValue(2)

        self.spin_bloque = QSpinBox()
        self.spin_bloque.setRange(1, 10)
        self.spin_bloque.setValue(5) # Por defecto 5

        t_layout.addWidget(QLabel("Cantidad de Registros:"))
        t_layout.addWidget(self.input_rango)
        t_layout.addSpacing(20)
        t_layout.addWidget(QLabel("Nº dígitos:"))
        t_layout.addWidget(self.spin_digitos)
        t_layout.addSpacing(20)
        t_layout.addStretch()
        layout.addWidget(top_panel)

        # === BOTONES ===
        btn_layout = QHBoxLayout()
        self.btn_crear = self.boton_accion("➕ Crear Archivo")
        self.btn_insertar = self.boton_accion("📥 Insertar")
        self.btn_buscar = self.boton_accion("🔍 Buscar")
        self.btn_eliminar = self.boton_accion("🗑️ Eliminar")
        self.btn_reset = self.boton_accion("♻️ Limpiar")
        self.btn_guardar = self.boton_accion("💾 Guardar")
        self.btn_abrir = self.boton_accion("📂 Recuperar")
        
        for b in [self.btn_crear, self.btn_insertar, self.btn_buscar, 
                  self.btn_reset, self.btn_eliminar, self.btn_guardar, self.btn_abrir]:
            btn_layout.addWidget(b)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # === TABLA Y CONSOLA ===
        split = QHBoxLayout()
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(2) # Bloque y Contenido
        self.tabla.setHorizontalHeaderLabels(["Bloque / Posición", "Contenido del Archivo"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.salida = QTextEdit()
        self.salida.setReadOnly(True)
        self.salida.setStyleSheet("background: #f8fcf9; color: #1b4332; font-family: Consolas; border-radius: 10px;")

        split.addWidget(self.tabla, 3)
        split.addWidget(self.salida, 2)
        layout.addLayout(split)

        # Iniciar controlador y conectar
        self.controlador = ControladorSecuencialExterna(self)
        self.btn_crear.clicked.connect(self.controlador.crear)
        self.btn_insertar.clicked.connect(self.controlador.insertar)
        self.btn_buscar.clicked.connect(self.controlador.buscar)
        self.btn_eliminar.clicked.connect(self.controlador.eliminar)
        self.btn_reset.clicked.connect(self.controlador.limpiar)
        self.btn_guardar.clicked.connect(self.controlador.guardar_archivo)
        self.btn_abrir.clicked.connect(self.controlador.abrir_archivo)

    def boton_accion(self, t, color="#2d6a4f"):
        btn = QPushButton(t)
        btn.setFixedHeight(35)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"background: {color}; color: white; font-weight: bold; border-radius: 8px; padding: 0 15px;")
        return btn

    def crear_tabla(self, filas_totales):
        tam_bloque = self.spin_bloque.value()
        num_bloques = (filas_totales + tam_bloque - 1) // tam_bloque
        self.tabla.setRowCount(num_bloques)
        for i in range(num_bloques):
            item_bloque = QTableWidgetItem(f"Bloque {i + 1}")
            item_bloque.setBackground(QColor("#2d6a4f"))
            item_bloque.setForeground(QColor("white"))
            item_bloque.setTextAlignment(Qt.AlignCenter)
            self.tabla.setItem(i, 0, item_bloque)
            self.tabla.setItem(i, 1, QTableWidgetItem(""))

    def actualizar_tabla(self, datos, tam_bloque):
        # Limpiar columnas de datos
        for i in range(self.tabla.rowCount()):
            self.tabla.setItem(i, 1, QTableWidgetItem(""))

        # Agrupar datos en formato: "10 | 20 | 30"
        for idx, clave in enumerate(datos):
            n_bloque = idx // tam_bloque
            if n_bloque < self.tabla.rowCount():
                item = self.tabla.item(n_bloque, 1)
                txt = item.text()
                nuevo_txt = f"{txt} | {clave}" if txt else clave
                self.tabla.setItem(n_bloque, 1, QTableWidgetItem(nuevo_txt))

    def resaltar_fila(self, fila):
        self.tabla.selectRow(fila)

    def mensaje(self, txt):
        self.salida.setText(f"<b>SISTEMA></b><br><br>{txt}")