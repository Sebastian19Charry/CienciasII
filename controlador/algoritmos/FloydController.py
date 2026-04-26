#Controlador.Algoritmos.FloydController

class FloydController:
    """Controlador para el algoritmo de Floyd (Alcance con ponderaciones)"""

    def __init__(self, num_vertices, aristas, etiquetas, ponderaciones=None):
        self.num_vertices = num_vertices
        self.aristas = aristas
        self.etiquetas = etiquetas
        self.ponderaciones = ponderaciones or {}
        self.iteraciones = []

    def sumar_ponderaciones(self, pond1, pond2):
        """Suma dos ponderaciones, pueden ser números o expresiones"""
        try:
            # Intentar convertir a números y sumar
            val1 = float(pond1) if pond1 and pond1 != '0' else 0
            val2 = float(pond2) if pond2 and pond2 != '0' else 0
            resultado = val1 + val2

            # Si el resultado es entero, devolverlo sin decimales
            if resultado == int(resultado):
                return str(int(resultado))
            return str(resultado)
        except (ValueError, TypeError):
            # Si no son números simples, concatenar
            if pond1 == '0' or not pond1:
                return pond2
            if pond2 == '0' or not pond2:
                return pond1
            return f"{pond1}+{pond2}"

    def ejecutar(self):
        """Ejecuta el algoritmo de Floyd y retorna todas las iteraciones"""
        n = self.num_vertices

        # Inicializar matriz de alcance (1 o 0)
        matriz_alcance = [[0 for _ in range(n)] for _ in range(n)]

        # Inicializar matriz de distancias/ponderaciones
        matriz_distancias = [[float('inf') for _ in range(n)] for _ in range(n)]

        # Llenar matrices iniciales
        for i in range(n):
            matriz_alcance[i][i] = 1
            matriz_distancias[i][i] = 0

        for origen, destino in self.aristas:
            if origen < n and destino < n:
                matriz_alcance[origen][destino] = 1

                # Obtener ponderación de la arista
                ponderacion = self.ponderaciones.get((origen, destino), '')
                if ponderacion:
                    try:
                        matriz_distancias[origen][destino] = float(ponderacion)
                    except ValueError:
                        matriz_distancias[origen][destino] = ponderacion
                else:
                    matriz_distancias[origen][destino] = 1

        # Guardar estado inicial
        self.iteraciones.append({
            'matriz_distancias': [fila[:] for fila in matriz_distancias],
            'etiquetas': self.etiquetas.copy(),
            'info': 'Matriz Inicial con ponderaciones directas'
        })

        # Algoritmo de Floyd
        for k in range(n):
            cambios_distancias = []
            matriz_anterior = [fila[:] for fila in matriz_distancias]

            for i in range(n):
                for j in range(n):
                    # Si hay camino de i a k y de k a j
                    if matriz_alcance[i][k] == 1 and matriz_alcance[k][j] == 1:
                        # Calcular nueva ponderación
                        pond_ik = matriz_distancias[i][k]
                        pond_kj = matriz_distancias[k][j]

                        # Si ambas son números, sumarlas
                        if isinstance(pond_ik, (int, float)) and isinstance(pond_kj, (int, float)):
                            if pond_ik != float('inf') and pond_kj != float('inf'):
                                nueva_pond = pond_ik + pond_kj
                            else:
                                nueva_pond = float('inf')
                        else:
                            # Si no son números, usar la función de suma
                            nueva_pond = self.sumar_ponderaciones(str(pond_ik), str(pond_kj))

                        # Si no había alcance antes, es un nuevo camino
                        if matriz_alcance[i][j] == 0:
                            cambios_distancias.append((i, j))
                            matriz_alcance[i][j] = 1
                            matriz_distancias[i][j] = nueva_pond
                        else:
                            # Ya había alcance, comparar si el nuevo camino es mejor
                            actual = matriz_distancias[i][j]

                            # Comparar valores numéricos
                            if isinstance(actual, (int, float)) and isinstance(nueva_pond, (int, float)):
                                if nueva_pond < actual:
                                    cambios_distancias.append((i, j))
                                    matriz_distancias[i][j] = nueva_pond

            # Construir información de la iteración
            etiq_k = self.etiquetas.get(k, str(k + 1))

            if cambios_distancias:
                caminos_encontrados = []
                for i, j in cambios_distancias:
                    etiq_i = self.etiquetas.get(i, str(i + 1))
                    etiq_j = self.etiquetas.get(j, str(j + 1))
                    pond = matriz_distancias[i][j]

                    if isinstance(pond, float):
                        if pond == int(pond):
                            pond_str = str(int(pond))
                        else:
                            pond_str = str(pond)
                    else:
                        pond_str = str(pond)

                    caminos_encontrados.append(f"({etiq_i}→{etiq_j}: {pond_str})")

                info = f"Usando {etiq_k} como intermediario. Nuevos caminos: {', '.join(caminos_encontrados)}"
            else:
                info = f"Usando {etiq_k} como intermediario. No hay nuevos caminos"

            self.iteraciones.append({
                'matriz_distancias': [fila[:] for fila in matriz_distancias],
                'etiquetas': self.etiquetas.copy(),
                'cambios_distancias': cambios_distancias,
                'info': info
            })

        return self.iteraciones

    def obtener_caminos_alcanzables(self, desde):
        """Retorna los nodos alcanzables desde un nodo dado con sus ponderaciones"""
        if not self.iteraciones:
            self.ejecutar()

        matriz_distancias = self.iteraciones[-1]['matriz_distancias']
        alcanzables = []

        for j in range(self.num_vertices):
            dist = matriz_distancias[desde][j]
            if dist != float('inf') and desde != j:
                alcanzables.append({
                    'destino': j,
                    'etiqueta': self.etiquetas.get(j, str(j + 1)),
                    'ponderacion': dist
                })

        return alcanzables

    def grafo_es_fuertemente_conexo(self):
        """Verifica si el grafo es fuertemente conexo"""
        if not self.iteraciones:
            self.ejecutar()

        matriz_final = self.iteraciones[-1]['matriz_distancias']

        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if i != j and matriz_final[i][j] == float('inf'):
                    return False

        return True

    def obtener_matriz_final_distancias(self):
        """Retorna la matriz final con todas las ponderaciones"""
        if not self.iteraciones:
            self.ejecutar()

        return self.iteraciones[-1]['matriz_distancias']
