from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from controlador.controlador_lineal import ControladorBusquedaLineal


class VistaBusquedaLineal(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # === TÍTULO INTERNO ===
        lbl_titulo = QLabel("Búsqueda Lineal / Secuencial")
        lbl_titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #1b4332; margin-bottom: 10px;")
        layout.addWidget(lbl_titulo)

        # === PANEL DE CONFIGURACIÓN ===
        top_panel = QFrame()
        top_panel.setStyleSheet("background: white; border-radius: 15px; border: 1px solid #d8e3dc;")
        top_layout = QVBoxLayout(top_panel)
        
        config_layout = QHBoxLayout()
        self.input_rango = QLineEdit()
        self.input_rango.setPlaceholderText("Ej: 10")
        self.input_rango.setFixedWidth(100)
        self.input_rango.setStyleSheet("padding: 8px; border: 1px solid #40916c; border-radius: 5px;")

        self.spin_digitos = QSpinBox()
        self.spin_digitos.setRange(1, 10)
        self.spin_digitos.setStyleSheet("padding: 5px; border: 1px solid #40916c; border-radius: 5px;")

        config_layout.addWidget(QLabel("Cantidad de datos:"))
        config_layout.addWidget(self.input_rango)
        config_layout.addSpacing(20)
        config_layout.addWidget(QLabel("Nº de dígitos:"))
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
        self.btn_man_save = self.boton_accion("💾 Guardar")
        self.btn_man_load = self.boton_accion("📂 Recuperar")

        # Layout horizontal para los botones (sin estirar demasiado)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.addWidget(self.btn_crear)
        btn_layout.addWidget(self.btn_insertar)
        btn_layout.addWidget(self.btn_buscar)
        btn_layout.addWidget(self.btn_eliminar)
        btn_layout.addWidget(self.btn_deshacer)
        btn_layout.addWidget(self.btn_reset)
        btn_layout.addWidget(self.btn_man_save)
        btn_layout.addWidget(self.btn_man_load)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)

        # === TABLA Y SALIDA ===
        split_layout = QHBoxLayout()

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(2)
        self.tabla.setHorizontalHeaderLabels(["Posición", "Clave"])
        self.tabla.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #d8e3dc;
                border-radius: 10px;
                gridline-color: #f0f7f4;
            }
            QHeaderView::section {
                background-color: #2d6a4f;
                color: white;
                padding: 5px;
                font-weight: bold;
                border: none;
            }
        """)
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

        split_layout.addWidget(self.tabla, 2)
        split_layout.addWidget(self.salida, 3)
        layout.addLayout(split_layout)

        self.controlador = ControladorBusquedaLineal(self)
        self.btn_man_save.clicked.connect(self.manual_save)
        self.btn_man_load.clicked.connect(self.manual_load)
        self.btn_reset.clicked.connect(self.reset_estructura)

    def reset_estructura(self):
        self.controlador.modelo.limpiar()
        self.tabla.setRowCount(0)
        self.input_rango.clear()
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
            QPushButton:pressed {
                background-color: #1b4332;
            }
        """)
        return btn

    # ===== MÉTODOS VISUALES =====
    def crear_tabla(self, filas):
        self.tabla.setRowCount(filas)
        self.tabla.verticalHeader().setVisible(False)

        for i in range(filas):
            # Columna posición
            item_pos = QTableWidgetItem(str(i + 1))
            item_pos.setTextAlignment(Qt.AlignCenter)
            self.tabla.setItem(i, 0, item_pos)

            # Columna clave (vacía)
            self.tabla.setItem(i, 1, QTableWidgetItem(""))

    def actualizar_tabla(self, datos):
        self.tabla.clearContents()

        for i in range(self.tabla.rowCount()):
            # Posición
            item_pos = QTableWidgetItem(str(i + 1))
            item_pos.setTextAlignment(Qt.AlignCenter)
            self.tabla.setItem(i, 0, item_pos)

            # Clave (si existe)
            if i < len(datos):
                self.tabla.setItem(i, 1, QTableWidgetItem(datos[i]))
            else:
                self.tabla.setItem(i, 1, QTableWidgetItem(""))

    def resaltar_fila(self, fila):
        self.tabla.selectRow(fila)

    def mensaje(self, texto):
        self.salida.clear()          # borra mensajes anteriores
        self.salida.setText(f"> {texto}")

