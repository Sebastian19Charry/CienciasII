from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from controlador.controlador_hash import ControladorHash

class VistaHash(QWidget):
    def __init__(self, main_window, metodo):
        super().__init__()
        self.main_window = main_window
        self.metodo = metodo

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # === TÍTULO ===
        lbl_titulo = QLabel(metodo)
        lbl_titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #1b4332; margin-bottom: 10px;")
        layout.addWidget(lbl_titulo)

        # === PANEL CONFIGURACIÓN ===
        top_panel = QFrame()
        top_panel.setStyleSheet("background: white; border-radius: 15px; border: 1px solid #d8e3dc;")
        top_layout = QVBoxLayout(top_panel)
        
        config_layout = QHBoxLayout()
        self.input_capacidad = QLineEdit()
        self.input_capacidad.setPlaceholderText("Ej: 10")
        self.input_capacidad.setFixedWidth(100)
        self.input_capacidad.setStyleSheet("padding: 8px; border: 1px solid #40916c; border-radius: 5px;")

        self.spin_digitos = QSpinBox()
        self.spin_digitos.setRange(1, 10)
        self.spin_digitos.setStyleSheet("padding: 5px; border: 1px solid #40916c; border-radius: 5px;")

        config_layout.addWidget(QLabel("Capacidad:"))
        config_layout.addWidget(self.input_capacidad)
        config_layout.addSpacing(20)
        config_layout.addWidget(QLabel("Nº dígitos:"))
        config_layout.addWidget(self.spin_digitos)
        config_layout.addStretch()
        
        top_layout.addLayout(config_layout)
        layout.addWidget(top_panel)

        # === BOTONES ===
        self.btn_crear = self.boton_accion("➕ Crear")
        self.btn_insertar = self.boton_accion("📥 Insertar")
        self.btn_buscar = self.boton_accion("🔍 Buscar")
        self.btn_eliminar = self.boton_accion("🗑️ Eliminar")
        self.btn_deshacer = self.boton_accion("↶ Deshacer")
        self.btn_reset = self.boton_accion("♻️ Limpiar")
        self.btn_manual_save = self.boton_accion("💾 Guardar")
        self.btn_manual_load = self.boton_accion("📂 Recuperar")

        # Layout horizontal para los botones
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.addWidget(self.btn_crear)
        btn_layout.addWidget(self.btn_insertar)
        btn_layout.addWidget(self.btn_buscar)
        btn_layout.addWidget(self.btn_eliminar)
        btn_layout.addWidget(self.btn_deshacer)
        btn_layout.addWidget(self.btn_reset)
        btn_layout.addWidget(self.btn_manual_save)
        btn_layout.addWidget(self.btn_manual_load)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)

        # === TABLA Y LOG ===
        split_layout = QHBoxLayout()

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(2)
        self.tabla.setHorizontalHeaderLabels(["Posición", "Claves / Lista"])
        self.tabla.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #d8e3dc;
                border-radius: 10px;
            }
            QHeaderView::section {
                background-color: #2d6a4f;
                color: white;
                padding: 5px;
                font-weight: bold;
                border: none;
            }
        """)
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.salida = QTextEdit()
        self.salida.setReadOnly(True)
        self.salida.setPlaceholderText("Logs del sistema...")
        self.salida.setStyleSheet("""
            QTextEdit {
                background: #f8fcf9;
                border: 1px solid #d8e3dc;
                border-radius: 10px;
                padding: 10px;
                color: #2d6a4f;
                font-family: 'Consolas', monospace;
            }
        """)

        split_layout.addWidget(self.tabla, 3)
        split_layout.addWidget(self.salida, 2)
        layout.addLayout(split_layout)

        # CONTROLADOR
        self.controlador = ControladorHash(self, metodo)
        self.conectar_botones()

    def conectar_botones(self):
        self.btn_crear.clicked.connect(self.controlador.crear)
        self.btn_insertar.clicked.connect(self.controlador.insertar)
        self.btn_buscar.clicked.connect(self.controlador.buscar)
        self.btn_eliminar.clicked.connect(self.controlador.eliminar)
        self.btn_deshacer.clicked.connect(self.controlador.deshacer)
        self.btn_manual_save.clicked.connect(self.manual_save)
        self.btn_manual_load.clicked.connect(self.manual_load)
        self.btn_reset.clicked.connect(self.reset_estructura)

    def reset_estructura(self):
        self.controlador.modelo.limpiar()
        self.tabla.setRowCount(0)
        self.input_capacidad.clear()
        self.spin_digitos.setValue(1)
        self.mensaje("Estructura y tabla eliminadas")
        self.controlador.guardar()

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

    def boton_accion(self, texto):
        btn = QPushButton(texto)
        btn.setFixedHeight(32)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #2d6a4f;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 4px 12px;
                font-size: 11px;
            }
            QPushButton:hover { background-color: #40916c; }
            QPushButton:pressed { background-color: #1b4332; }
        """)
        return btn

    def configurar_tabla(self, n):
        self.tabla.setRowCount(n)
        for i in range(n):
            self.tabla.setItem(i, 0, QTableWidgetItem(f"Pos {i+1}"))
            self.tabla.setItem(i, 1, QTableWidgetItem(""))
            self.tabla.item(i, 0).setTextAlignment(Qt.AlignCenter)

    def actualizar_tabla(self, datos, colisiones):
        for i in range(self.tabla.rowCount()):
            pos = i + 1
            primaria = datos.get(pos, "")
            extras = colisiones.get(pos, [])
            
            texto = primaria
            if extras:
                texto += " -> " + " -> ".join(extras)
            
            item = QTableWidgetItem(texto)
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.tabla.setItem(i, 1, item)

    def resaltar_fila(self, pos):
        self.tabla.selectRow(pos - 1)

    def mensaje(self, texto):
        self.salida.setText(f"> {texto}")


