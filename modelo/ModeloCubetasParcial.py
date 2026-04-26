import json

class ModeloCubetasParcial:
    def __init__(self):
        self.reg_por_cubeta = 3
        self.num_cubetas = 2
        self.capacidad_total = 6
        self.datos = {i: [] for i in range(self.num_cubetas)}
        self.colisiones = []
        self.orden_entrada = []

    def crear(self, reg_cubeta):
        self.reg_por_cubeta = reg_cubeta
        self.num_cubetas = 2
        self.capacidad_total = self.num_cubetas * self.reg_por_cubeta
        self.datos = {i: [] for i in range(self.num_cubetas)}
        self.colisiones = []
        self.orden_entrada = []

    def calcular_siguiente_expansion(self, n):
        """
        Si n es potencia de 2 (2, 4, 8...): sumamos n/2 -> (2+1=3, 4+2=6, 8+4=12)
        Si n no es potencia de 2 (3, 6, 12...): sumamos n/3 -> (3+1=4, 6+2=8, 12+4=16)
        """
        import math
        es_potencia = (n & (n - 1) == 0) and n != 0
        if es_potencia:
            return int(n + (n / 2))
        else:
            return int(n + (n / 3))

    def calcular_siguiente_reduccion(self, n):
        """Lógica inversa: 3->2, 4->3, 6->4, 8->6, 12->8..."""
        import math
        # Verificamos si al bajar un escalón llegamos a una potencia de 2
        # Caso 3->2, 6->4, 12->8 (n / 1.5)
        paso_atras = n / 1.5
        es_potencia = (int(paso_atras) & (int(paso_atras) - 1) == 0) and paso_atras != 0
        
        if paso_atras.is_integer() and es_potencia:
            return int(paso_atras)
        else:
            # Caso 4->3, 8->6, 16->12 (n * 0.75)
            return int(n * 0.75)

    def insertar(self, clave):
        if clave in self.orden_entrada: return False, "Clave duplicada."
        
        self.orden_entrada.append(clave)
        self.reorganizar_todo()
        
        log = f"🔢 Hash Parcial: {clave} mod {self.num_cubetas} = Cubeta {int(clave) % self.num_cubetas}<br>"
        
        # Umbral de Expansión > 75%
        ocupacion = (len(self.orden_entrada) / self.capacidad_total) * 100
        if ocupacion > 75:
            self.num_cubetas = self.calcular_siguiente_expansion(self.num_cubetas)
            self.capacidad_total = self.num_cubetas * self.reg_por_cubeta
            self.reorganizar_todo()
            log += f"<font color='#2d6a4f'><b>¡EXPANSIÓN PARCIAL!</b> Ahora hay {self.num_cubetas} cubetas.</font>"
        
        return True, log

    def eliminar(self, clave):
        if clave not in self.orden_entrada: return False, "No existe."
        
        self.orden_entrada.remove(clave)
        self.reorganizar_todo()
        log = f"❌ Eliminado: {clave}<br>"
        
        # Umbral de Reducción < 125%
        if self.num_cubetas > 2:
            indicador_red = (len(self.orden_entrada) / self.num_cubetas) * 100
            if indicador_red < 125:
                self.num_cubetas = self.calcular_siguiente_reduccion(self.num_cubetas)
                self.capacidad_total = self.num_cubetas * self.reg_por_cubeta
                self.reorganizar_todo()
                log += f"<font color='#bc4749'><b>¡REDUCCIÓN PARCIAL!</b> Ahora hay {self.num_cubetas} cubetas.</font>"
        return True, log

    def reorganizar_todo(self):
        self.datos = {i: [] for i in range(self.num_cubetas)}
        self.colisiones = []
        for c in self.orden_entrada:
            indice = int(c) % self.num_cubetas
            if len(self.datos[indice]) < self.reg_por_cubeta:
                self.datos[indice].append(c)
            else:
                self.colisiones.append(c)

    def buscar(self, clave):
        for idx, regs in self.datos.items():
            if clave in regs: return "principal", idx, regs.index(clave)
        if clave in self.colisiones: return "colision", None, self.colisiones.index(clave)
        return None, None, None

    def guardar_datos(self, ruta):
        try:
            with open(ruta, "w") as f:
                json.dump({"k": self.reg_por_cubeta, "n": self.num_cubetas, "data": self.orden_entrada}, f)
            return True
        except: return False

    def cargar_datos(self, ruta):
        try:
            with open(ruta, "r") as f:
                p = json.load(f)
                self.reg_por_cubeta, self.num_cubetas, self.orden_entrada = p["k"], p["n"], p["data"]
                self.capacidad_total = self.num_cubetas * self.reg_por_cubeta
                self.reorganizar_todo()
            return True
        except: return False
