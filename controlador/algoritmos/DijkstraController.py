#Controlador.Algoritmos.DijkstraController

import heapq


class DijkstraController:
    def __init__(self, model):
        self.model = model

    def ejecutar_dijkstra(self, origen):
        """
        Ejecuta el algoritmo de Dijkstra desde un vértice origen.
        Retorna:
        - distancias: dict con distancias mínimas a cada vértice
        - predecesores: dict con el predecesor en el camino más corto
        - todos_caminos: dict con todos los caminos encontrados a cada vértice
        - proceso: lista con los pasos del algoritmo
        """
        num_vertices = self.model.obtener_num_vertices()
        aristas = self.model.obtener_aristas()

        # Validar origen
        if origen < 0 or origen >= num_vertices:
            return None, None, None, ["Error: Vértice origen inválido"]

        # Inicialización
        distancias = {i: float('inf') for i in range(num_vertices)}
        predecesores = {i: None for i in range(num_vertices)}
        todos_caminos = {i: [] for i in range(num_vertices)}
        visitados = set()
        cola_prioridad = []
        proceso = []

        distancias[origen] = 0
        todos_caminos[origen] = [[0, [origen]]]
        heapq.heappush(cola_prioridad, (0, origen, [origen]))

        proceso.append(f"Inicio desde vértice {origen + 1}")
        proceso.append(f"Distancias iniciales: {self._formatear_distancias(distancias)}")

        paso = 1

        while cola_prioridad:
            dist_actual, u, camino_actual = heapq.heappop(cola_prioridad)

            # Si ya visitamos este vértice con menor distancia, continuar
            if u in visitados:
                continue

            visitados.add(u)
            proceso.append(f"\nPaso {paso}: Visitando vértice {u + 1} (distancia: {dist_actual})")
            proceso.append(f"Camino: {' → '.join(str(v + 1) for v in camino_actual)}")

            # Explorar vecinos
            vecinos = self._obtener_vecinos(u, aristas)

            for vecino, peso in vecinos:
                nueva_distancia = dist_actual + peso
                nuevo_camino = camino_actual + [vecino]

                # Guardar TODOS los caminos encontrados (incluso si el vértice ya fue visitado)
                todos_caminos[vecino].append([nueva_distancia, nuevo_camino.copy()])

                # Solo actualizar distancia y cola si el vecino no ha sido visitado
                if vecino not in visitados:
                    if nueva_distancia < distancias[vecino]:
                        distancias[vecino] = nueva_distancia
                        predecesores[vecino] = u
                        heapq.heappush(cola_prioridad, (nueva_distancia, vecino, nuevo_camino))

                        proceso.append(
                            f"  → Actualizar vértice {vecino + 1}: distancia {nueva_distancia} (desde {u + 1}, peso {peso})")
                    else:
                        proceso.append(
                            f"  → Camino alternativo a {vecino + 1}: distancia {nueva_distancia} (no mejora)")
                else:
                    proceso.append(
                        f"  → Camino adicional a {vecino + 1} (ya visitado): distancia {nueva_distancia}")

            paso += 1

        # Resumen final
        proceso.append("\n=== RESULTADO FINAL ===")
        proceso.append(f"Distancias mínimas: {self._formatear_distancias(distancias)}")

        for i in range(num_vertices):
            if i != origen:
                camino = self._reconstruir_camino(predecesores, origen, i)
                if camino:
                    camino_str = ' → '.join(str(v + 1) for v in camino)
                    proceso.append(f"Camino más corto a {i + 1}: {camino_str} (distancia: {distancias[i]})")

        return distancias, predecesores, todos_caminos, proceso

    def _obtener_vecinos(self, vertice, aristas):
        """Obtiene los vecinos de un vértice con sus pesos"""
        vecinos = []
        ponderaciones = self.model.obtener_ponderaciones_como_lista()

        for idx, (u, v) in enumerate(aristas):
            if u == vertice:
                # Obtener peso
                peso = 1  # peso por defecto
                if idx < len(ponderaciones) and ponderaciones[idx]:
                    try:
                        peso = float(ponderaciones[idx])
                    except ValueError:
                        peso = 1

                vecinos.append((v, peso))

        return vecinos

    def _reconstruir_camino(self, predecesores, origen, destino):
        """Reconstruye el camino desde origen hasta destino"""
        if predecesores[destino] is None and destino != origen:
            return None

        camino = []
        actual = destino
        while actual is not None:
            camino.append(actual)
            actual = predecesores[actual]

        camino.reverse()
        return camino if camino[0] == origen else None

    def _formatear_distancias(self, distancias):
        """Formatea el diccionario de distancias para mostrar"""
        resultado = []
        for v, d in sorted(distancias.items()):
            if d == float('inf'):
                resultado.append(f"{v + 1}:∞")
            else:
                resultado.append(f"{v + 1}:{d}")
        return "{" + ", ".join(resultado) + "}"

    def verificar_pesos_validos(self):
        """Verifica que todos los pesos sean no negativos"""
        ponderaciones = self.model.obtener_ponderaciones_como_lista()

        for peso in ponderaciones:
            if peso:
                try:
                    valor = float(peso)
                    if valor < 0:
                        return False, "Dijkstra requiere pesos no negativos"
                except ValueError:
                    return False, "Todos los pesos deben ser números"

        return True, "Pesos válidos"