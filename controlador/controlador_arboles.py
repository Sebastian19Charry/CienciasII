from modelo.modelo_arboles import ArbolDigital, ArbolHuffman, TrieResiduos, MultiplesResiduos
from modelo.manejador_archivos import ManejadorArchivos

class ControladorArboles:
    def __init__(self, vista, metodo):
        self.vista = vista
        self.metodo = metodo
        self.ruta_archivo = f"data/tree_{metodo.replace(' ', '_').lower()}.json"
        self.modelo = self._inicializar_modelo()
        # No cargar aquí para evitar error de inicialización en la vista

    def _inicializar_modelo(self):
        if self.metodo == "Árboles Digitales":
            return ArbolDigital()
        elif self.metodo == "Árboles de Huffman":
            return ArbolHuffman()
        elif self.metodo == "Tries de Residuos":
            return TrieResiduos()
        elif self.metodo == "Múltiples Residuos":
            return MultiplesResiduos()
        return None

    def insertar(self, clave):
        if not clave: return
        
        if self.metodo == "Árboles Digitales":
            res, msg = self.modelo.insertar(clave)
            if res:
                self.vista.mensaje(f"Palabra '{clave}' insertada.")
                self.vista.actualizar_dibujo()
                self.guardar()
            else:
                self.vista.mensaje(f"Error: {msg}")

        elif self.metodo == "Árboles de Huffman":
            self.modelo.construir(clave)
            self.vista.mensaje("Árbol de Huffman construido.")
            self.vista.actualizar_dibujo()
            self.guardar()
            
            stats = self._obtener_stats_huffman()
            self.vista.mensaje(f"Compresión: {stats['porcentaje']}%")

        elif self.metodo in ["Tries de Residuos", "Múltiples Residuos"]:
            for char in clave.upper():
                if char.isalpha():
                    self.modelo.insertar(char)
            self.vista.mensaje(f"Clave '{clave}' procesada en el Trie.")
            self.vista.actualizar_dibujo()
            self.guardar()

    def buscar(self, clave):
        if not clave:
            return

        # Si es Huffman, necesitamos obtener el código (la ruta de bits)
        if self.metodo == "Árboles de Huffman":
            # Asumiendo que tu modelo Huffman tiene el diccionario 'codigos'
            res = self.modelo.codigos.get(clave) 
        else:
            res = self.modelo.buscar(clave)

        if res:
            self.vista.mensaje(f"Encontrado: {clave} → ruta {res}")
            self.vista.resaltar_camino(res)
        else:
            self.vista.mensaje(f"No se encontró: {clave}")
            self.vista.resaltar_camino(None)

    def eliminar(self, clave):
        if not clave: return
        if self.metodo == "Árboles de Huffman":
            self.vista.mensaje("No se puede eliminar de un árbol de Huffman individualmente. Limpie el árbol.")
            return

        res = self.modelo.eliminar(clave)
        if res:
            self.vista.mensaje(f"Eliminado: {clave}")
            self.vista.actualizar_dibujo()
            self.guardar()
        else:
            self.vista.mensaje(f"Error al eliminar: {clave}")

    def codificar(self, texto):
        if self.metodo != "Árboles de Huffman": return
        binario = self.modelo.codificar(texto)
        self.vista.mensaje(f"Codificación: {binario}")
        return binario

    def decodificar(self, binario):
        if self.metodo != "Árboles de Huffman": return
        texto = self.modelo.decodificar(binario)
        self.vista.mensaje(f"Decodificación: {texto}")
        return texto

    def _obtener_stats_huffman(self):
        m = self.modelo
        bits_originales = len(m.frecuencias) * 8 # Aproximación simple
        bits_comprimidos = sum(len(m.codigos[c]) * f for c, f in m.frecuencias.items())
        ahorro = bits_originales - bits_comprimidos
        porc = round((ahorro / bits_originales) * 100, 2) if bits_originales > 0 else 0
        return {"porcentaje": porc}

    def eliminar_todo(self):
        self.modelo = self._inicializar_modelo()
        self.vista.mensaje("Estructura reiniciada.")
        self.vista.actualizar_dibujo()
        self.guardar()

    def guardar(self):
        ManejadorArchivos.guardar_json(self.ruta_archivo, self.modelo.to_dict())

    def cargar(self):
        datos = ManejadorArchivos.leer_json(self.ruta_archivo)
        if not datos: return

        if self.metodo == "Árboles Digitales":
            for p in datos.get("palabras", []):
                self.modelo.insertar(p)
        elif self.metodo == "Árboles de Huffman":
            self.modelo.from_dict(datos)
        elif self.metodo in ["Tries de Residuos", "Múltiples Residuos"]:
            for l in datos.get("letras", []):
                self.modelo.insertar(l)
        
        self.vista.actualizar_dibujo()
