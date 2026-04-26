from PySide6.QtWidgets import QMessageBox
from modelo.modelo_binaria import ModeloBusquedaBinaria
from modelo.manejador_archivos import ManejadorArchivos


class ControladorBusquedaBinaria:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = ModeloBusquedaBinaria()
        self.ruta_archivo = "data/binaria.json"
        self.conectar()
        self.cargar()

    def conectar(self):
        self.vista.btn_crear.clicked.connect(self.crear)
        self.vista.btn_insertar.clicked.connect(self.insertar)
        self.vista.btn_buscar.clicked.connect(self.buscar)
        self.vista.btn_eliminar.clicked.connect(self.eliminar)
        self.vista.btn_deshacer.clicked.connect(self.deshacer)

    def crear(self):
        try:
            n = int(self.vista.input_rango.text())
            d = self.vista.spin_digitos.value()
            if n <= 0: raise ValueError
        except:
            self.error("Ingrese una cantidad válida")
            return

        self.modelo.crear(n, d)
        self.vista.crear_tabla(n)
        self.vista.mensaje("Estructura creada")
        self.guardar()

    def insertar(self):
        digitos = self.vista.spin_digitos.value()
        valor, ok = self.vista.pedir_valor("Insertar clave")
        if not ok:
            return

        if not valor.isdigit() or len(valor) != digitos:
            self.error(f"La clave debe tener {digitos} dígitos")
            return

        ok, msg = self.modelo.insertar(valor)
        if not ok:
            self.error(msg)
            return

        self.vista.actualizar_tabla(self.modelo.datos)
        self.vista.mensaje(msg)
        self.guardar()

    def buscar(self):
        valor, ok = self.vista.pedir_valor("Buscar clave")
        if not ok:
            return

        pos = self.modelo.buscar(int(valor))
        if pos == -1:
            self.error("Clave no encontrada")
        else:
            self.vista.tabla.selectRow(pos)
            self.vista.mensaje(f"Clave encontrada en la posición {pos + 1}")

    def eliminar(self):
        valor, ok = self.vista.pedir_valor("Eliminar clave")
        if not ok:
            return

        ok, msg = self.modelo.eliminar(valor)
        if not ok:
            self.error(msg)
            return

        self.vista.actualizar_tabla(self.modelo.datos)
        self.vista.mensaje(msg)
        self.guardar()

    def deshacer(self):
        if self.modelo.deshacer():
            self.vista.actualizar_tabla(self.modelo.datos)
            self.vista.mensaje("Acción deshecha")
            self.guardar()
        else:
            self.error("No hay acciones para deshacer")

    def guardar(self):
        ManejadorArchivos.guardar_json(self.ruta_archivo, self.modelo.to_dict())

    def cargar(self):
        datos = ManejadorArchivos.leer_json(self.ruta_archivo)
        if datos:
            self.modelo.from_dict(datos)
            self.vista.crear_tabla(self.modelo.maximo)
            self.vista.actualizar_tabla(self.modelo.datos)
            self.vista.input_rango.setText(str(self.modelo.maximo))
            self.vista.spin_digitos.setValue(self.modelo.digitos)

    def error(self, msg):
        QMessageBox.critical(self.vista, "Error", msg)