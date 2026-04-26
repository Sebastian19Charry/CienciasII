from PySide6.QtWidgets import QInputDialog, QMessageBox, QFileDialog

class ControladorCubetasParcial:
    def __init__(self, vista):
        self.vista = vista
        from modelo.ModeloCubetasParcial import ModeloCubetasParcial
        self.modelo = ModeloCubetasParcial()

    def crear(self):
        k = self.vista.spin_reg_cubeta.value()
        self.modelo.crear(k)
        self.actualizar_interfaz(f"Estructura Parcial iniciada con K={k}")

    def insertar(self):
        clave, ok = QInputDialog.getText(self.vista, "Insertar", "Clave:")
        if ok and clave:
            exito, msg = self.modelo.insertar(clave.strip())
            if exito: self.actualizar_interfaz(msg)
            else: QMessageBox.warning(self.vista, "Atención", msg)

    def eliminar(self):
        clave, ok = QInputDialog.getText(self.vista, "Eliminar", "Clave:")
        if ok and clave:
            exito, msg = self.modelo.eliminar(clave.strip())
            if exito: self.actualizar_interfaz(msg)

    def buscar(self):
        clave, ok = QInputDialog.getText(self.vista, "Buscar", "Clave:")
        if ok and clave:
            tipo, cubeta, pos = self.modelo.buscar(clave.strip())
            if tipo == "principal":
                self.vista.resaltar_celda(cubeta, pos)
                self.vista.mensaje(f"🔍 En Cubeta {cubeta}, pos {pos}")
            else: self.vista.mensaje("No encontrado.")

    def limpiar(self):
        self.modelo.crear(self.vista.spin_reg_cubeta.value())
        self.actualizar_interfaz("🧹 Limpiado")

    def guardar(self):
        ruta, _ = QFileDialog.getSaveFileName(self.vista, "Guardar", "", "JSON (*.json)")
        if ruta: self.modelo.guardar_datos(ruta)

    def recuperar(self):
        ruta, _ = QFileDialog.getOpenFileName(self.vista, "Cargar", "", "JSON (*.json)")
        if ruta and self.modelo.cargar_datos(ruta):
            self.vista.spin_reg_cubeta.setValue(self.modelo.reg_por_cubeta)
            self.actualizar_interfaz("📂 Cargado")

    def actualizar_interfaz(self, msg):
        self.vista.crear_tabla(self.modelo.num_cubetas)
        self.vista.actualizar_tabla(self.modelo.datos, self.modelo.colisiones, self.modelo.num_cubetas, self.modelo.reg_por_cubeta)
        self.vista.mensaje(msg)