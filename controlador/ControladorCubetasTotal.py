from PySide6.QtWidgets import QInputDialog, QMessageBox, QFileDialog

class ControladorCubetasTotal:
    def __init__(self, vista):
        self.vista = vista
        from modelo.ModeloCubetasTotal import ModeloCubetasTotal
        self.modelo = ModeloCubetasTotal()

    def crear(self):
        k = self.vista.spin_reg_cubeta.value()
        self.modelo.crear(k)
        self.actualizar_interfaz(f"Estructura inicializada con K={k}")

    def insertar(self):
        clave, ok = QInputDialog.getText(self.vista, "Insertar", "Clave:")
        if ok and clave:
            exito, msg = self.modelo.insertar(clave.strip())
            self.actualizar_interfaz(msg) if exito else QMessageBox.warning(self.vista, "Error", msg)

    def eliminar(self):
        clave, ok = QInputDialog.getText(self.vista, "Eliminar", "Clave:")
        if ok and clave:
            exito, msg = self.modelo.eliminar(clave.strip())
            self.actualizar_interfaz(msg) if exito else QMessageBox.warning(self.vista, "Error", msg)

    def buscar(self):
        clave, ok = QInputDialog.getText(self.vista, "Buscar", "Clave:")
        if ok and clave:
            tipo, cubeta, pos = self.modelo.buscar(clave.strip())
            if tipo == "principal":
                self.vista.resaltar_celda(cubeta, pos)
                self.vista.mensaje(f"🔍 Encontrada en Cubeta {cubeta}")
            else:
                self.vista.mensaje("No encontrada o en colisión.")

    def limpiar(self):
        self.modelo.crear(self.vista.spin_reg_cubeta.value())
        self.actualizar_interfaz("🧹 Limpiado")

    def guardar(self):
        ruta, _ = QFileDialog.getSaveFileName(self.vista, "Guardar JSON", "", "JSON (*.json)")
        if ruta:
            if self.modelo.guardar_datos(ruta):
                self.vista.mensaje(f"💾 Guardado en: {ruta}")

    def recuperar(self):
        ruta, _ = QFileDialog.getOpenFileName(self.vista, "Cargar JSON", "", "JSON (*.json)")
        if ruta:
            if self.modelo.cargar_datos(ruta):
                self.vista.spin_reg_cubeta.setValue(self.modelo.reg_por_cubeta)
                self.actualizar_interfaz("📂 Recuperado")

    def actualizar_interfaz(self, msg):
        self.vista.actualizar_tabla(self.modelo.datos, self.modelo.colisiones, self.modelo.num_cubetas, self.modelo.reg_por_cubeta)
        self.vista.mensaje(msg)