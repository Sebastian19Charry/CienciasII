from PySide6.QtWidgets import QInputDialog, QMessageBox
from modelo.modelo_hash import ModeloHash
from modelo.manejador_archivos import ManejadorArchivos

class ControladorHash:
    def __init__(self, vista, metodo):
        self.vista = vista
        self.metodo = metodo
        self.modelo = ModeloHash()
        self.ruta_archivo = f"data/hash_{metodo.replace(' ', '_').lower()}.json"
        self.cargar()
        
    def crear(self):
        try:
            n = int(self.vista.input_capacidad.text())
            d = self.vista.spin_digitos.value()
            if n <= 0: raise ValueError
        except:
            self.vista.mensaje("Error: Capacidad debe ser un entero positivo")
            return

        self.modelo.crear(n, d, self.metodo)
        self.vista.configurar_tabla(n)
        self.vista.mensaje(f"Estructura creada ({self.metodo})")
        self.guardar()

    def insertar(self):
        clave, ok = QInputDialog.getText(self.vista, "Insertar", f"Ingrese clave ({self.modelo.digitos} dígitos):")
        if not ok or not clave: return

        if not clave.isdigit() or len(clave) != self.modelo.digitos:
            self.vista.mensaje(f"Error: La clave debe tener {self.modelo.digitos} dígitos")
            return

        res, msg, expl = self.modelo.insertar(clave)
        
        if msg == "COLISION":
            for paso in expl: self.vista.mensaje(paso)
            estrategias = ["Sondeo Lineal", "Sondeo Cuadrático", "Doble Hash", "Encadenamiento"]
            est, ok = QInputDialog.getItem(self.vista, "Colisión detectada", 
                                          "Seleccione estrategia de resolución:", estrategias, 0, False)
            if ok:
                res, msg, expl = self.modelo.insertar(clave, est)
            else:
                return

        for paso in expl: self.vista.mensaje(paso)
        
        if res:
            self.actualizar_vista()
            self.guardar()
        else:
            self.vista.mensaje(f"Error: {msg}")

    def buscar(self):
        clave, ok = QInputDialog.getText(self.vista, "Buscar", "Ingrese clave:")
        if not ok or not clave: return
        
        self.vista.mensaje(f"--- Buscando clave {clave} ---")
        encontrado, pos, tipo = self.modelo.buscar(clave)
        if encontrado:
            self.vista.mensaje(f"Clave encontrada en posición {pos} ({tipo})")
            self.vista.resaltar_fila(pos)
        else:
            self.vista.mensaje("Clave no encontrada")

    def eliminar(self):
        clave, ok = QInputDialog.getText(self.vista, "Eliminar", "Ingrese clave:")
        if not ok or not clave: return

        res, msg = self.modelo.eliminar(clave)
        if res:
            self.vista.mensaje(msg)
            self.actualizar_vista()
            self.guardar()
        else:
            self.vista.mensaje(f"Error: {msg}")

    def deshacer(self):
        if self.modelo.deshacer():
            self.vista.mensaje("Última acción deshecha")
            self.actualizar_vista()
            self.guardar()
        else:
            self.vista.mensaje("No hay más acciones para deshacer")

    def guardar(self):
        ManejadorArchivos.guardar_json(self.ruta_archivo, self.modelo.to_dict())

    def cargar(self):
        datos = ManejadorArchivos.leer_json(self.ruta_archivo)
        if datos:
            self.modelo.from_dict(datos)
            self.vista.input_capacidad.setText(str(self.modelo.capacidad))
            self.vista.spin_digitos.setValue(self.modelo.digitos)
            self.vista.configurar_tabla(self.modelo.capacidad)
            self.actualizar_vista()

    def actualizar_vista(self):
        self.vista.actualizar_tabla(self.modelo.datos, self.modelo.colisiones)
