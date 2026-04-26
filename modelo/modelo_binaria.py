class ModeloBusquedaBinaria:
    def __init__(self):
        self.datos = []
        self.maximo = 0
        self.digitos = 0
        self.historial = []

    def crear(self, n, d=0):
        self.maximo = n
        self.digitos = d
        self.datos = []
        self.historial = []

    def _guardar_estado(self):
        self.historial.append(list(self.datos))
        if len(self.historial) > 10:
            self.historial.pop(0)

    def insertar(self, valor):
        if valor in self.datos or len(self.datos) >= self.maximo:
            return False, "Error al insertar"
        self._guardar_estado()
        self.datos.append(int(valor))
        self.datos.sort()
        return True, f"Clave {valor} insertada"

    def buscar(self, valor):
        low, high = 0, len(self.datos) - 1

        while low <= high:
            mid = (low + high) // 2
            if self.datos[mid] == valor:
                return mid
            elif valor < self.datos[mid]:
                high = mid - 1
            else:
                low = mid + 1

        return -1

    def eliminar(self, valor):
        val = int(valor)
        if val in self.datos:
            self._guardar_estado()
            self.datos.remove(val)
            return True, f"Clave {valor} eliminada"
        return False, "La clave no existe"

    def deshacer(self):
        if self.historial:
            self.datos = self.historial.pop()
            return True
        return False

    def limpiar(self):
        self.datos = []
        self.maximo = 0
        self.digitos = 0
        self.historial = []

    def to_dict(self):
        return {
            "datos": self.datos,
            "maximo": self.maximo
        }

    def from_dict(self, data):
        self.datos = data.get("datos", [])
        self.maximo = data.get("maximo", 0)