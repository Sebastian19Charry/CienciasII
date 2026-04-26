from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QLineEdit, QTableWidget, QTableWidgetItem,  # <--- Agregar aquí
    QScrollArea, QGroupBox, QMessageBox, QFrame
)

class ControladorIndices:
    def __init__(self, vista, modelo):
        self.vista = vista
        self.modelo = modelo
        self.vista.btn_generar.clicked.connect(self.procesar)

    def procesar(self):
        try:
            # Obtener datos de la vista
            tipo = self.vista.cb_tipo.currentText()
            niveles = self.vista.cb_niveles.currentText()
            b = int(self.vista.txt_bloque.text())
            r = int(self.vista.txt_regs.text())
            tr = int(self.vista.txt_tam_reg.text())
            tri = int(self.vista.txt_tam_ind.text())

            # Calcular en el modelo
            resultados, cant_est = self.modelo.calcular_indices(tipo, niveles, b, r, tr, tri)

            # Actualizar Tabla
            self.vista.tabla.setRowCount(0)
            for fila in resultados:
                row_pos = self.vista.tabla.rowCount()
                self.vista.tabla.insertRow(row_pos)
                for i, valor in enumerate(fila):
                    self.vista.tabla.setItem(row_pos, i, QTableWidgetItem(str(valor)))

            # Actualizar Canvas
            datos_dibujo = {
                'tipo': tipo,
                'cant_estructuras': cant_est,
                'resultados': resultados
            }
            self.vista.canvas.actualizar_dibujo(datos_dibujo)

        except ValueError:
            QMessageBox.critical(self.vista, "Error", "Por favor ingrese solo números en los campos de tamaño.")