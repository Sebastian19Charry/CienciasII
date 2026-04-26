import heapq
from collections import Counter

# =========================================================
# 1. ÁRBOLES DIGITALES (Digital Trees)
# =========================================================
class NodoDigital:
    def __init__(self):
        self.hijos = {'0': None, '1': None} # Bifurcación binaria
        self.letras = [] # Caracteres guardados en este nodo
        self.es_fin = False # Marca si una palabra termina aquí

class ArbolDigital:
    def __init__(self):
        self.raiz = NodoDigital()
        # Mapeo a-z -> 5 bits
        self.codigos = {chr(97 + i): format(i + 1, "05b") for i in range(26)}
        self.palabras = []

    def insertar(self, palabra):
        palabra = palabra.lower().strip()

        if not palabra:
            return False, "Palabra vacía"

        letras = [c for c in palabra if c.isalpha()]
        if not letras:
            return False, "Sin letras válidas"

        palabra_limpia = "".join(letras)

        for letra in letras:

            codigo = self.codigos[letra]
            nodo = self.raiz

            # recorrer el camino binario
            for bit in codigo:

                if nodo.hijos[bit] is None:
                    nodo.hijos[bit] = NodoDigital()

                nodo = nodo.hijos[bit]

            # guardar letra en el nodo final
            if letra not in nodo.letras:
                nodo.letras.append(letra)

        if palabra_limpia not in self.palabras:
            self.palabras.append(palabra_limpia)

        return True, "OK"

    def buscar(self, letra):
        """Busca una letra y retorna su ruta binaria."""
        letra = letra.lower().strip()
        def _recorrer(nodo, ruta):
            if not nodo: return None
            if letra in nodo.letras: return ruta
            for bit in ['0', '1']:
                res = _recorrer(nodo.hijos[bit], ruta + bit)
                if res is not None: return res
            return None
        return _recorrer(self.raiz, "")

    def eliminar(self, letra):
        """Elimina una letra y reconstruye."""
        letra = letra.lower().strip()
        nuevas = []
        encontrada = False
        for p in self.palabras:
            n = p.replace(letra, "")
            if n: nuevas.append(n)
            if p != n: encontrada = True
            
        if not encontrada: return False, f"Letra '{letra}' no encontrada"
        
        self.raiz = NodoDigital()
        self.palabras = []
        for n in nuevas:
            self.insertar(n)
        return True, "OK"

    def to_dict(self):
        return {"palabras": self.palabras}

# =========================================================
# 2. ÁRBOLES DE HUFFMAN
# =========================================================
class NodoHuffman:
    def __init__(self, char=None, freq=0, izq=None, der=None):
        self.char = char
        self.freq = freq
        self.izq = izq
        self.der = der

    def __lt__(self, otro):
        return self.freq < otro.freq

class ArbolHuffman:
    def __init__(self):
        self.raiz = None
        self.codigos = {}
        self.frecuencias = {}

    def construir(self, texto):
        if not texto: return False
        self.frecuencias = Counter(texto)
        heap = [NodoHuffman(c, f) for c, f in self.frecuencias.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            n1 = heapq.heappop(heap)
            n2 = heapq.heappop(heap)
            padre = NodoHuffman(None, n1.freq + n2.freq, n1, n2)
            heapq.heappush(heap, padre)

        self.raiz = heap[0] if heap else None
        self.codigos = {}
        self._generar_codigos(self.raiz, "")
        return True

    def _generar_codigos(self, nodo, ruta):
        if not nodo: return
        if nodo.char:
            self.codigos[nodo.char] = ruta or "0"
            return
        self._generar_codigos(nodo.izq, ruta + "0")
        self._generar_codigos(nodo.der, ruta + "1")

    # --- MÉTODO AÑADIDO PARA EL RESALTADO ---
    def buscar(self, letra):
        """Retorna la ruta binaria (ej: '101') de una letra."""
        return self.codigos.get(letra, None)

    def codificar(self, texto):
        if not self.codigos: return ""
        return "".join(self.codigos.get(c, "") for c in texto)

    def decodificar(self, binario):
        if not self.raiz: return ""
        res = []
        curr = self.raiz
        for bit in binario:
            if bit == '0': curr = curr.izq
            else: curr = curr.der
            if curr and curr.char:
                res.append(curr.char)
                curr = self.raiz
        return "".join(res)

    def to_dict(self):
        return {"frecuencias": self.frecuencias}
    
    def from_dict(self, data):
        freq = data.get("frecuencias", {})
        if freq:
            texto_dummy = "".join(c * f for c, f in freq.items())
            self.construir(texto_dummy)

# =========================================================
# 3. TRIES DE RESIDUOS (Standard Radix Trie)
# =========================================================
class NodoTrie:
    def __init__(self, letra=None, es_enlace=False):
        self.letra = letra
        self.es_enlace = es_enlace # '*' en el proyecto original
        self.hijos = {} # '0' y '1'

class TrieResiduos:
    def __init__(self):
        self.raiz = NodoTrie(es_enlace=True)
        self.codigos = {chr(65 + i): format(i + 1, "05b") for i in range(26)}
        self.letras = set()

    def insertar(self, letra):
        letra = letra.upper()
        if letra not in self.codigos or letra in self.letras: return
        
        codigo = self.codigos[letra]
        nodo = self.raiz
        self.letras.add(letra)

        for i, bit in enumerate(codigo):
            if bit not in nodo.hijos:
                nodo.hijos[bit] = NodoTrie(letra=letra)
                return
            
            hijo = nodo.hijos[bit]
            if hijo.es_enlace:
                nodo = hijo
                continue
            
            # Colisión: transformar hoja en enlace
            letra_vieja = hijo.letra
            if letra_vieja == letra: return
            
            hijo.es_enlace = True
            hijo.letra = None
            
            # Re-insertar ambas desde el siguiente bit
            self._insertar_desde(hijo, letra_vieja, i + 1)
            self._insertar_desde(hijo, letra, i + 1)
            return

    def _insertar_desde(self, nodo, letra, n_bit):
        cod = self.codigos[letra]
        curr = nodo
        for i in range(n_bit, len(cod)):
            bit = cod[i]
            if bit not in curr.hijos:
                curr.hijos[bit] = NodoTrie(letra=letra)
                return
            hijo = curr.hijos[bit]
            if hijo.es_enlace:
                curr = hijo
                continue
            
            # Nueva colisión en nivel inferior
            v_l = hijo.letra
            hijo.es_enlace = True
            hijo.letra = None
            self._insertar_desde(hijo, v_l, i + 1)
            curr = hijo

    def buscar(self, letra):
        letra = letra.upper()
        if letra not in self.codigos: return None
        cod = self.codigos[letra]
        nodo = self.raiz
        ruta = ""
        for bit in cod:
            if bit not in nodo.hijos: return None
            ruta += bit
            hijo = nodo.hijos[bit]
            if not hijo.es_enlace and hijo.letra == letra:
                return ruta
            if hijo.es_enlace:
                nodo = hijo
            else:
                return None
        return None

    def eliminar(self, letra):
        letra = letra.upper()
        if letra not in self.letras: return False
        self.letras.remove(letra)
        temp = list(self.letras)
        self.raiz = NodoTrie(es_enlace=True)
        self.letras = set()
        for l in temp: self.insertar(l)
        return True

    def to_dict(self):
        return {"letras": list(self.letras)}

# =========================================================
# 4. MÚLTIPLES RESIDUOS (Radix-4 Trie)
# =========================================================
class NodoMulti:
    def __init__(self, letra=None):
        self.letra = letra
        self.hijos = {} # '00', '01', '10', '11'

class MultiplesResiduos:
    def __init__(self):
        self.raiz = NodoMulti()
        self.codigos = {chr(65 + i): format(i + 1, "05b") for i in range(26)}
        self.letras = set()

    def insertar(self, letra):
        letra = letra.upper()
        if letra not in self.codigos or letra in self.letras: return
        self.letras.add(letra)
        
        cod = self.codigos[letra]
        # Dividir 5 bits en: [2, 2, 1]
        pasos = [cod[0:2], cod[2:4], cod[4:5]]
        
        nodo = self.raiz
        for i, par in enumerate(pasos):
            if par not in nodo.hijos:
                if i == len(pasos) - 1:
                    nodo.hijos[par] = NodoMulti(letra)
                else:
                    nodo.hijos[par] = NodoMulti()
                    nodo = nodo.hijos[par]
            else:
                if i == len(pasos) - 1:
                    # En este modelo se asume que si hay colisión se sobreescribe o ignora 
                    # según el diseño simple del controlador original
                    pass
                else:
                    nodo = nodo.hijos[par]

    def buscar(self, letra):
        letra = letra.upper()
        if letra not in self.codigos: return None
        cod = self.codigos[letra]
        pasos = [cod[0:2], cod[2:4], cod[4:5]]
        nodo = self.raiz
        ruta = []
        for par in pasos:
            if par not in nodo.hijos: return None
            ruta.append(par)
            hijo = nodo.hijos[par]
            if hijo.letra == letra: return "-".join(ruta)
            nodo = hijo
        return None

    def eliminar(self, letra):
        letra = letra.upper()
        if letra not in self.letras: return False
        self.letras.remove(letra)
        temp = list(self.letras)
        self.raiz = NodoMulti()
        self.letras = set()
        for l in temp: self.insertar(l)
        return True

    def to_dict(self):
        return {"letras": list(self.letras)}
