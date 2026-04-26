import json

class BellmanController:
    def __init__(self, vista):
        self.vista = vista
        self.num_vertices = 0
        self.aristas = []
        self.ponderaciones = []
        self.etiquetas_originales = {}
        self.etiquetas_enumeradas = {}
        self.mapeo_original_a_enum = {}
        self.mapeo_enum_a_original = {}

    def crear_grafo_vacio(self, num_vertices):
        self.num_vertices = num_vertices
        self.aristas = []
        self.ponderaciones = []
        # Usar etiquetas de la vista si existen, sino default
        self.etiquetas_originales = getattr(self.vista, 'etiquetas', {i: str(i+1) for i in range(num_vertices)})
        self.mapeo_original_a_enum = {}
        self.mapeo_enum_a_original = {}
        self.etiquetas_enumeradas = {}
        self.vista.grafo_original.set_grafo(num_vertices, [], self.etiquetas_originales, [])
        self.vista.grafo_enumerado.set_grafo(0, [], {}, [])

    def agregar_arista(self, origen, destino, peso):
        arista = (origen, destino)
        self.aristas.append(arista)
        self.ponderaciones.append(str(peso))
        self.cargar_grafo(self.num_vertices, self.aristas, self.etiquetas_originales, self.ponderaciones)

    def eliminar_ultima_arista(self):
        if self.aristas:
            self.aristas.pop()
            self.ponderaciones.pop()
            if len(self.aristas) > 0:
                self.cargar_grafo(self.num_vertices, self.aristas, self.etiquetas_originales, self.ponderaciones)
            else:
                self.crear_grafo_vacio(self.num_vertices)

    def actualizar_ponderacion(self, arista, nueva_ponderacion):
        try:
            indice = self.aristas.index(arista)
            self.ponderaciones[indice] = nueva_ponderacion
            self.vista.grafo_original.set_grafo(self.num_vertices, self.aristas, self.etiquetas_originales, self.ponderaciones)
            if len(self.aristas) > 0:
                self.enumerar_vertices()
                aristas_enumeradas = [(self.mapeo_original_a_enum[o], self.mapeo_original_a_enum[d]) for o, d in self.aristas]
                self.vista.grafo_enumerado.set_grafo(self.num_vertices, aristas_enumeradas, self.etiquetas_enumeradas, self.ponderaciones)
        except ValueError: pass

    def guardar_grafo(self, archivo):
        datos = {
            'num_vertices': self.num_vertices,
            'aristas': self.aristas,
            'etiquetas': self.etiquetas_originales,
            'ponderaciones': self.ponderaciones
        }
        with open(archivo, 'w') as f: json.dump(datos, f, indent=4)

    def cargar_grafo_desde_archivo(self, archivo):
        with open(archivo, 'r') as f:
            datos = json.load(f)
        num_vertices = datos['num_vertices']
        aristas = [tuple(a) for a in datos['aristas']]
        etiquetas = {int(k): v for k, v in datos['etiquetas'].items()}
        ponderaciones = datos['ponderaciones']
        self.cargar_grafo(num_vertices, aristas, etiquetas, ponderaciones)

    def cargar_grafo(self, num_vertices, aristas, etiquetas=None, ponderaciones=None):
        self.num_vertices = num_vertices
        self.aristas = aristas
        if etiquetas: self.etiquetas_originales = etiquetas.copy()
        else: self.etiquetas_originales = getattr(self.vista, 'etiquetas', {i: str(i+1) for i in range(num_vertices)})
        if ponderaciones: self.ponderaciones = ponderaciones.copy() if isinstance(ponderaciones, list) else list(ponderaciones.values())
        else: self.ponderaciones = ["1"] * len(aristas)
        self.vista.grafo_original.set_grafo(num_vertices, aristas, self.etiquetas_originales, self.ponderaciones)
        if len(aristas) > 0:
            self.enumerar_vertices()
            aristas_enumeradas = [(self.mapeo_original_a_enum[o], self.mapeo_original_a_enum[d]) for o, d in aristas]
            self.vista.grafo_enumerado.set_grafo(self.num_vertices, aristas_enumeradas, self.etiquetas_enumeradas, self.ponderaciones)
        else:
            self.vista.grafo_enumerado.set_grafo(0, [], {}, [])
        self.vista.actualizar_combos_aristas()

    def enumerar_vertices(self):
        grado_entrada = {i: 0 for i in range(self.num_vertices)}
        for origen, destino in self.aristas: grado_entrada[destino] += 1
        vertices_fuente = [v for v in range(self.num_vertices) if grado_entrada[v] == 0]
        if not vertices_fuente: vertices_fuente = list(range(self.num_vertices))
        posiciones = self.obtener_posiciones_vertices()
        vertices_fuente.sort(key=lambda v: (posiciones[v][1], posiciones[v][0]))
        enumeracion = 1
        visitados = set()
        cola = []
        self.mapeo_original_a_enum = {}
        self.mapeo_enum_a_original = {}
        self.etiquetas_enumeradas = {}
        while len(visitados) < self.num_vertices:
            if not cola:
                for v in vertices_fuente:
                    if v not in visitados:
                        cola.append(v)
                        break
                if not cola:
                    for v in range(self.num_vertices):
                        if v not in visitados:
                            cola.append(v)
                            break
            if not cola: break
            vertice = cola.pop(0)
            if vertice in visitados: continue
            enum_actual = enumeracion - 1
            self.mapeo_original_a_enum[vertice] = enum_actual
            self.mapeo_enum_a_original[enum_actual] = vertice
            self.etiquetas_enumeradas[enum_actual] = str(enumeracion)
            visitados.add(vertice)
            enumeracion += 1
            sucesores = [d for o, d in self.aristas if o == vertice and d not in visitados]
            sucesores.sort(key=lambda v: (posiciones[v][1], posiciones[v][0]))
            cola.extend(sucesores)

    def obtener_posiciones_vertices(self):
        import math
        posiciones = {}
        centro_x, centro_y = 200, 200
        radio = 150
        for i in range(self.num_vertices):
            angulo = 2 * math.pi * i / self.num_vertices - math.pi / 2
            x = centro_x + radio * math.cos(angulo)
            y = centro_y + radio * math.sin(angulo)
            posiciones[i] = (x, y)
        return posiciones

    def ejecutar_bellman(self):
        vertice_origen = 0
        distancias = {i: float('inf') for i in range(self.num_vertices)}
        distancias[vertice_origen] = 0
        predecesores = {i: None for i in range(self.num_vertices)}
        aristas_enum = []
        for i, (o, d) in enumerate(self.aristas):
            o_enum = self.mapeo_original_a_enum[o]
            d_enum = self.mapeo_original_a_enum[d]
            peso = float(self.ponderaciones[i]) if self.ponderaciones[i] else 1.0
            aristas_enum.append((o_enum, d_enum, peso))
        aristas_por_destino = {i: [] for i in range(self.num_vertices)}
        for o, d, peso in aristas_enum: aristas_por_destino[d].append((o, peso))
        iteraciones = []
        distancias_str = {self.etiquetas_enumeradas[i]: distancias[i] if distancias[i] != float('inf') else '∞' for i in range(self.num_vertices)}
        iteraciones.append({'iteracion': 0, 'distancias': distancias_str, 'cambios': []})
        for i in range(1, self.num_vertices):
            cambios = []
            aristas_entrantes = aristas_por_destino[i]
            if not aristas_entrantes:
                distancias_str = {self.etiquetas_enumeradas[j]: int(distancias[j]) if distancias[j] != float('inf') else '∞' for j in range(self.num_vertices)}
                iteraciones.append({'iteracion': i, 'distancias': distancias_str, 'cambios': []})
                continue
            opciones = []
            opciones_texto = []
            for o, peso in aristas_entrantes:
                if distancias[o] != float('inf'):
                    costo = distancias[o] + peso
                    opciones.append((costo, o))
                    etiq_o = self.etiquetas_enumeradas[o]
                    label_o = self.etiquetas_originales.get(self.mapeo_enum_a_original[o], f"V{etiq_o}")
                    opciones_texto.append(f"(λ{o + 1}({label_o}) + V{etiq_o}{self.etiquetas_enumeradas[i]}) = ({int(distancias[o])} + {int(peso)}) = {int(costo)}")
            if opciones:
                min_costo, min_origen = min(opciones)
                distancias[i] = min_costo
                predecesores[i] = min_origen
                etiq_i = self.etiquetas_enumeradas[i]
                if len(opciones_texto) == 1: cambios.append(f"V{etiq_i} = {opciones_texto[0]}")
                else: cambios.append(f"V{etiq_i} = min {{ {' ; '.join(opciones_texto)} }} = {int(min_costo)}")
            distancias_str = {self.etiquetas_enumeradas[j]: int(distancias[j]) if distancias[j] != float('inf') else '∞' for j in range(self.num_vertices)}
            iteraciones.append({'iteracion': i, 'distancias': distancias_str, 'cambios': cambios})
        ciclo_negativo = False
        for o, d, peso in aristas_enum:
            if distancias[o] != float('inf') and distancias[o] + peso < distancias[d]:
                ciclo_negativo = True
                break
        resultado_final = {}
        for i in range(self.num_vertices):
            camino = self.reconstruir_camino(predecesores, vertice_origen, i)
            etiq_i = self.etiquetas_enumeradas[i]
            resultado_final[etiq_i] = {'distancia': int(distancias[i]) if distancias[i] != float('inf') else float('inf'), 'camino': camino}
        ultimo_vertice = self.num_vertices - 1
        camino_mas_corto = int(distancias[ultimo_vertice]) if distancias[ultimo_vertice] != float('inf') else float('inf')
        return {'iteraciones': iteraciones, 'resultado_final': resultado_final, 'ciclo_negativo': ciclo_negativo, 'camino_total': camino_mas_corto}

    def reconstruir_camino(self, predecesores, origen, destino):
        if destino == origen: return f"V{self.etiquetas_enumeradas[destino]}"
        if predecesores[destino] is None: return "-"
        camino = []
        actual = destino
        while actual is not None:
            camino.append(f"V{self.etiquetas_enumeradas[actual]}")
            actual = predecesores[actual]
        return " ← ".join(camino[::-1])
