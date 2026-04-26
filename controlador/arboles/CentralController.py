# controlador/arboles/centralController.py
# Lógica idéntica al proyecto de referencia CienciasII-main
from collections import deque


class CentralController:
    """
    Controlador para el algoritmo de Centro de Árbol.
    
    Algoritmo:
    1. Calcula excentricidades: e(v) = max distancia desde v a cualquier otro vértice (BFS).
    2. Radio   = min(excentricidades)
    3. Diámetro = max(excentricidades)
    4. Centro  = {v : e(v) == radio}
    5. Genera pasos visuales eliminando hojas iterativamente.
    6. Genera tabla HTML de distancias con columna de excentricidades.
    """

    def __init__(self):
        self.num_vertices = 0
        self.aristas = []
        self.etiquetas = {}

    # ── Configuración ────────────────────────────────────────────────────────
    def set_grafo(self, num_vertices, aristas, etiquetas=None):
        """Configura el grafo/árbol."""
        self.num_vertices = num_vertices
        self.aristas = aristas.copy()
        if etiquetas:
            self.etiquetas = etiquetas.copy()
        else:
            self.etiquetas = {i: chr(97 + i) for i in range(num_vertices)}

    # ── Validaciones ─────────────────────────────────────────────────────────
    def es_arbol(self):
        """Verifica si el grafo es un árbol (n-1 aristas y conexo)."""
        if not self.aristas:
            return self.num_vertices == 1
        if len(self.aristas) != self.num_vertices - 1:
            return False
        return self.es_conexo()

    def es_conexo(self):
        """Verifica si el grafo es conexo usando BFS."""
        if self.num_vertices == 0:
            return True
        ady = [[] for _ in range(self.num_vertices)]
        for o, d in self.aristas:
            ady[o].append(d)
            ady[d].append(o)
        visitados = [False] * self.num_vertices
        cola = deque([0])
        visitados[0] = True
        count = 1
        while cola:
            actual = cola.popleft()
            for v in ady[actual]:
                if not visitados[v]:
                    visitados[v] = True
                    cola.append(v)
                    count += 1
        return count == self.num_vertices

    # ── Cálculo de distancias ─────────────────────────────────────────────────
    def calcular_distancias_desde(self, inicio):
        """Distancias desde un vértice a todos los demás (BFS)."""
        ady = [[] for _ in range(self.num_vertices)]
        for o, d in self.aristas:
            ady[o].append(d)
            ady[d].append(o)
        distancias = [-1] * self.num_vertices
        distancias[inicio] = 0
        cola = deque([inicio])
        while cola:
            actual = cola.popleft()
            for v in ady[actual]:
                if distancias[v] == -1:
                    distancias[v] = distancias[actual] + 1
                    cola.append(v)
        return distancias

    def calcular_excentricidades(self):
        """Excentricidad de cada vértice = max distancia desde ese vértice."""
        exc = {}
        for v in range(self.num_vertices):
            dist = self.calcular_distancias_desde(v)
            exc[v] = max(dist)
        return exc

    # ── Algoritmo principal ───────────────────────────────────────────────────
    def calcular_centro(self):
        """
        Calcula el centro del árbol.
        Retorna: (centro, excentricidades, radio, diametro, detalles_texto)
        """
        if not self.es_arbol():
            return None, None, None, None, "Error: El grafo no es un árbol válido"

        exc = self.calcular_excentricidades()
        radio    = min(exc.values())
        diametro = max(exc.values())
        centro   = [v for v, e in exc.items() if e == radio]
        detalles = self.generar_detalles(exc, centro, radio, diametro)
        return centro, exc, radio, diametro, detalles

    # ── Pasos del algoritmo (poda de hojas) ───────────────────────────────────
    def generar_pasos_algoritmo(self):
        """
        Genera los pasos del algoritmo de centro eliminando hojas
        (vértices de grado 1) iterativamente, hasta que queden ≤ 2 vértices.
        """
        pasos = []
        vertices_activos = set(range(self.num_vertices))
        aristas_activas  = self.aristas.copy()
        etiquetas_activas = self.etiquetas.copy()
        iteracion = 0

        # Paso 0: árbol original
        pasos.append({
            'titulo': 'Paso 0: Árbol Original',
            'descripcion': (f' Árbol con {len(vertices_activos)} vértices '
                            f'y {len(aristas_activas)} aristas'),
            'vertices_activos': sorted(list(vertices_activos)),
            'aristas': aristas_activas.copy(),
            'etiquetas': etiquetas_activas.copy(),
            'vertices_eliminados': []
        })

        while len(vertices_activos) > 2:
            iteracion += 1

            # Calcular grados
            grados = {v: 0 for v in vertices_activos}
            for o, d in aristas_activas:
                if o in vertices_activos and d in vertices_activos:
                    grados[o] += 1
                    grados[d] += 1

            hojas = [v for v in vertices_activos if grados[v] == 1]
            if not hojas:
                break

            hojas_et  = [self.etiquetas[h] for h in sorted(hojas)]
            grados_txt = ", ".join(
                [f"{self.etiquetas[h]}(grado={grados[h]})" for h in sorted(hojas)])

            # Paso a: identificar hojas
            pasos.append({
                'titulo': f'Iteración {iteracion}a: Identificar Hojas',
                'descripcion': (f' Hojas encontradas (grado 1): '
                                f'{", ".join(hojas_et)}\n   Detalles: {grados_txt}'),
                'vertices_activos': sorted(list(vertices_activos)),
                'aristas': aristas_activas.copy(),
                'etiquetas': etiquetas_activas.copy(),
                'vertices_eliminados': []
            })

            # Eliminar hojas
            for h in hojas:
                vertices_activos.remove(h)
            aristas_activas = [
                (o, d) for o, d in aristas_activas
                if o not in hojas and d not in hojas
            ]

            restantes_et = [self.etiquetas[v] for v in sorted(vertices_activos)]

            # Paso b: resultado tras eliminar
            pasos.append({
                'titulo': f'Iteración {iteracion}b: Después de Eliminar Hojas',
                'descripcion': (f'Eliminadas: {", ".join(hojas_et)}\n'
                                f'Quedan {len(vertices_activos)} vértices: '
                                f'{", ".join(restantes_et)}\n'
                                f' Aristas restantes: {len(aristas_activas)}'),
                'vertices_activos': sorted(list(vertices_activos)),
                'aristas': aristas_activas.copy(),
                'etiquetas': etiquetas_activas.copy(),
                'vertices_eliminados': hojas
            })

        # Paso final
        centro_verts = sorted(list(vertices_activos))
        centro_et    = [self.etiquetas[v] for v in centro_verts]
        if len(vertices_activos) == 1:
            desc = f'¡Centro encontrado!\n   Vértice central: {centro_et[0]}'
        else:
            desc = f' ¡Centro encontrado!\n   Vértices centrales: {", ".join(centro_et)}'

        pasos.append({
            'titulo': 'Resultado Final: Centro del Árbol',
            'descripcion': desc,
            'vertices_activos': centro_verts,
            'aristas': aristas_activas.copy(),
            'etiquetas': etiquetas_activas.copy(),
            'vertices_eliminados': []
        })

        return pasos

    # ── Detalles textuales ────────────────────────────────────────────────────
    def generar_detalles(self, excentricidades, centro, radio, diametro):
        """Genera un reporte detallado del análisis en texto plano."""
        det = "=== RESULTADO FINAL ===\n\n"
        det += "EXCENTRICIDADES:\n"
        for v in sorted(excentricidades.keys()):
            et  = self.etiquetas.get(v, str(v))
            exc = excentricidades[v]
            marca = " ← CENTRO ⭐" if v in centro else ""
            det += f"  Vértice {et}: e({et}) = {exc}{marca}\n"

        det += f"\n📏 RADIO del árbol: {radio}\n"
        det += f"📐 DIÁMETRO del árbol: {diametro}\n"
        det += "\n🎯 CENTRO del árbol: "
        centro_et = [self.etiquetas.get(v, str(v)) for v in centro]
        if len(centro) == 1:
            det += f"{centro_et[0]}\n"
        else:
            det += f"{{{', '.join(centro_et)}}}\n"

        det += "\n💡 INTERPRETACIÓN:\n"
        if len(centro) == 1:
            et = centro_et[0]
            det += f"El vértice {et} es el centro del árbol.\n"
            det += f"Su excentricidad es {radio}, la menor de todos los vértices.\n"
        else:
            det += f"Los vértices {{{', '.join(centro_et)}}} forman el centro.\n"
            det += f"Ambos tienen excentricidad {radio}.\n"

        return det

    # ── Tabla HTML de distancias ──────────────────────────────────────────────
    def obtener_matriz_distancias(self):
        """Genera la matriz completa de distancias."""
        return [self.calcular_distancias_desde(i)
                for i in range(self.num_vertices)]

    def generar_tabla_distancias_html(self):
        """Tabla HTML con distancias y columna de excentricidades, idéntica a referencia."""
        matriz = self.obtener_matriz_distancias()
        exc    = self.calcular_excentricidades()
        centro, _, _, _, _ = self.calcular_centro()
        if centro is None:
            centro = []

        html = ('<table border="1" cellpadding="8" cellspacing="0" '
                'style="border-collapse:collapse; margin:10px; font-family:Arial;">')

        # Encabezado
        html += ('<tr style="background-color:#9c724a; color:#FFEAC5; font-weight:bold;">'
                 '<th></th>')
        for j in range(self.num_vertices):
            html += f'<th>{self.etiquetas.get(j, str(j))}</th>'
        html += '<th>Exc.</th></tr>'

        # Filas
        for i in range(self.num_vertices):
            et_i = self.etiquetas.get(i, str(i))
            if i in centro:
                html += '<tr style="background-color:#E8D4B8; font-weight:bold;">'
            else:
                html += '<tr>'
            html += f'<th style="background-color:#D3C1A8; color:#2d1f15;">{et_i}</th>'
            for j in range(self.num_vertices):
                html += f'<td style="text-align:center;">{matriz[i][j]}</td>'
            if i in centro:
                html += (f'<td style="text-align:center; font-weight:bold; '
                         f'background-color:#8B6342; color:#FFEAC5;">'
                         f'{exc[i]} </td>')
            else:
                html += f'<td style="text-align:center; font-weight:bold;">{exc[i]}</td>'
            html += '</tr>'

        html += '</table>'
        return html
