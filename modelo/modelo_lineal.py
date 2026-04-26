class ModeloBusquedaLineal:
    def __init__(self):
        self.datos = []
        self.max_size = 0
        self.digitos = 0
        self.historial = []

    def crear(self, cantidad, digitos):
        self.max_size = cantidad
        self.digitos = digitos
        self.datos = []
        self.historial.clear()

    def validar_clave(self, clave):
        if not clave.isdigit():
            return False, "La clave debe ser numérica"
        if len(clave) != self.digitos:
            return False, f"La clave debe tener {self.digitos} dígitos"
        if clave in self.datos:
            return False, "La clave ya existe"
        return True, ""

    def insertar(self, clave):
        valido, msg = self.validar_clave(clave)
        if not valido:
            return False, msg

        if len(self.datos) >= self.max_size:
            return False, "La estructura está llena"

        self.historial.append(self.datos.copy())
        self.datos.append(clave)
        self.datos.sort(key=int)
        return True, "Clave insertada correctamente"

    def buscar(self, clave):
        for i, v in enumerate(self.datos):
            if v == clave:
                return True, i
        return False, -1

    def eliminar(self, clave):
        if clave in self.datos:
            self.historial.append(self.datos.copy())
            self.datos.remove(clave)
            return True, "Clave eliminada"
        return False, "La clave no existe"

    def deshacer(self):
        if self.historial:
            self.datos = self.historial.pop()
            return True
        return False

    def limpiar(self):
        self.datos = []
        self.max_size = 0
        self.digitos = 0
        self.historial = []

    def to_dict(self):
        return {
            "datos": self.datos,
            "max_size": self.max_size,
            "digitos": self.digitos
        }

    def from_dict(self, data):
        self.datos = data.get("datos", [])
        self.max_size = data.get("max_size", 0)
        self.digitos = data.get("digitos", 0)
        self.historial.clear()
