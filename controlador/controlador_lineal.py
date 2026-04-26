from modelo.modelo_lineal import ModeloBusquedaLineal
from modelo.manejador_archivos import ManejadorArchivos
from PySide6.QtWidgets import QInputDialog, QMessageBox


class ControladorBusquedaLineal:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = ModeloBusquedaLineal()
        self.ruta_archivo = "data/lineal.json"
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
            cantidad = int(self.vista.input_rango.text())
            digitos = self.vista.spin_digitos.value()
        except ValueError:
            self.error("Debe ingresar valores válidos")
            return

        self.modelo.crear(cantidad, digitos)
        self.vista.crear_tabla(cantidad)
        self.vista.mensaje("Estructura creada")
        self.guardar()

    def insertar(self):
        clave, ok = QInputDialog.getText(
            self.vista,
            "Insertar clave",
            f"Ingrese clave de {self.modelo.digitos} dígitos"
        )
        if not ok:
            return

        ok, msg = self.modelo.insertar(clave)
        if not ok:
            self.error(msg)
            return

        self.vista.actualizar_tabla(self.modelo.datos)
        self.vista.mensaje(msg)
        self.guardar()

    def buscar(self):
        clave, ok = QInputDialog.getText(self.vista, "Buscar", "Clave:")
        if not ok:
            return

        ok, pos = self.modelo.buscar(clave)
        if ok:
            self.vista.resaltar_fila(pos)
            self.vista.mensaje(f"Clave encontrada en posición {pos + 1}")
        else:
            self.error("La clave no fue encontrada")

    def eliminar(self):
        clave, ok = QInputDialog.getText(self.vista, "Eliminar", "Clave:")
        if not ok:
            return

        ok, msg = self.modelo.eliminar(clave)
        if not ok:
            self.error(msg)
            return

        self.vista.actualizar_tabla(self.modelo.datos)
        self.vista.mensaje(msg)
        self.guardar()

    def deshacer(self):
        if self.modelo.deshacer():
            self.vista.actualizar_tabla(self.modelo.datos)
            self.vista.mensaje("Última acción deshecha")
            self.guardar()
        else:
            self.error("No hay acciones para deshacer")

    def guardar(self):
        ManejadorArchivos.guardar_json(self.ruta_archivo, self.modelo.to_dict())

    def cargar(self):
        datos = ManejadorArchivos.leer_json(self.ruta_archivo)
        if datos:
            self.modelo.from_dict(datos)
            self.vista.crear_tabla(self.modelo.max_size)
            self.vista.actualizar_tabla(self.modelo.datos)
            self.vista.input_rango.setText(str(self.modelo.max_size))
            self.vista.spin_digitos.setValue(self.modelo.digitos)

    def error(self, mensaje):
        QMessageBox.critical(
            self.vista,
            "Error",
            mensaje,
            QMessageBox.Ok
        )
