from PySide6.QtWidgets import QInputDialog, QMessageBox 
from modelo.ModeloHashExterno import ModeloHashExterno
import json
from PySide6.QtWidgets import QInputDialog, QTableWidgetItem, QFileDialog
import json
from PySide6.QtWidgets import QInputDialog, QTableWidgetItem

class ControladorHashExterno:
    def __init__(self, vista, metodo):
        self.vista = vista
        self.metodo = metodo
        self.modelo = ModeloHashExterno()

    def crear(self):
        try:
            cap = int(self.vista.input_capacidad.text())
            dig = self.vista.spin_digitos.value()
            self.modelo.crear(cap, dig, self.metodo)
            self.vista.configurar_tabla(self.modelo.num_bloques)
            self.vista.mensaje(f"Estructura externa creada: {self.modelo.num_bloques} bloques.")
        except:
            self.vista.mensaje("Error: Ingrese una capacidad válida (número entero).")

    def insertar(self):
        clave, ok = QInputDialog.getText(self.vista, "Insertar", f"Ingrese clave ({self.modelo.digitos} dígitos):")
        if not ok or not clave: return

        # Validar longitud
        if len(clave) != self.modelo.digitos or not clave.isdigit():
            self.vista.mensaje(f"Error: La clave debe ser de {self.modelo.digitos} dígitos.")
            return

        res, msg, expl = self.modelo.insertar(clave)

        if msg == "COLISION":
            for p in expl: self.vista.mensaje(p)
            estrategias = ["Sondeo Lineal", "Sondeo Cuadrático", "Encadenamiento"]
            est, ok = QInputDialog.getItem(self.vista, "Bloque Lleno", 
                                          "Seleccione estrategia para el archivo:", estrategias, 0, False)
            if ok:
                res, msg, expl = self.modelo.insertar(clave, est)
            else: return

        for p in expl: self.vista.mensaje(p)
        if res: 
            self.actualizar_vista()
        else: 
            self.vista.mensaje(f"Error: {msg}")

    def eliminar(self):
        clave, ok = QInputDialog.getText(self.vista, "Eliminar", "Clave a eliminar:")
        if ok and clave:
            res, msg = self.modelo.eliminar(clave)
            self.vista.mensaje(msg)
            if res: self.actualizar_vista()

    def buscar(self):
        clave, ok = QInputDialog.getText(self.vista, "Buscar", "Clave a buscar:")
        if ok and clave:
            clave_str = str(clave).zfill(self.modelo.digitos)
            for i, lista in self.modelo.bloques.items():
                if clave_str in lista:
                    self.vista.mensaje(f"Clave {clave_str} encontrada en Bloque {i}")
                    self.vista.resaltar_fila(i - 1)
                    return
            self.vista.mensaje("Clave no encontrada en el archivo.")

    def deshacer(self):
        if self.modelo.deshacer():
            self.vista.mensaje("Acción deshecha correctamente.")
            self.actualizar_vista()
        else:
            self.vista.mensaje("No hay acciones para deshacer.")

    def actualizar_vista(self):
        for i in range(1, self.modelo.num_bloques + 1):
            datos = self.modelo.bloques[i]
            texto = " | ".join(datos)
            self.vista.tabla.setItem(i-1, 1, QTableWidgetItem(texto))

    # --- MÉTODOS QUE FALTABAN PARA EVITAR EL ERROR ---
    def guardar(self):
        if not self.modelo.bloques:
            self.vista.mensaje("No hay datos para guardar.")
            return

        # Abrir explorador de archivos
        ruta, _ = QFileDialog.getSaveFileName(
            self.vista,
            "Guardar Archivo Hash",
            "",
            "Archivos JSON (*.json)"
        )

        if ruta:
            try:
                # Si el usuario no puso .json, lo agregamos
                if not ruta.endswith('.json'):
                    ruta += '.json'
                
                datos = self.modelo.exportar_datos()
                with open(ruta, 'w', encoding='utf-8') as f:
                    json.dump(datos, f, indent=4, ensure_ascii=False)
                
                self.vista.mensaje(f"Archivo guardado en: {ruta}")
            except Exception as e:
                self.vista.mensaje(f"Error al guardar: {str(e)}")

    def recuperar(self):
        # Abrir explorador de archivos
        ruta, _ = QFileDialog.getOpenFileName(
            self.vista,
            "Abrir Archivo Hash",
            "",
            "Archivos JSON (*.json)"
        )

        if ruta:
            try:
                with open(ruta, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                
                self.modelo.importar_datos(datos)
                # Actualizar la vista con los datos cargados
                self.vista.configurar_tabla(self.modelo.num_bloques)
                self.actualizar_vista()
                self.vista.mensaje("Datos cargados correctamente.")
            except Exception as e:
                self.vista.mensaje(f"Error al cargar: {str(e)}")

    def limpiar(self):
        # Si el modelo tiene un método limpiar, lo llamas
        if hasattr(self.modelo, 'crear'):
            self.modelo.crear(self.modelo.capacidad_registros, self.modelo.digitos, self.metodo)
            self.actualizar_vista()
            self.vista.mensaje("Estructura reiniciada (limpia).")