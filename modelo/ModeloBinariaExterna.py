class ModeloBinariaExterna:
    def __init__(self):
        self.datos = []
        self.max_size = 0
        self.digitos = 0
        self.bloque_size = 5  # Actualizado a 5 según tu solicitud

    def crear(self, cantidad, digitos, tam_bloque):
        self.max_size = cantidad
        self.digitos = digitos
        self.bloque_size = tam_bloque
        self.datos = []

    def insertar(self, clave):
        if len(self.datos) >= self.max_size: return False, "Error: Archivo lleno"
        if len(clave) != self.digitos: return False, f"Error: Deben ser {self.digitos} dígitos"
        if clave in self.datos: return False, "Error: Clave duplicada"
        
        self.datos.append(clave)
        self.datos.sort(key=int) # Mantiene el archivo ordenado para la binaria
        return True, f"Clave '{clave}' insertada y archivo re-ordenado."

    def eliminar(self, clave):
        if clave in self.datos:
            self.datos.remove(clave)
            return True, f"Clave '{clave}' eliminada."
        return False, "Error: Clave no encontrada."

    def buscar_binario_pasos(self, clave):
        izq = 0
        der = len(self.datos) - 1
        
        while izq <= der:
            medio = (izq + der) // 2
            # Calculamos el bloque (basado en tam_bloque de 5)
            num_bloque = (medio // self.bloque_size) + 1
            valor_medio = self.datos[medio]

            if valor_medio == clave:
                # Solo retornamos la información del bloque final
                log = f"<font color='green'><b>¡EXITO!</b> La clave {clave} se encuentra en el <b>Bloque {num_bloque}</b></font>"
                return True, medio, log
            
            if int(clave) > int(valor_medio):
                izq = medio + 1
            else:
                der = medio - 1
                
        return False, -1, f"<font color='red'>La clave {clave} no existe en el archivo.</font>"

    def to_dict(self):
        return {"datos": self.datos, "max_size": self.max_size, "digitos": self.digitos, "bloque_size": self.bloque_size}

    def from_dict(self, data):
        self.datos = data["datos"]
        self.max_size = data["max_size"]
        self.digitos = data["digitos"]
        self.bloque_size = data.get("bloque_size", 5)