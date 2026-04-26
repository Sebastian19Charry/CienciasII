import json
from PySide6.QtWidgets import QInputDialog, QMessageBox, QFileDialog

class ControladorSecuencialExterna:
    def __init__(self, vista):
        self.vista = vista
        from modelo.ModeloSecuencialExterna import ModeloSecuencialExterna
        self.modelo = ModeloSecuencialExterna()

    def crear(self):
        try:
            cant = int(self.vista.input_rango.text())
            dig = self.vista.spin_digitos.value()
            bloque = self.vista.spin_bloque.value()
            self.modelo.crear(cant, dig, bloque)
            self.vista.crear_tabla(cant)
            self.vista.actualizar_tabla([], bloque)
            self.vista.mensaje(f"Archivo creado: {cant} registros, bloques de {bloque}.")
        except:
            QMessageBox.critical(self.vista, "Error", "Datos de entrada inválidos.")

    def insertar(self):
        clave, ok = QInputDialog.getText(self.vista, "Insertar", "Clave:")
        if ok and clave:
            exito, msg = self.modelo.insertar(clave.strip())
            if exito:
                self.vista.actualizar_tabla(self.modelo.datos, self.modelo.bloque_size)
                self.vista.mensaje(msg)
            else:
                QMessageBox.warning(self.vista, "Atención", msg)

    def buscar(self):
        clave, ok = QInputDialog.getText(self.vista, "Buscar", "Clave a buscar:")
        if ok and clave:
            encontrado, pos_indice, num_bloque = self.modelo.buscar(clave)
            if encontrado:
                fila_bloque = pos_indice // self.modelo.bloque_size
                self.vista.resaltar_fila(fila_bloque)
                self.vista.mensaje(f"<font color='green'><b>¡ENCONTRADO!</b> En el <b>Bloque {num_bloque}</b></font>")
            else:
                self.vista.mensaje(f"<font color='red'>La clave {clave} no existe.</font>")

    def eliminar(self):
        if not self.modelo.datos:
            QMessageBox.warning(self.vista, "Atención", "El archivo está vacío.")
            return

        clave, ok = QInputDialog.getText(self.vista, "Eliminar Registro", "Ingrese clave a eliminar:")
        
        if ok and clave:
            exito, msg = self.modelo.eliminar(clave.strip())
            if exito:
                # Refrescamos la tabla con los datos restantes
                self.vista.actualizar_tabla(self.modelo.datos, self.modelo.bloque_size)
                self.vista.mensaje(msg)
            else:
                QMessageBox.warning(self.vista, "Error", msg)

    def guardar_archivo(self):
        path, _ = QFileDialog.getSaveFileName(self.vista, "Guardar JSON", "", "JSON (*.json)")
        if path:
            if not path.endswith('.json'): path += '.json'
            with open(path, 'w') as f:
                json.dump(self.modelo.to_dict(), f, indent=4)
            self.vista.mensaje(f"Archivo guardado en: {path}")

    def abrir_archivo(self):
        path, _ = QFileDialog.getOpenFileName(self.vista, "Abrir JSON", "", "JSON (*.json)")
        if path:
            with open(path, 'r') as f:
                data = json.load(f)
                self.modelo.from_dict(data)
            self.vista.crear_tabla(self.modelo.max_size)
            self.vista.actualizar_tabla(self.modelo.datos, self.modelo.bloque_size)
            self.vista.mensaje("Archivo cargado correctamente.")

    def limpiar(self):
        self.modelo.datos = []
        self.vista.actualizar_tabla([], self.modelo.bloque_size)
        self.vista.salida.clear()
        self.vista.mensaje("Sistema reiniciado.")