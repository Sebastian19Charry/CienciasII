class ModeloSecuencialExterna:
    def __init__(self):
        self.datos = [] 
        self.max_size = 0
        self.digitos = 0
        self.bloque_size = 5 # Por defecto 5
        self.historial = []

    def crear(self, cantidad, digitos, tam_bloque):
        self.max_size = cantidad
        self.digitos = digitos
        self.bloque_size = tam_bloque
        self.datos = []
        self.historial.clear()

    def insertar(self, clave):
        if len(self.datos) >= self.max_size:
            return False, "Error: El archivo está lleno."
        if len(clave) != self.digitos:
            return False, f"Error: La clave debe tener {self.digitos} dígitos."
        if clave in self.datos:
            return False, f"Error: La clave '{clave}' ya existe."
        
        self.historial.append(self.datos.copy())
        self.datos.append(clave)
        self.datos.sort(key=int) # Mantenemos el orden secuencial
        return True, f"Éxito: Registro '{clave}' guardado."

    def buscar(self, clave):
        # Búsqueda secuencial simple
        for i, v in enumerate(self.datos):
            if v == clave:
                num_bloque = (i // self.bloque_size) + 1
                return True, i, num_bloque
        return False, -1, -1

    def eliminar(self, clave):
        if clave in self.datos:
            self.datos.remove(clave)
            # Al eliminar, el archivo sigue ordenado, no hace falta sort()
            return True, f"Éxito: Clave '{clave}' eliminada del archivo."
        return False, f"Error: La clave '{clave}' no existe."

    def to_dict(self):
        return {"datos": self.datos, "max_size": self.max_size, 
                "digitos": self.digitos, "bloque_size": self.bloque_size}

    def from_dict(self, data):
        self.datos = data.get("datos", [])
        self.max_size = data.get("max_size", 0)
        self.digitos = data.get("digitos", 0)
        self.bloque_size = data.get("bloque_size", 5)