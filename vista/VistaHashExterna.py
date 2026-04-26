from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from controlador.ControladorHashExterno import ControladorHashExterno

class VistaHashExterna(QWidget):
    def __init__(self, main_window, metodo):
        super().__init__()
        self.main_window = main_window
        self.metodo = metodo
        self.controlador = ControladorHashExterno(self, metodo)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Título dinámico
        self.lbl_titulo = QLabel(f"Función {self.metodo}")
        self.lbl_titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #1b4332;")
        layout.addWidget(self.lbl_titulo)

        # --- PANEL SUPERIOR CONFIGURACIÓN ---
        panel_config = QFrame()
        panel_config.setStyleSheet("background: white; border-radius: 10px; border: 1px solid #e0e0e0;")
        layout_config = QHBoxLayout(panel_config)
        
        self.input_capacidad = QLineEdit()
        self.input_capacidad.setPlaceholderText("Cant. datos")
        self.input_capacidad.setFixedWidth(120)
        
        self.spin_digitos = QSpinBox()
        self.spin_digitos.setRange(1, 10)

        layout_config.addWidget(QLabel("Cantidad de registros:"))
        layout_config.addWidget(self.input_capacidad)
        layout_config.addSpacing(20)
        layout_config.addWidget(QLabel("Nº dígitos:"))
        layout_config.addWidget(self.spin_digitos)
        layout_config.addStretch()
        layout.addWidget(panel_config)

        # --- FILA DE BOTONES DE ACCIÓN ---
        btn_layout = QHBoxLayout()
        self.btn_crear = self.crear_boton_accion("➕ Crear", "#2d6a4f")
        self.btn_insertar = self.crear_boton_accion("📥 Insertar", "#2d6a4f")
        self.btn_buscar = self.crear_boton_accion("🔍 Buscar", "#2d6a4f")
        self.btn_eliminar = self.crear_boton_accion("🗑️ Eliminar", "#2d6a4f")
        self.btn_deshacer = self.crear_boton_accion("↶ Deshacer", "#2d6a4f")
        self.btn_limpiar = self.crear_boton_accion("♻️ Limpiar", "#2d6a4f")
        self.btn_guardar = self.crear_boton_accion("💾 Guardar", "#2d6a4f")
        self.btn_recuperar = self.crear_boton_accion("📂 Recuperar", "#2d6a4f")

        for b in [self.btn_crear, self.btn_insertar, self.btn_buscar, self.btn_eliminar, 
                  self.btn_deshacer, self.btn_limpiar, self.btn_guardar, self.btn_recuperar]:
            btn_layout.addWidget(b)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # --- ÁREA CENTRAL (TABLA Y LOGS) ---
        central_layout = QHBoxLayout()
        
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(2)
        self.tabla.setHorizontalHeaderLabels(["Bloque / Posición", "Contenido del Archivo"])
        self.tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla.setStyleSheet("background: white; gridline-color: #d8e3dc; border: 1px solid #d8e3dc;")
        
        self.txt_logs = QTextEdit()
        self.txt_logs.setReadOnly(True)
        self.txt_logs.setPlaceholderText("Logs del sistema...")
        self.txt_logs.setFixedWidth(300)
        self.txt_logs.setStyleSheet("background: #fdfdfd; border: 1px solid #d8e3dc; color: #1b4332;")

        central_layout.addWidget(self.tabla, 7)
        central_layout.addWidget(self.txt_logs, 3)
        layout.addLayout(central_layout)

        # Conexiones
        self.btn_crear.clicked.connect(self.controlador.crear)
        self.btn_insertar.clicked.connect(self.controlador.insertar)
        self.btn_buscar.clicked.connect(self.controlador.buscar)
        self.btn_eliminar.clicked.connect(self.controlador.eliminar)
        self.btn_deshacer.clicked.connect(self.controlador.deshacer) # <--- Agregado
        self.btn_limpiar.clicked.connect(self.controlador.limpiar)   # <--- Agregado
        self.btn_guardar.clicked.connect(self.controlador.guardar)
        self.btn_recuperar.clicked.connect(self.controlador.recuperar)

    def crear_boton_accion(self, texto, color):
        btn = QPushButton(texto)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 5px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: #40916c; }}
        """)
        return btn

    def configurar_tabla(self, num_filas):
        self.tabla.setRowCount(num_filas)
        for i in range(num_filas):
            # i empieza en 0, así que ponemos i + 1 para que el usuario vea "Bloque 1"
            item_bloque = QTableWidgetItem(f"Bloque {i + 1}")
            
            item_bloque.setBackground(QColor("#2d6a4f")) 
            item_bloque.setForeground(QColor("white"))
            item_bloque.setTextAlignment(Qt.AlignCenter)
            
            self.tabla.setItem(i, 0, item_bloque)
            self.tabla.setItem(i, 1, QTableWidgetItem(""))

    def mensaje(self, texto):

        self.txt_logs.setText(f"> {texto}")

    def resaltar_fila(self, fila):
        self.tabla.selectRow(fila)
        self.tabla.scrollToItem(self.tabla.item(fila, 0))