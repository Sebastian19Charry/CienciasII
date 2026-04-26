import json

class ModeloCubetasTotal:
    def __init__(self):
        # Valores por defecto iniciales
        self.reg_por_cubeta = 3
        self.num_cubetas = 2
        self.capacidad_total = 6
        self.datos = {i: [] for i in range(self.num_cubetas)}
        self.colisiones = []
        self.orden_entrada = []

    def crear(self, reg_cubeta):
        """Inicializa la estructura con K registros por cubeta y 2 cubetas iniciales"""
        self.reg_por_cubeta = reg_cubeta
        self.num_cubetas = 2
        self.capacidad_total = self.num_cubetas * self.reg_por_cubeta
        self.datos = {i: [] for i in range(self.num_cubetas)}
        self.colisiones = []
        self.orden_entrada = []

    def insertar(self, clave):
        if not clave: return False, "Clave vacía."
        if clave in self.orden_entrada: return False, "Clave duplicada."
        
        self.orden_entrada.append(clave)
        self.reorganizar_todo()
        
        log = f"🔢 Hash: {clave} mod {self.num_cubetas} = Cubeta {int(clave) % self.num_cubetas}<br>"
        
        # Factor de ocupación para Expansión (> 75%)
        # Fórmula: Ocupados / Capacidad Total
        ocupacion = (len(self.orden_entrada) / self.capacidad_total) * 100
        if ocupacion > 75:
            self.num_cubetas *= 2
            self.capacidad_total = self.num_cubetas * self.reg_por_cubeta
            self.reorganizar_todo()
            log += f"<font color='#2d6a4f'><b>¡EXPANSIÓN!</b> Estructura duplicada a {self.num_cubetas} cubetas.</font>"
        
        return True, log

    def eliminar(self, clave):
        if clave not in self.orden_entrada:
            return False, f"La clave {clave} no existe."
        
        self.orden_entrada.remove(clave)
        self.reorganizar_todo()
        
        log = f"❌ Eliminado: {clave}<br>"
        
        # Factor de reducción (< 125%)
        # Fórmula: Ocupados / Cantidad de Cubetas
        if self.num_cubetas > 2:
            indicador_red = (len(self.orden_entrada) / self.num_cubetas) * 100
            if indicador_red < 125:
                self.num_cubetas //= 2
                self.capacidad_total = self.num_cubetas * self.reg_por_cubeta
                self.reorganizar_todo()
                log += f"<font color='#bc4749'><b>¡REDUCCIÓN!</b> Estructura reducida a {self.num_cubetas} cubetas.</font>"
                
        return True, log

    def buscar(self, clave):
        """Busca en cubetas y luego en colisiones"""
        for idx, registros in self.datos.items():
            if clave in registros:
                return "principal", idx, registros.index(clave)
        if clave in self.colisiones:
            return "colision", None, self.colisiones.index(clave)
        return None, None, None

    def reorganizar_todo(self):
        """Reparte los datos en las cubetas respetando el límite K y el orden de entrada"""
        self.datos = {i: [] for i in range(self.num_cubetas)}
        self.colisiones = []
        
        for c in self.orden_entrada:
            indice = int(c) % self.num_cubetas
            if len(self.datos[indice]) < self.reg_por_cubeta:
                self.datos[indice].append(c)
            else:
                self.colisiones.append(c)

    def guardar_datos(self, ruta): # <-- Debe tener 'ruta'
        try:
            payload = {
                "reg_por_cubeta": self.reg_por_cubeta,
                "num_cubetas": self.num_cubetas,
                "orden_entrada": self.orden_entrada
            }
            with open(ruta, "w", encoding='utf-8') as f:
                json.dump(payload, f, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False

    def cargar_datos(self, ruta): # <-- Debe tener 'ruta'
        try:
            with open(ruta, "r", encoding='utf-8') as f:
                payload = json.load(f)
                self.reg_por_cubeta = payload["reg_por_cubeta"]
                self.num_cubetas = payload["num_cubetas"]
                self.orden_entrada = payload["orden_entrada"]
                self.capacidad_total = self.num_cubetas * self.reg_por_cubeta
                self.reorganizar_todo()
            return True
        except Exception as e:
            print(f"Error al cargar: {e}")
            return False