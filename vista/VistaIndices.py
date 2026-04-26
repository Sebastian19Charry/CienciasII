from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QLineEdit, QTableWidget, QTableWidgetItem,
    QScrollArea, QGroupBox, QGridLayout, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QColor, QFont
import math

class IndiceCanvas(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setMinimumHeight(550)
        self.datos = None

    def actualizar_dibujo(self, datos):
        self.datos = datos
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if not self.datos:
            painter.drawText(self.rect(), Qt.AlignCenter, "Ingrese datos y presione Calcular")
            return

        # Estilos basados en tu interfaz
        pen_borde = QPen(QColor("#1b4332"), 2) 
        pen_lineas = QPen(QColor("#a68a64"), 1)
        painter.setFont(QFont("Arial", 9, QFont.Bold))

        # Configuración de posiciones
        x_idx, x_pri = 60, 380
        y_ini, ancho, alto_rect = 80, 200, 380

        # --- ESTRUCTURA ÍNDICE ---
        painter.setPen(pen_borde)
        painter.drawText(x_idx + 50, y_ini - 20, f"Índice {self.datos['tipo']}")
        painter.drawRect(x_idx, y_ini, ancho, alto_rect)
        # Bloques de índice
        painter.drawRect(x_idx, y_ini + 10, ancho, 40)
        painter.drawText(x_idx + 85, y_ini + 35, "B1")
        painter.drawRect(x_idx, y_ini + alto_rect - 50, ancho, 40)
        painter.drawText(x_idx + 75, y_ini + alto_rect - 25, f"B{self.datos['bloques_idx']}")

        # --- ESTRUCTURA PRINCIPAL ---
        painter.drawText(x_pri + 70, y_ini - 20, "Archivo Principal")
        painter.drawRect(x_pri, y_ini, ancho, alto_rect)
        # Bloques de datos
        painter.drawRect(x_pri, y_ini + 5, ancho, 50)
        painter.drawText(x_pri + 85, y_ini + 35, "B1")
        painter.drawRect(x_pri, y_ini + alto_rect - 55, ancho, 50)
        painter.drawText(x_pri + 75, y_ini + alto_rect - 25, f"B{self.datos['bloques_dat']}")

        # --- CONECTORES ---
        painter.setPen(pen_lineas)
        # Conexión superior
        painter.drawLine(x_idx + ancho, y_ini + 30, x_pri, y_ini + 30)
        # Conexión inferior
        painter.drawLine(x_idx + ancho, y_ini + alto_rect - 30, x_pri, y_ini + alto_rect - 30)

        # --- ETIQUETAS LATERALES ---
        painter.setPen(Qt.black)
        # Registros en principal
        painter.drawText(x_pri - 30, y_ini + 40, str(self.datos['rpb']))
        painter.drawText(x_pri - 50, y_ini + alto_rect - 5, str(self.datos['n']))

class VistaIndices(QWidget):
    def __init__(self, main_window, parent_window=None):
        super().__init__()
        self.main_window = main_window
        self.parent_window = parent_window
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #f0f7f4;") # Tu fondo claro
        layout = QVBoxLayout(self)

        # Header con botón Volver
        header = QHBoxLayout()
        btn_volver = QPushButton(" ⬅  Volver")
        btn_volver.setFixedSize(120, 40)
        btn_volver.setStyleSheet("background-color: #1b4332; color: white; border-radius: 5px; font-weight: bold;")
        btn_volver.clicked.connect(self.volver_atras)
        
        titulo = QLabel("SIMULACIÓN DE ÍNDICES")
        titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #1b4332; margin-left: 20px;")
        header.addWidget(btn_volver)
        header.addWidget(titulo)
        header.addStretch()
        layout.addLayout(header)

        # Visualización y Tabla
        body = QHBoxLayout()
        self.canvas = IndiceCanvas(self.main_window)
        scroll = QScrollArea()
        scroll.setWidget(self.canvas)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: 2px solid #1b4332; background: white;")

        self.tabla = QTableWidget(0, 3)
        self.tabla.setHorizontalHeaderLabels(["N. Est", "Variable", "Valor"])
        self.tabla.setFixedWidth(320)
        self.tabla.setStyleSheet("QHeaderView::section { background-color: #1b4332; color: white; }")
        
        body.addWidget(scroll, 3)
        body.addWidget(self.tabla, 1)
        layout.addLayout(body)

        # Controles Inferiores
        controls = QGroupBox("Parámetros de Entrada")
        controls.setStyleSheet("color: #1b4332; font-weight: bold;")
        grid = QGridLayout(controls)

        self.cb_tipo = QComboBox(); self.cb_tipo.addItems(["Primario", "Secundario"])
        self.cb_niveles = QComboBox(); self.cb_niveles.addItems(["Un Nivel", "Multinivel"])
        self.txt_bloque = QLineEdit("1024")
        self.txt_regs = QLineEdit("700000")
        self.txt_tam_reg = QLineEdit("20")
        self.txt_tam_ind = QLineEdit("12")

        # Layout de inputs
        inputs = [
            ("Tipo de Índice:", self.cb_tipo), ("Niveles:", self.cb_niveles), ("Tamaño Bloque (B):", self.txt_bloque),
            ("Cant. Registros (N):", self.txt_regs), ("Tam. Registro (R):", self.txt_tam_reg), ("Tam. Entrada Índice (V+P):", self.txt_tam_ind)
        ]
        for i, (lab, widget) in enumerate(inputs):
            grid.addWidget(QLabel(lab), i // 3, (i % 3) * 2)
            grid.addWidget(widget, i // 3, (i % 3) * 2 + 1)
            widget.setStyleSheet("background: white; color: black; border: 1px solid #1b4332; padding: 5px;")

        layout.addWidget(controls)

        self.btn_calc = QPushButton("🚀 CALCULAR Y GRAFICAR")
        self.btn_calc.setFixedHeight(50)
        self.btn_calc.setStyleSheet("background-color: #2d6a4f; color: white; font-weight: bold; font-size: 16px;")
        self.btn_calc.clicked.connect(self.ejecutar_logica)
        layout.addWidget(self.btn_calc)

    def ejecutar_logica(self):
        try:
            B = int(self.txt_bloque.text())
            n = int(self.txt_regs.text())
            r = int(self.txt_tam_reg.text())
            si = int(self.txt_tam_ind.text())
            tipo = self.cb_tipo.currentText()

            # --- LÓGICA DE CÁLCULO ---
            rpb = B // r # Registros por bloque
            bloques_dat = math.ceil(n / rpb)
            fbi = B // si # Entradas de índice por bloque

            if tipo == "Primario":
                # Un índice primario suele ser disperso: 1 entrada por BLOQUE de datos
                cant_entradas_idx = bloques_dat
            else:
                # Un índice secundario es denso: 1 entrada por cada REGISTRO
                cant_entradas_idx = n

            bloques_idx = math.ceil(cant_entradas_idx / fbi)

            # Actualizar Tabla
            self.tabla.setRowCount(0)
            res = [
                ("1", "Cant. Registros", n), ("1", "Reg. x Bloque", rpb), ("1", "Total Bloques Data", bloques_dat),
                ("2", f"Entradas Índice ({tipo})", cant_entradas_idx), ("2", "Índices x Bloque", fbi), ("2", "Total Bloques Índice", bloques_idx)
            ]
            for nest, var, val in res:
                row = self.tabla.rowCount()
                self.tabla.insertRow(row)
                for i, item in enumerate([nest, var, str(val)]):
                    self.tabla.setItem(row, i, QTableWidgetItem(item))

            self.canvas.actualizar_dibujo({
                'tipo': tipo, 'n': n, 'rpb': rpb, 'bloques_dat': bloques_dat,
                'fbi': fbi, 'bloques_idx': bloques_idx
            })

        except ValueError:
            QMessageBox.warning(self, "Error", "Asegúrate de ingresar solo números enteros.")

    def volver_atras(self):
        if self.parent_window:
            self.main_window.cambiar_pantalla(self.parent_window)
        else:
            self.main_window.volver_inicio()