import math
import json

class ModeloHashExterno:
    def __init__(self):
        self.capacidad_registros = 0 
        self.registros_por_bloque = 5  # Tamaño fijo de la "cubeta"
        self.num_bloques = 0
        self.digitos = 0
        self.metodo = ""
        self.estrategia_fija = None # Una vez elegida una estrategia, se mantiene
        
        self.bloques = {}  # {indice_bloque: [lista_de_claves]}
        self.historial = []

    def crear(self, capacidad, digitos, metodo):
        self.capacidad_registros = capacidad
        self.digitos = digitos
        self.metodo = metodo
        self.estrategia_fija = None
        
        # En externa, calculamos cuántas cubetas (bloques) existen
        self.num_bloques = math.ceil(capacidad / self.registros_por_bloque)
        self.bloques = {i: [] for i in range(1, self.num_bloques + 1)}
        self.historial = []

    def _guardar_estado(self):
        estado = {k: v.copy() for k, v in self.bloques.items()}
        self.historial.append(estado)

    def calcular_hash(self, clave_int):
        pasos = []
        # El hash se calcula sobre el número de bloques disponibles
        if "módulo" in self.metodo.lower():
            pos = (clave_int % self.num_bloques) + 1
            pasos.append(f"Cálculo: ({clave_int} % {self.num_bloques} bloques) + 1 = {pos}")
        elif "cuadrado" in self.metodo.lower():
            cuadrado = str(clave_int ** 2).zfill(2)
            mid = len(cuadrado) // 2
            ext = cuadrado[max(0, mid-1):mid+1]
            pos = (int(ext) % self.num_bloques) + 1
            pasos.append(f"Cuadrado: {clave_int}²={cuadrado}. Centro: {ext}. Bloque: {pos}")
        else:
            pos = (clave_int % self.num_bloques) + 1 # Default
            
        return pos, pasos

    def insertar(self, clave, estrategia=None):
        clave_str = str(clave).zfill(self.digitos)
        pos_ideal, pasos = self.calcular_hash(int(clave))
        explicacion = [f"--- Buscando Bloque para {clave_str} ---"] + pasos

        # 1. Verificar si ya existe
        for b in self.bloques.values():
            if clave_str in b: return False, "Clave duplicada", explicacion

        # 2. Si hay espacio en el bloque ideal (Sin colisión de bloque)
        if len(self.bloques[pos_ideal]) < self.registros_por_bloque:
            self._guardar_estado()
            self.bloques[pos_ideal].append(clave_str)
            explicacion.append(f"Bloque {pos_ideal} con espacio. Insertado.")
            return True, "EXITO", explicacion

        # 3. COLISIÓN DE BLOQUE (Bloque lleno)
        if self.estrategia_fija is None and estrategia is None:
            explicacion.append(f"¡COLISIÓN! El bloque {pos_ideal} está lleno.")
            return False, "COLISION", explicacion

        if estrategia: self.estrategia_fija = estrategia
        
        self._guardar_estado()
        return self.resolver_colision(pos_ideal, clave_str, explicacion)

    def resolver_colision(self, pos_inicial, clave, explicacion):
        est = self.estrategia_fija
        explicacion.append(f"Resolviendo en archivo con: {est}")

        if est == "Encadenamiento":
            # Se añade al bloque aunque exceda el tamaño (simula overflow area)
            self.bloques[pos_inicial].append(clave)
            explicacion.append(f"Clave añadida al área de desborde del bloque {pos_inicial}")
            return True, "EXITO", explicacion

        # Sondeos (buscan otros bloques con espacio)
        for i in range(1, self.num_bloques):
            if est == "Sondeo Lineal":
                nueva_pos = ((pos_inicial - 1 + i) % self.num_bloques) + 1
            elif est == "Sondeo Cuadrático":
                nueva_pos = ((pos_inicial - 1 + i**2) % self.num_bloques) + 1
            
            explicacion.append(f"Probando Bloque {nueva_pos}...")
            if len(self.bloques[nueva_pos]) < self.registros_por_bloque:
                self.bloques[nueva_pos].append(clave)
                explicacion.append(f"Espacio encontrado en Bloque {nueva_pos}. Insertado.")
                return True, "EXITO", explicacion

        return False, "Archivo lleno", explicacion

    def eliminar(self, clave):
        clave_str = str(clave).zfill(self.digitos)
        for i in self.bloques:
            if clave_str in self.bloques[i]:
                self._guardar_estado()
                self.bloques[i].remove(clave_str)
                return True, f"Clave {clave_str} eliminada del bloque {i}"
        return False, "No encontrada"

    def deshacer(self):
        if self.historial:
            self.bloques = self.historial.pop()
            return True
        return False
    
    def exportar_datos(self):
        """Prepara los datos para ser guardados en JSON"""
        return {
            "configuracion": {
                "capacidad_registros": self.capacidad_registros,
                "registros_por_bloque": self.registros_por_bloque,
                "num_bloques": self.num_bloques,
                "digitos": self.digitos,
                "metodo": self.metodo,
                "estrategia_fija": self.estrategia_fija
            },
            "bloques": self.bloques
        }

    def importar_datos(self, data):
        """Carga los datos desde un diccionario (usado para Recuperar)"""
        config = data["configuracion"]
        self.capacidad_registros = config["capacidad_registros"]
        self.registros_por_bloque = config["registros_por_bloque"]
        self.num_bloques = config["num_bloques"]
        self.digitos = config["digitos"]
        self.metodo = config["metodo"]
        self.estrategia_fija = config["estrategia_fija"]
        # Convertir llaves a int porque JSON las guarda como string
        self.bloques = {int(k): v for k, v in data["bloques"].items()}
        self.historial = []