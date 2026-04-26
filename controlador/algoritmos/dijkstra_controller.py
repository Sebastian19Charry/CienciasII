import heapq

class DijkstraController:
    def __init__(self, model):
        self.model = model

    def ejecutar_dijkstra(self, origen):
        num_vertices = self.model.obtener_num_vertices()
        aristas = self.model.obtener_aristas()

        if origen < 0 or origen >= num_vertices:
            return None, None, None, ["Error: Vértice origen inválido"]

        distancias = {i: float('inf') for i in range(num_vertices)}
        predecesores = {i: None for i in range(num_vertices)}
        todos_caminos = {i: [] for i in range(num_vertices)}
        visitados = set()
        cola_prioridad = []
        proceso = []

        distancias[origen] = 0
        todos_caminos[origen] = [[0, [origen]]]
        heapq.heappush(cola_prioridad, (0, origen, [origen]))

        proceso.append(f"Inicio desde vértice {self.model.etiquetas.get(origen, str(origen + 1))}")
        proceso.append(f"Distancias iniciales: {self._formatear_distancias(distancias)}")

        paso = 1
        while cola_prioridad:
            dist_actual, u, camino_actual = heapq.heappop(cola_prioridad)
            if u in visitados: continue
            visitados.add(u)
            proceso.append(f"\nPaso {paso}: Visitando vértice {self.model.etiquetas.get(u, str(u + 1))} (distancia: {dist_actual})")
            proceso.append(f"Camino: {' → '.join(self.model.etiquetas.get(v, str(v + 1)) for v in camino_actual)}")

            vecinos = self._obtener_vecinos(u, aristas)
            for vecino, peso in vecinos:
                nueva_distancia = dist_actual + peso
                nuevo_camino = camino_actual + [vecino]
                todos_caminos[vecino].append([nueva_distancia, nuevo_camino.copy()])

                if vecino not in visitados:
                    if nueva_distancia < distancias[vecino]:
                        distancias[vecino] = nueva_distancia
                        predecesores[vecino] = u
                        heapq.heappush(cola_prioridad, (nueva_distancia, vecino, nuevo_camino))
                        proceso.append(f"  → Actualizar vértice {self.model.etiquetas.get(vecino, str(vecino + 1))}: distancia {nueva_distancia} (desde {self.model.etiquetas.get(u, str(u + 1))}, peso {peso})")
                    else:
                        proceso.append(f"  → Camino alternativo a {self.model.etiquetas.get(vecino, str(vecino + 1))}: distancia {nueva_distancia} (no mejora)")
                else:
                    proceso.append(f"  → Camino adicional a {self.model.etiquetas.get(vecino, str(vecino + 1))} (ya visitado): distancia {nueva_distancia}")
            paso += 1

        proceso.append("\n=== RESULTADO FINAL ===")
        proceso.append(f"Distancias mínimas: {self._formatear_distancias(distancias)}")
        for i in range(num_vertices):
            if i != origen:
                camino = self._reconstruir_camino(predecesores, origen, i)
                if camino:
                    camino_str = ' → '.join(self.model.etiquetas.get(v, str(v + 1)) for v in camino)
                    proceso.append(f"Camino más corto a {self.model.etiquetas.get(i, str(i + 1))}: {camino_str} (distancia: {distancias[i]})")
        return distancias, predecesores, todos_caminos, proceso

    def _obtener_vecinos(self, vertice, aristas):
        vecinos = []
        ponderaciones = self.model.obtener_ponderaciones_como_lista()
        for idx, (u, v) in enumerate(aristas):
            if u == vertice:
                peso = 1
                if idx < len(ponderaciones) and ponderaciones[idx]:
                    try: peso = float(ponderaciones[idx])
                    except ValueError: peso = 1
                vecinos.append((v, peso))
        return vecinos

    def _reconstruir_camino(self, predecesores, origen, destino):
        if predecesores[destino] is None and destino != origen: return None
        camino = []; actual = destino
        while actual is not None:
            camino.append(actual)
            actual = predecesores[actual]
        camino.reverse()
        return camino if camino[0] == origen else None

    def _formatear_distancias(self, distancias):
        resultado = []
        for v, d in sorted(distancias.items()):
            label = self.model.etiquetas.get(v, str(v + 1))
            if d == float('inf'): resultado.append(f"{label}:∞")
            else: resultado.append(f"{label}:{d}")
        return "{" + ", ".join(resultado) + "}"

    def verificar_pesos_validos(self):
        ponderaciones = self.model.obtener_ponderaciones_como_lista()
        for peso in ponderaciones:
            if peso:
                try:
                    valor = float(peso)
                    if valor < 0: return False, "Dijkstra requiere pesos no negativos"
                except ValueError: return False, "Todos los pesos deben ser números"
        return True, "Pesos válidos"
