import json
from PySide6.QtWidgets import QInputDialog, QMessageBox, QFileDialog

class ControladorBinariaExterna:
    def __init__(self, vista):
        self.vista = vista
        from modelo.ModeloBinariaExterna import ModeloBinariaExterna
        self.modelo = ModeloBinariaExterna()

    def crear(self):
        try:
            cant = int(self.vista.input_rango.text())
            bloque = self.vista.spin_bloque.value()
            digitos = self.vista.spin_digitos.value()
            self.modelo.crear(cant, digitos, bloque)
            self.vista.crear_tabla(cant)
            self.vista.actualizar_tabla([], bloque) # Inicializa visualmente los bloques
            self.vista.mensaje(f"Archivo creado. {cant} registros, bloques de {bloque}.")
        except: 
            QMessageBox.critical(self.vista, "Error", "Verifique los datos de entrada.")

    def insertar(self):
        clave, ok = QInputDialog.getText(self.vista, "Insertar", f"Ingrese clave ({self.modelo.digitos} dígitos):")
        if ok and clave:
            valido, msg = self.modelo.insertar(clave)
            if valido:
                self.vista.actualizar_tabla(self.modelo.datos, self.modelo.bloque_size)
                self.vista.mensaje(msg)
            else: 
                QMessageBox.warning(self.vista, "Error", msg)

    def eliminar(self):
        clave, ok = QInputDialog.getText(self.vista, "Eliminar", "Clave a eliminar:")
        if ok and clave:
            valido, msg = self.modelo.eliminar(clave)
            if valido:
                self.vista.actualizar_tabla(self.modelo.datos, self.modelo.bloque_size)
                self.vista.mensaje(msg)
            else: 
                QMessageBox.warning(self.vista, "Error", msg)

    def buscar(self):
        clave, ok = QInputDialog.getText(self.vista, "Buscar Binario", "Clave:")
        if ok and clave:
            encontrado, pos_indice, log = self.modelo.buscar_binario_pasos(clave)
            self.vista.mensaje(log)
            if encontrado:
                # Calculamos en qué fila (bloque) está ese índice
                fila_bloque = pos_indice // self.modelo.bloque_size
                self.vista.resaltar_fila(fila_bloque)

    def guardar_archivo(self):
        path, _ = QFileDialog.getSaveFileName(self.vista, "Guardar JSON", "", "JSON (*.json)")
        if path:
            try:
                with open(path, 'w') as f: 
                    json.dump(self.modelo.to_dict(), f, indent=4)
                self.vista.mensaje(f"Guardado en: {path}")
            except Exception as e:
                QMessageBox.critical(self.vista, "Error", str(e))

    def abrir_archivo(self):
        path, _ = QFileDialog.getOpenFileName(self.vista, "Abrir JSON", "", "JSON (*.json)")
        if path:
            try:
                with open(path, 'r') as f: 
                    data = json.load(f)
                    self.modelo.from_dict(data)
                self.vista.crear_tabla(self.modelo.max_size)
                self.vista.actualizar_tabla(self.modelo.datos, self.modelo.bloque_size)
                self.vista.mensaje("Archivo cargado correctamente.")
            except Exception as e:
                QMessageBox.critical(self.vista, "Error", str(e))

    def limpiar(self):
        self.modelo.datos = []
        self.vista.actualizar_tabla([], self.modelo.bloque_size)
        self.vista.salida.clear()
        self.vista.mensaje("Sistema reiniciado.")