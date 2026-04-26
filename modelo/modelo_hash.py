class ModeloHash:

    def __init__(self):

        self.capacidad = 0
        self.digitos = 0
        self.metodo = ""
        self.estrategia_colision = None

        self.datos = {}
        self.colisiones = {}

        self.historial = []

        self.posiciones_truncamiento = [1, 2]

    # =============================
    # CREAR ESTRUCTURA
    # =============================

    def crear(self, capacidad, digitos, metodo):

        self.capacidad = capacidad
        self.digitos = digitos
        self.metodo = metodo
        self.estrategia_colision = None

        self.datos = {i: "" for i in range(1, capacidad + 1)}
        self.colisiones = {i: [] for i in range(1, capacidad + 1)}

        self.historial = []

    # =============================
    # GUARDAR ESTADO PARA DESHACER
    # =============================

    def _guardar_estado(self):

        estado = {
            "datos": self.datos.copy(),
            "colisiones": {k: v.copy() for k, v in self.colisiones.items()}
        }

        self.historial.append(estado)

    # =============================
    # CALCULAR HASH
    # =============================

    def calcular_hash(self, clave_int):

        pasos = []
        pos = 1

        if self.metodo == "Función módulo":

            pos = (clave_int % self.capacidad) + 1

            pasos.append("Fórmula: (Clave % Capacidad) + 1")
            pasos.append(f"Cálculo: ({clave_int} % {self.capacidad}) + 1 = {pos}")

        elif self.metodo == "Función cuadrado":

            cuadrado = str(clave_int ** 2)

            pasos.append(f"1. Elevar al cuadrado: {clave_int}² = {cuadrado}")

            if len(cuadrado) < 2:
                cuadrado = cuadrado.zfill(2)

            mid = len(cuadrado) // 2

            extraidos = cuadrado[max(0, mid - 1):mid + 1]

            pasos.append(f"2. Extraer dígitos centrales: '{extraidos}'")

            pos = (int(extraidos) % self.capacidad) + 1

            pasos.append(
                f"3. Ajustar al rango: ({extraidos} % {self.capacidad}) + 1 = {pos}"
            )

        elif self.metodo == "Función plegamiento":

            s = str(clave_int)

            partes = [int(s[i:i + 2]) for i in range(0, len(s), 2)]

            pasos.append(f"1. Dividir clave en partes: {partes}")

            suma = sum(partes)

            pasos.append(
                f"2. Sumar partes: {' + '.join(map(str, partes))} = {suma}"
            )

            pos = (suma % self.capacidad) + 1

            pasos.append(
                f"3. Ajustar al rango: ({suma} % {self.capacidad}) + 1 = {pos}"
            )

        elif self.metodo == "Función truncamiento":

            s = str(clave_int).zfill(self.digitos)

            pasos.append(f"1. Clave formateada: {s}")

            seleccion = "".join(
                [s[p - 1] for p in self.posiciones_truncamiento if p <= len(s)]
            )

            pasos.append(
                f"2. Extraer posiciones {self.posiciones_truncamiento}: '{seleccion}'"
            )

            if not seleccion:
                seleccion = "0"

            pos = (int(seleccion) % self.capacidad) + 1

            pasos.append(
                f"3. Ajustar al rango: ({seleccion} % {self.capacidad}) + 1 = {pos}"
            )

        return pos, pasos

    # =============================
    # INSERTAR
    # =============================

    def insertar(self, clave, estrategia=None):

        clave_str = str(clave).zfill(self.digitos)

        clave_int = int(clave)

        pos_inicial, pasos = self.calcular_hash(clave_int)

        explicacion = [f"--- Insertando clave {clave_str} ---"] + pasos

        # evitar duplicados
        if clave_str in self.datos.values():
            return False, "Clave repetida", explicacion

        for lista in self.colisiones.values():
            if clave_str in lista:
                return False, "Clave repetida", explicacion

        # posición libre
        if self.datos[pos_inicial] == "":

            self._guardar_estado()

            self.datos[pos_inicial] = clave_str

            explicacion.append(
                f"Posición {pos_inicial} libre. Clave insertada."
            )

            return True, "Insertado", explicacion

        # colisión
        if self.estrategia_colision is None and estrategia is None:

            explicacion.append(f"Colisión en posición {pos_inicial}")

            return False, "COLISION", explicacion

        if estrategia is not None:
            self.estrategia_colision = estrategia

        estrategia = self.estrategia_colision

        self._guardar_estado()

        explicacion.append(f"Resolviendo con estrategia: {estrategia}")

        # =============================
        # SONDEO LINEAL
        # =============================

        if estrategia == "Sondeo Lineal":

            for i in range(1, self.capacidad):

                nueva_pos = ((pos_inicial - 1 + i) % self.capacidad) + 1

                explicacion.append(f"Intento {i}: probando {nueva_pos}")

                if self.datos[nueva_pos] == "":
                    self.datos[nueva_pos] = clave_str
                    explicacion.append(f"Insertado en {nueva_pos}")
                    return True, "Insertado", explicacion

        # =============================
        # SONDEO CUADRÁTICO
        # =============================

        elif estrategia == "Sondeo Cuadrático":

            for i in range(1, self.capacidad):

                nueva_pos = ((pos_inicial - 1 + i ** 2) % self.capacidad) + 1

                explicacion.append(f"Intento {i}: probando {nueva_pos}")

                if self.datos[nueva_pos] == "":
                    self.datos[nueva_pos] = clave_str
                    explicacion.append(f"Insertado en {nueva_pos}")
                    return True, "Insertado", explicacion

        # =============================
        # DOBLE HASH
        # =============================

        elif estrategia == "Doble Hash":

            pos_actual = pos_inicial

            for intento in range(1, self.capacidad):

                nueva_pos = ((pos_actual) % self.capacidad) + 1

                explicacion.append(
                    f"Rehash {intento}: ({pos_actual} % {self.capacidad}) + 1 = {nueva_pos}"
                )

                if self.datos[nueva_pos] == "":
                    self.datos[nueva_pos] = clave_str
                    explicacion.append(f"Insertado en {nueva_pos}")
                    return True, "Insertado", explicacion

                else:
                    explicacion.append(f"Colisión en {nueva_pos}")
                    pos_actual = nueva_pos

        # =============================
        # ENCADENAMIENTO
        # =============================

        elif estrategia == "Encadenamiento":

            self.colisiones[pos_inicial].append(clave_str)

            explicacion.append(f"Agregado a lista en {pos_inicial}")

            return True, "Encadenado", explicacion

        explicacion.append("Tabla llena")

        return False, "Tabla llena", explicacion

    # =============================
    # BUSCAR
    # =============================

    def buscar(self, clave):

        clave_str = str(clave).zfill(self.digitos)

        for pos, val in self.datos.items():
            if val == clave_str:
                return True, pos, "Principal"

        for pos, lista in self.colisiones.items():
            if clave_str in lista:
                return True, pos, "Encadenado"

        return False, -1, ""

    # =============================
    # ELIMINAR
    # =============================

    def eliminar(self, clave):

        clave_str = str(clave).zfill(self.digitos)

        self._guardar_estado()

        for pos, val in self.datos.items():

            if val == clave_str:

                self.datos[pos] = ""

                return True, f"Clave eliminada de {pos}"

        for pos, lista in self.colisiones.items():

            if clave_str in lista:

                lista.remove(clave_str)

                return True, f"Clave eliminada de lista {pos}"

        self.historial.pop()

        return False, "Clave no encontrada"

    # =============================
    # DESHACER
    # =============================

    def deshacer(self):

        if not self.historial:
            return False

        ultimo = self.historial.pop()

        self.datos = ultimo["datos"]

        self.colisiones = ultimo["colisiones"]

        return True

    # =============================
    # LIMPIAR
    # =============================

    def limpiar(self):

        self.datos = {i: "" for i in range(1, self.capacidad + 1)}

        self.colisiones = {i: [] for i in range(1, self.capacidad + 1)}

        self.historial = []

    # =============================
    # GUARDAR JSON
    # =============================

    def to_dict(self):

        return {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "metodo": self.metodo,
            "estrategia": self.estrategia_colision,
            "datos": self.datos,
            "colisiones": self.colisiones
        }

    # =============================
    # CARGAR JSON
    # =============================

    def from_dict(self, data):

        self.capacidad = data["capacidad"]
        self.digitos = data["digitos"]
        self.metodo = data["metodo"]
        self.estrategia_colision = data["estrategia"]

        # convertir claves a int
        self.datos = {int(k): v for k, v in data["datos"].items()}

        self.colisiones = {int(k): v for k, v in data["colisiones"].items()}

        self.historial = []