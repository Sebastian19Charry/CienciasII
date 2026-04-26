# controlador/arboles/maximaController.py
# Lógica idéntica al proyecto de referencia CienciasII-main
# ÚNICA diferencia vs minimaController: sort DESCENDENTE en ejecutar_algoritmo
from PySide6.QtWidgets import QFileDialog
import json
from controlador.arboles.minimaController import (
    _UnionFind, _bfs_camino, _es_conexo, _tabla_inicio
)
from collections import deque
from itertools import combinations


class MaximaController:
    """
    Controlador para el Árbol de Expansión Máxima.
    Algoritmo: Kruskal con UnionFind (union por rango + path compression).
    Ordena aristas DESCENDENTE (mayor peso primero).
    
    Produce exactamente los mismos análisis que MinimaController:
    - Ramas / Cuerdas / Peso total
    - Circuitos del grafo original (DFS)
    - Circuitos fundamentales (BFS por cada cuerda)
    - Conjuntos de corte minimales
    - Matrices: adyacencia, incidencia, CF vs aristas (0/1), CF vs ponderaciones
    """

    def __init__(self, vista):
        self.vista = vista
        self.vertices = 0
        self.aristas = []
        self.etiquetas = {}
        self.ponderaciones = {}
        self.arbol_aristas = []
        self.peso_total = 0

    # ── Callbacks del VisualizadorGrafo ─────────────────────────────────────
    def actualizar_etiqueta(self, indice, nueva_etiqueta):
        self.etiquetas[indice] = nueva_etiqueta

    def actualizar_ponderacion(self, arista, ponderacion):
        if isinstance(ponderacion, str) and ponderacion.strip():
            try:
                self.ponderaciones[arista] = float(ponderacion)
            except ValueError:
                self.ponderaciones[arista] = ponderacion
        elif isinstance(ponderacion, (int, float)):
            self.ponderaciones[arista] = ponderacion
        else:
            self.ponderaciones.pop(arista, None)

    # ── Gestión del grafo ────────────────────────────────────────────────────
    def crear_grafo(self):
        self.vertices = self.vista.vertices_spin.value()
        self.aristas = []
        self.etiquetas = {i: str(i + 1) for i in range(self.vertices)}
        self.ponderaciones = {}
        self._refresh_visual_grafo()

    def agregar_arista(self):
        if self.vertices == 0:
            self._dlg("Error", "Primero debes crear el grafo.")
            return
        from vista.dialogo_arista import DialogoArista
        dlg = DialogoArista(self.vertices, self.vista, self.etiquetas)
        if dlg.exec():
            arista = dlg.get_arista()
            if arista[0] == arista[1]:
                self._dlg("Error", "Los nodos origen y destino deben ser diferentes.")
                return
            if arista not in self.aristas:
                self.aristas.append(arista)
            peso = dlg.get_peso() if hasattr(dlg, 'get_peso') else 1
            self.ponderaciones[arista] = peso
            self._refresh_visual_grafo()

    def eliminar_arista(self):
        if not self.aristas:
            self._dlg("Error", "No hay aristas para eliminar.")
            return
        from vista.dialogo_arista import DialogoArista
        dlg = DialogoArista(self.vertices, self.vista, self.etiquetas)
        if dlg.exec():
            arista = dlg.get_arista()
            if arista in self.aristas:
                self.aristas.remove(arista)
                self.ponderaciones.pop(arista, None)
                self._refresh_visual_grafo()
            else:
                self._dlg("Error", "La arista especificada no existe.")

    def limpiar_grafo(self):
        self.vertices = 0
        self.aristas = []
        self.etiquetas = {}
        self.ponderaciones = {}
        self.vista.visual_grafo.set_grafo(0, [], {}, {})
        self.vista.vertices_spin.setValue(4)
        self.limpiar_resultado()

    def guardar_grafo(self):
        if self.vertices == 0:
            self._dlg("Error", "No hay grafo para guardar.")
            return
        archivo, _ = QFileDialog.getSaveFileName(
            self.vista, "Guardar Grafo", "", "JSON Files (*.json)")
        if archivo:
            datos = {
                'vertices': self.vertices,
                'aristas': self.aristas,
                'etiquetas': self.etiquetas,
                'ponderaciones': {str(k): v for k, v in self.ponderaciones.items()}
            }
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            self._dlg("Éxito", "Grafo guardado correctamente.")

    def cargar_grafo(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self.vista, "Cargar Grafo", "", "JSON Files (*.json)")
        if not archivo:
            return
        with open(archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        self.vertices = datos['vertices']
        self.aristas = [tuple(a) for a in datos['aristas']]
        self.etiquetas = {int(k): v for k, v in datos.get('etiquetas', {}).items()}
        self.ponderaciones = {}
        for k, v in datos.get('ponderaciones', {}).items():
            try:
                arista_tuple = tuple(map(int, k.strip('()').split(', ')))
                self.ponderaciones[arista_tuple] = v
            except Exception:
                pass
        self.vista.vertices_spin.setValue(self.vertices)
        self._refresh_visual_grafo()
        self._dlg("Éxito", "Grafo cargado correctamente.")

    def limpiar_resultado(self):
        self.arbol_aristas = []
        self.peso_total = 0
        self.vista.visual_arbol.set_grafo(0, [], {}, {})
        for attr in ('info_text', 'circuitos_text', 'circuitos_fund_text',
                     'conjuntos_text', 'matrices_text'):
            if hasattr(self.vista, attr):
                getattr(self.vista, attr).setHtml("")

    # ── Algoritmo principal: Kruskal Máximo ──────────────────────────────────
    def ejecutar_algoritmo(self):
        if self.vertices < 2:
            self._dlg("Error", "El grafo necesita al menos 2 vértices.")
            return
        if not self.aristas:
            self._dlg("Error", "El grafo necesita al menos una arista.")
            return

        aristas_con_peso = []
        for arista in self.aristas:
            peso = self.ponderaciones.get(arista, 1)
            try:
                peso = float(peso)
            except (ValueError, TypeError):
                peso = 1
            aristas_con_peso.append((peso, arista))

        # Ordenar DESCENDENTE → máxima  ← única diferencia con mínima
        aristas_con_peso.sort(reverse=True)

        uf = _UnionFind(self.vertices)
        self.arbol_aristas = []
        self.peso_total = 0

        for peso, arista in aristas_con_peso:
            u, v = arista
            if uf.unir(u, v):
                self.arbol_aristas.append(arista)
                self.peso_total += peso
                if len(self.arbol_aristas) == self.vertices - 1:
                    break

        if len(self.arbol_aristas) < self.vertices - 1:
            self._dlg("Advertencia",
                      f"El grafo no es conexo.\n"
                      f"Se generó un bosque con {len(self.arbol_aristas)} aristas\n"
                      f"en lugar de {self.vertices - 1}.")

        self._mostrar_resultados()

    # ── Mostrar resultados ───────────────────────────────────────────────────
    def _mostrar_resultados(self):
        ponds_arbol = {a: self.ponderaciones[a]
                       for a in self.arbol_aristas if a in self.ponderaciones}
        self.vista.visual_arbol.set_grafo(
            self.vertices, self.arbol_aristas, self.etiquetas, ponds_arbol)

        ramas = self.arbol_aristas
        cuerdas = [a for a in self.aristas if a not in ramas]

        html = "<h3>Árbol de Expansión Máxima</h3>"
        html += f"<p><b>Peso total:</b> {self.peso_total}</p>"
        html += f"<p><b>Aristas en el árbol:</b> {len(ramas)}</p>"
        html += "<h4>Ramas (Aristas del Árbol):</h4><ul>"
        for a in ramas:
            eu = self.etiquetas.get(a[0], str(a[0]+1))
            ev = self.etiquetas.get(a[1], str(a[1]+1))
            p = self.ponderaciones.get(a, 1)
            html += f"<li>({eu}, {ev}) = {p}</li>"
        html += "</ul>"
        if cuerdas:
            html += "<h4>Cuerdas (Aristas NO usadas):</h4><ul>"
            for a in cuerdas:
                eu = self.etiquetas.get(a[0], str(a[0]+1))
                ev = self.etiquetas.get(a[1], str(a[1]+1))
                p = self.ponderaciones.get(a, 1)
                html += f"<li>({eu}, {ev}) = {p}</li>"
            html += "</ul>"
        else:
            html += "<p><i>No hay cuerdas.</i></p>"
        self.vista.info_text.setHtml(html)

        self._analizar_circuitos_original()
        self._analizar_circuitos_fundamentales()
        self._analizar_conjuntos_corte()
        self._generar_matrices()

        self._dlg("Árbol Generado",
                  f"Árbol de expansión máxima generado.\nPeso total: {self.peso_total}")

    # ── Circuitos del grafo original (DFS) ────────────────────────────────────
    def _analizar_circuitos_original(self):
        grafo = {i: [] for i in range(self.vertices)}
        for u, v in self.aristas:
            grafo[u].append(v)
            grafo[v].append(u)

        encontrados = []

        def dfs(inicio, actual, visitados, camino, padre):
            visitados.add(actual)
            camino.append(actual)
            for vecino in grafo[actual]:
                if vecino == padre:
                    continue
                if vecino == inicio and len(camino) >= 3:
                    norm = tuple(sorted(camino))
                    if norm not in encontrados:
                        encontrados.append(norm)
                elif vecino not in visitados:
                    dfs(inicio, vecino, visitados, camino, actual)
            camino.pop()
            visitados.remove(actual)

        for v in range(self.vertices):
            dfs(v, v, set(), [], -1)

        html = "<h3>Circuitos del Grafo Original</h3>"
        if encontrados:
            for idx, ciclo in enumerate(encontrados, 1):
                ciclo_list = list(ciclo)
                ponds = []
                for i in range(len(ciclo_list)):
                    u, v = ciclo_list[i], ciclo_list[(i+1) % len(ciclo_list)]
                    p = (self.ponderaciones.get((u, v))
                         or self.ponderaciones.get((v, u)) or 1)
                    ponds.append(str(p))
                et = [self.etiquetas.get(v, str(v+1)) for v in ciclo_list]
                html += (f"<p><b>Circuito {idx}:</b> "
                         f"{' → '.join(et)} → {et[0]}<br>"
                         f"<b>Ponderaciones:</b> ({', '.join(ponds)})</p>")
        else:
            html += "<p><i>No se encontraron circuitos.</i></p>"
        self.vista.circuitos_text.setHtml(html)

    # ── Circuitos fundamentales (BFS) ────────────────────────────────────────
    def _analizar_circuitos_fundamentales(self):
        cuerdas = [a for a in self.aristas if a not in self.arbol_aristas]
        if not cuerdas:
            self.vista.circuitos_fund_text.setHtml(
                "<p>No hay circuitos fundamentales (no hay cuerdas).</p>")
            return

        html = f"<h3>Circuitos Fundamentales</h3>"
        html += f"<p>Total: {len(cuerdas)} circuito(s)</p>"

        for idx, cuerda in enumerate(cuerdas, 1):
            u, v = cuerda
            camino = _bfs_camino(u, v, self.arbol_aristas, self.vertices)
            if camino:
                ponds = []
                for i in range(len(camino) - 1):
                    o, d = camino[i], camino[i+1]
                    p = (self.ponderaciones.get((o, d))
                         or self.ponderaciones.get((d, o)) or 1)
                    ponds.append(str(p))
                peso_cuerda = (self.ponderaciones.get(cuerda)
                               or self.ponderaciones.get((v, u)) or 1)
                ponds.append(str(peso_cuerda))
                eu = self.etiquetas.get(u, str(u+1))
                ev = self.etiquetas.get(v, str(v+1))
                circuito_et = [self.etiquetas.get(n, str(n+1)) for n in camino]
                html += (f"<p><b>CF{idx}:</b> (con cuerda ({eu}, {ev}))<br>"
                         f"<b>Camino:</b> {' → '.join(circuito_et)} → {eu}<br>"
                         f"<b>Ponderaciones:</b> ({', '.join(ponds)})</p>")

        self.vista.circuitos_fund_text.setHtml(html)

    # ── Conjuntos de corte minimales ─────────────────────────────────────────
    def _analizar_conjuntos_corte(self):
        html = "<h3>Conjuntos de Corte</h3>"
        html += "<p>Conjuntos minimales de aristas que al eliminarlas hacen el grafo inconexo:</p>"

        conjuntos = []
        max_t = min(len(self.aristas), 4)

        for tamano in range(1, max_t + 1):
            for combo in combinations(self.aristas, tamano):
                combo_list = list(combo)
                if any(set(cc).issubset(set(combo_list)) for cc in conjuntos):
                    continue
                restantes = [a for a in self.aristas if a not in combo]
                if not _es_conexo(restantes, self.vertices):
                    es_minimal = True
                    if len(combo_list) > 1:
                        for a in combo_list:
                            sin_una = [x for x in combo_list if x != a]
                            temp = [x for x in self.aristas if x not in sin_una]
                            if not _es_conexo(temp, self.vertices):
                                es_minimal = False
                                break
                    if es_minimal:
                        conjuntos.append(combo_list)

        if conjuntos:
            for idx, conj in enumerate(conjuntos, 1):
                parts = []
                for a in conj:
                    eu = self.etiquetas.get(a[0], str(a[0]+1))
                    ev = self.etiquetas.get(a[1], str(a[1]+1))
                    p = (self.ponderaciones.get(a)
                         or self.ponderaciones.get((a[1], a[0])) or 1)
                    parts.append(f"({eu},{ev})={p}")
                html += f"<p><b>CC{idx}:</b> {{{', '.join(parts)}}}</p>"
        else:
            html += "<p><i>No se encontraron conjuntos de corte.</i></p>"

        self.vista.conjuntos_text.setHtml(html)

    # ── Matrices ─────────────────────────────────────────────────────────────
    def _generar_matrices(self):
        ramas = self.arbol_aristas
        cuerdas = [a for a in self.aristas if a not in ramas]

        html = "<div style='max-width:100%; overflow-x:auto;'>"

        # Adyacencia
        ady = [[0] * self.vertices for _ in range(self.vertices)]
        for u, v in ramas:
            ady[u][v] = ady[v][u] = 1

        html += "<h3>Matriz de Adyacencia (del Árbol)</h3>"
        html += _tabla_inicio()
        html += "<tr style='background:#FFDBB5;'><th style='padding:10px;'></th>"
        for i in range(self.vertices):
            html += f"<th style='padding:10px;'>{self.etiquetas.get(i, str(i+1))}</th>"
        html += "</tr>"
        for i in range(self.vertices):
            html += f"<tr><th style='background:#FFDBB5;padding:10px;'>{self.etiquetas.get(i, str(i+1))}</th>"
            for j in range(self.vertices):
                html += f"<td align='center' style='padding:10px;'>{ady[i][j]}</td>"
            html += "</tr>"
        html += "</table><br><br>"

        # Incidencia
        inc = [[0] * len(ramas) for _ in range(self.vertices)]
        for idx, (u, v) in enumerate(ramas):
            inc[u][idx] = inc[v][idx] = 1

        html += "<h3>Matriz de Incidencia (del Árbol)</h3>"
        html += _tabla_inicio()
        html += "<tr style='background:#FFDBB5;'><th style='padding:10px;'>Vértices</th>"
        for idx, (u, v) in enumerate(ramas):
            eu = self.etiquetas.get(u, str(u+1))
            ev = self.etiquetas.get(v, str(v+1))
            html += f"<th style='padding:10px;'>e{idx+1}<br>({eu},{ev})</th>"
        html += "</tr>"
        for i in range(self.vertices):
            html += f"<tr><th style='background:#FFDBB5;padding:10px;'>{self.etiquetas.get(i, str(i+1))}</th>"
            for j in range(len(ramas)):
                html += f"<td align='center' style='padding:10px;'>{inc[i][j]}</td>"
            html += "</tr>"
        html += "</table><br><br>"

        # Circuitos
        if cuerdas:
            todas = list(self.aristas)

            html += "<h3>Matriz: Circuitos Fundamentales vs Aristas</h3>"
            html += "<p style='font-size:11px;color:#6C4E31;'>1 = pertenece al circuito, 0 = no pertenece</p>"
            html += _tabla_inicio()
            html += "<tr style='background:#FFDBB5;'><th style='padding:10px;'>Circuito</th>"
            for a in todas:
                eu = self.etiquetas.get(a[0], str(a[0]+1))
                ev = self.etiquetas.get(a[1], str(a[1]+1))
                html += f"<th style='padding:10px;'>({eu},{ev})</th>"
            html += "</tr>"

            for idx_c, cuerda in enumerate(cuerdas, 1):
                u, v = cuerda
                camino = _bfs_camino(u, v, ramas, self.vertices)
                en_circ = set()
                if camino:
                    for i in range(len(camino) - 1):
                        en_circ.add((camino[i], camino[i+1]))
                        en_circ.add((camino[i+1], camino[i]))
                    en_circ.add(cuerda)
                    en_circ.add((v, u))

                html += f"<tr><th style='background:#FFDBB5;padding:10px;'>CF{idx_c}</th>"
                for a in todas:
                    val = "1" if a in en_circ else "0"
                    bold = " font-weight:bold;" if val == "1" else ""
                    html += f"<td align='center' style='padding:10px;{bold}'>{val}</td>"
                html += "</tr>"
            html += "</table><br><br>"

            html += "<h3>Matriz: Circuitos vs Ponderaciones</h3>"
            html += _tabla_inicio()
            html += "<tr style='background:#FFDBB5;'><th style='padding:10px;'>Circuito</th>"
            for a in todas:
                p = (self.ponderaciones.get(a)
                     or self.ponderaciones.get((a[1], a[0])) or 1)
                html += f"<th style='padding:10px;'>{p}</th>"
            html += "</tr>"

            for idx_c, cuerda in enumerate(cuerdas, 1):
                u, v = cuerda
                camino = _bfs_camino(u, v, ramas, self.vertices)
                en_circ = set()
                if camino:
                    for i in range(len(camino) - 1):
                        en_circ.add((camino[i], camino[i+1]))
                        en_circ.add((camino[i+1], camino[i]))
                    en_circ.add(cuerda)
                    en_circ.add((v, u))

                html += f"<tr><th style='background:#FFDBB5;padding:10px;'>CF{idx_c}</th>"
                for a in todas:
                    if a in en_circ:
                        p = (self.ponderaciones.get(a)
                             or self.ponderaciones.get((a[1], a[0])) or 1)
                        html += f"<td align='center' style='padding:10px;font-weight:bold;'>{p}</td>"
                    else:
                        html += "<td align='center' style='padding:10px;'>-</td>"
                html += "</tr>"
            html += "</table>"

        html += "</div>"
        self.vista.matrices_text.setHtml(html)

    # ── Utilidades ────────────────────────────────────────────────────────────
    def _refresh_visual_grafo(self):
        self.vista.visual_grafo.set_grafo(
            self.vertices, self.aristas, self.etiquetas, self.ponderaciones)

    def _dlg(self, titulo, mensaje):
        from vista.dialogo_clave import DialogoClave
        DialogoClave(0, titulo, "mensaje", self.vista, mensaje).exec()
