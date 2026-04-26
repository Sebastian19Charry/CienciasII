class FloydController:
    def __init__(self, num_vertices, aristas, etiquetas, ponderaciones=None):
        self.num_vertices = num_vertices
        self.aristas = aristas
        self.etiquetas = etiquetas
        self.ponderaciones = ponderaciones or {}
        self.iteraciones = []

    def sumar_ponderaciones(self, pond1, pond2):
        try:
            val1 = float(pond1) if pond1 and pond1 != '0' else 0
            val2 = float(pond2) if pond2 and pond2 != '0' else 0
            resultado = val1 + val2
            if resultado == int(resultado): return str(int(resultado))
            return str(resultado)
        except (ValueError, TypeError):
            if pond1 == '0' or not pond1: return pond2
            if pond2 == '0' or not pond2: return pond1
            return f"{pond1}+{pond2}"

    def ejecutar(self):
        n = self.num_vertices
        matriz_alcance = [[0 for _ in range(n)] for _ in range(n)]
        matriz_distancias = [[float('inf') for _ in range(n)] for _ in range(n)]
        for i in range(n):
            matriz_alcance[i][i] = 1
            matriz_distancias[i][i] = 0
        for origen, destino in self.aristas:
            if origen < n and destino < n:
                matriz_alcance[origen][destino] = 1
                ponderacion = self.ponderaciones.get((origen, destino), '')
                if ponderacion:
                    try: matriz_distancias[origen][destino] = float(ponderacion)
                    except ValueError: matriz_distancias[origen][destino] = ponderacion
                else: matriz_distancias[origen][destino] = 1
        self.iteraciones.append({
            'matriz_distancias': [fila[:] for fila in matriz_distancias],
            'etiquetas': self.etiquetas.copy(),
            'info': 'Matriz Inicial'
        })
        for k in range(n):
            cambios_distancias = []
            for i in range(n):
                for j in range(n):
                    if matriz_alcance[i][k] == 1 and matriz_alcance[k][j] == 1:
                        pond_ik = matriz_distancias[i][k]
                        pond_kj = matriz_distancias[k][j]
                        if isinstance(pond_ik, (int, float)) and isinstance(pond_kj, (int, float)):
                            if pond_ik != float('inf') and pond_kj != float('inf'):
                                nueva_pond = pond_ik + pond_kj
                            else: nueva_pond = float('inf')
                        else: nueva_pond = self.sumar_ponderaciones(str(pond_ik), str(pond_kj))
                        if matriz_alcance[i][j] == 0:
                            cambios_distancias.append((i, j))
                            matriz_alcance[i][j] = 1
                            matriz_distancias[i][j] = nueva_pond
                        else:
                            actual = matriz_distancias[i][j]
                            if isinstance(actual, (int, float)) and isinstance(nueva_pond, (int, float)):
                                if nueva_pond < actual:
                                    cambios_distancias.append((i, j))
                                    matriz_distancias[i][j] = nueva_pond
            etiq_k = self.etiquetas.get(k, str(k + 1))
            self.iteraciones.append({
                'matriz_distancias': [fila[:] for fila in matriz_distancias],
                'etiquetas': self.etiquetas.copy(),
                'cambios_distancias': cambios_distancias,
                'info': f"Usando {etiq_k} como intermediario"
            })
        return self.iteraciones

    def grafo_es_fuertemente_conexo(self):
        if not self.iteraciones: self.ejecutar()
        matriz_final = self.iteraciones[-1]['matriz_distancias']
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if i != j and matriz_final[i][j] == float('inf'): return False
        return True
