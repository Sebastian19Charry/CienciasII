from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from controlador.ControladorBinariaExterna import ControladorBinariaExterna

class VistaBinariaExterna(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        # 1. Definir Layout Principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        # === TÍTULO ===
        lbl_titulo = QLabel("Búsqueda Binaria Externa (Acceso por Bloque)")
        lbl_titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #1b4332;")
        layout.addWidget(lbl_titulo)

        # === CONFIGURACIÓN ===
        top_panel = QFrame()
        top_panel.setStyleSheet("background: white; border-radius: 15px; border: 1px solid #d8e3dc;")
        t_layout = QHBoxLayout(top_panel)
        
        self.input_rango = QLineEdit("20")
        self.input_rango.setFixedWidth(60)
        
        self.spin_digitos = QSpinBox()
        self.spin_digitos.setRange(1, 10)
        self.spin_digitos.setValue(2)

        self.spin_bloque = QSpinBox()
        self.spin_bloque.setRange(1, 10)
        self.spin_bloque.setValue(5) # Valor solicitado: 5

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
        self.btn_eliminar = self.boton_accion("❌ Eliminar")
        self.btn_buscar = self.boton_accion("🔍 Buscar Binario")
        self.btn_reset = self.boton_accion("♻️ Limpiar")
        self.btn_guardar = self.boton_accion("💾 Guardar")
        self.btn_abrir = self.boton_accion("📂 Recuperar")
        
        for b in [self.btn_crear, self.btn_insertar, self.btn_eliminar, 
                  self.btn_buscar, self.btn_reset, self.btn_guardar, self.btn_abrir]:
            btn_layout.addWidget(b)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # === TABLA Y CONSOLA ===
        split = QHBoxLayout()
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["Bloque", "Posición", "Clave"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        self.salida = QTextEdit()
        self.salida.setReadOnly(True)
        self.salida.setPlaceholderText("Resultados de la búsqueda...")
        self.salida.setStyleSheet("background: #f8fcf9; color: #003049; font-family: Consolas; font-size: 13px; border-radius: 10px;")

        split.addWidget(self.tabla, 3)
        split.addWidget(self.salida, 2)
        layout.addLayout(split)

        # 2. INICIALIZAR CONTROLADOR
        self.controlador = ControladorBinariaExterna(self)

        # 3. CONECTAR SEÑALES (Si el controlador no lo hace en su __init__)
        self.btn_crear.clicked.connect(self.controlador.crear)
        self.btn_insertar.clicked.connect(self.controlador.insertar)
        self.btn_eliminar.clicked.connect(self.controlador.eliminar)
        self.btn_buscar.clicked.connect(self.controlador.buscar)
        self.btn_reset.clicked.connect(self.controlador.limpiar)
        self.btn_guardar.clicked.connect(self.controlador.guardar_archivo)
        self.btn_abrir.clicked.connect(self.controlador.abrir_archivo)

    def boton_accion(self, t, color="#2d6a4f"):
        btn = QPushButton(t)
        btn.setFixedHeight(35)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {color}; color: white; font-weight: bold; 
                border-radius: 8px; padding: 0 12px;
            }}
            QPushButton:hover {{ background: #40916c; }}
        """)
        return btn

    def crear_tabla(self, filas_totales):
        # Calculamos cuántas filas (bloques) mostrar
        # Si bloque_size es 5 y pides 20 registros, habrán 4 filas.
        tam_bloque = self.spin_bloque.value()
        num_bloques = (filas_totales + tam_bloque - 1) // tam_bloque
        
        self.tabla.setRowCount(num_bloques)
        self.tabla.setColumnCount(2) # Solo 2 columnas como en tu foto de Hash
        self.tabla.setHorizontalHeaderLabels(["Bloque / Posición", "Contenido del Archivo"])
        
        for i in range(num_bloques):
            item_bloque = QTableWidgetItem(f"Bloque {i + 1}")
            item_bloque.setBackground(QColor("#2d6a4f"))
            item_bloque.setForeground(QColor("white"))
            item_bloque.setTextAlignment(Qt.AlignCenter)
            self.tabla.setItem(i, 0, item_bloque)
            self.tabla.setItem(i, 1, QTableWidgetItem(""))

    def actualizar_tabla(self, datos, tam_bloque):
        # Limpiar contenido de la columna de datos
        for i in range(self.tabla.rowCount()):
            self.tabla.setItem(i, 1, QTableWidgetItem(""))

        # Agrupar los datos en sus respectivos bloques
        for idx, clave in enumerate(datos):
            num_bloque = idx // tam_bloque
            if num_bloque < self.tabla.rowCount():
                item_actual = self.tabla.item(num_bloque, 1)
                contenido_previo = item_actual.text() if item_actual else ""
                
                nuevo_texto = f"{contenido_previo} | {clave}" if contenido_previo else clave
                self.tabla.setItem(num_bloque, 1, QTableWidgetItem(nuevo_texto))
    def mensaje(self, txt):
        # setText para que no se acumule (como pediste)
        self.salida.setText(f"<b>SISTEMA></b><br>{txt}")

    def resaltar_fila(self, fila):
        self.tabla.selectRow(fila)
        self.tabla.scrollToItem(self.tabla.item(fila, 0))