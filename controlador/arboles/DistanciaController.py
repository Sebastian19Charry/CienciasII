# controlador/arboles/distanciaController.py
# Lógica idéntica al proyecto de referencia CienciasII-main
from collections import deque


class DistanciaController:
    """
    Controlador para calcular la distancia entre dos árboles ponderados.

    Fórmula (igual a referencia):
        D(T1, T2) = (Σ |w1(e) - w2(e)|) / 2

    Donde w1(e) es la ponderación de e en T1, w2(e) en T2.
    Si la arista no existe en un árbol su ponderación es 0.

    Produce:
    - Conjuntos SV, SA de cada árbol
    - Unión / intersección de vértices y aristas
    - Tabla de diferencias por arista
    - Reporte HTML completo
    """

    def __init__(self):
        self.arbol1 = {'vertices': 0, 'aristas': [], 'etiquetas': {}, 'ponderaciones': {}}
        self.arbol2 = {'vertices': 0, 'aristas': [], 'etiquetas': {}, 'ponderaciones': {}}

    # ── Configuración ────────────────────────────────────────────────────────
    def set_arbol1(self, num_vertices, aristas, etiquetas, ponderaciones=None):
        """Configura el árbol 1."""
        self.arbol1 = {
            'vertices':     num_vertices,
            'aristas':      aristas.copy(),
            'etiquetas':    etiquetas.copy() if etiquetas else {},
            'ponderaciones': ponderaciones.copy() if ponderaciones else {}
        }

    def set_arbol2(self, num_vertices, aristas, etiquetas, ponderaciones=None):
        """Configura el árbol 2."""
        self.arbol2 = {
            'vertices':     num_vertices,
            'aristas':      aristas.copy(),
            'etiquetas':    etiquetas.copy() if etiquetas else {},
            'ponderaciones': ponderaciones.copy() if ponderaciones else {}
        }

    # ── Validaciones ─────────────────────────────────────────────────────────
    def es_arbol(self, arbol):
        """Verifica si el grafo es un árbol (n-1 aristas y conexo)."""
        v = arbol['vertices']
        a = arbol['aristas']
        if not a:
            return v == 1
        if len(a) != v - 1:
            return False
        return self.es_conexo(arbol)

    def es_conexo(self, arbol):
        """Verifica conexidad por BFS."""
        v = arbol['vertices']
        a = arbol['aristas']
        if v == 0:
            return True
        ady = [[] for _ in range(v)]
        for o, d in a:
            ady[o].append(d)
            ady[d].append(o)
        visitados = [False] * v
        cola = deque([0])
        visitados[0] = True
        count = 1
        while cola:
            actual = cola.popleft()
            for nb in ady[actual]:
                if not visitados[nb]:
                    visitados[nb] = True
                    cola.append(nb)
                    count += 1
        return count == v

    # ── Conjuntos SV y SA ────────────────────────────────────────────────────
    def obtener_conjuntos_vertices_aristas(self, arbol):
        """
        Retorna (SV, SA) donde:
          SV = conjunto de etiquetas de vértices (str)
          SA = dict { (etiq_u, etiq_v) : ponderacion } con etiquetas ordenadas
        """
        et    = arbol['etiquetas']
        ars   = arbol['aristas']
        ponds = arbol.get('ponderaciones', {})

        sv = set(et.values())
        sa = {}
        for o, d in ars:
            eto  = et.get(o, str(o))
            etd  = et.get(d, str(d))
            key  = tuple(sorted([eto, etd]))
            akey = tuple(sorted([o, d]))
            pond = ponds.get(akey, 1)
            sa[key] = pond

        return sv, sa

    # ── Algoritmo principal ───────────────────────────────────────────────────
    def calcular_distancia_arboles(self):
        """
        Calcula D(T1,T2) = (Σ |w1(e) - w2(e)|) / 2
        Retorna (distancia, detalles_dict) o (None, mensaje_error)
        """
        if not self.es_arbol(self.arbol1):
            return None, "El grafo 1 no es un árbol válido"
        if not self.es_arbol(self.arbol2):
            return None, "El grafo 2 no es un árbol válido"

        sv1, sa1 = self.obtener_conjuntos_vertices_aristas(self.arbol1)
        sv2, sa2 = self.obtener_conjuntos_vertices_aristas(self.arbol2)

        aristas1 = set(sa1.keys())
        aristas2 = set(sa2.keys())

        vertices_union        = sv1 | sv2
        vertices_interseccion = sv1 & sv2
        aristas_union         = aristas1 | aristas2
        aristas_interseccion  = aristas1 & aristas2
        solo_en_t1            = aristas1 - aristas2
        solo_en_t2            = aristas2 - aristas1

        suma_diferencias = 0
        detalles_aristas = []

        for arista in sorted(aristas_union):
            w1 = sa1.get(arista, 0)
            w2 = sa2.get(arista, 0)
            diff = abs(w1 - w2)
            suma_diferencias += diff

            if arista in solo_en_t1:
                ubicacion = 'Solo en T1'
            elif arista in solo_en_t2:
                ubicacion = 'Solo en T2'
            else:
                ubicacion = 'En ambos'

            detalles_aristas.append({
                'arista':    arista,
                'en_t1':     arista in aristas1,
                'en_t2':     arista in aristas2,
                'w1':        w1,
                'w2':        w2,
                'diferencia': diff,
                'ubicacion': ubicacion
            })

        distancia = suma_diferencias / 2

        suma_union        = sum(max(sa1.get(a, 0), sa2.get(a, 0)) for a in aristas_union)
        suma_interseccion = sum(min(sa1.get(a, 0), sa2.get(a, 0)) for a in aristas_interseccion)

        detalles = {
            'arbol1': {
                'sv': sv1,
                'sa': sa1,
                'cardinalidad_sv': len(sv1),
                'cardinalidad_sa': len(sa1),
                'suma_ponderaciones': sum(sa1.values())
            },
            'arbol2': {
                'sv': sv2,
                'sa': sa2,
                'cardinalidad_sv': len(sv2),
                'cardinalidad_sa': len(sa2),
                'suma_ponderaciones': sum(sa2.values())
            },
            'operaciones': {
                'vertices_union':           vertices_union,
                'vertices_interseccion':    vertices_interseccion,
                'aristas_union':            aristas_union,
                'aristas_interseccion':     aristas_interseccion,
                'aristas_solo_t1':          solo_en_t1,
                'aristas_solo_t2':          solo_en_t2,
                'card_vertices_union':      len(vertices_union),
                'card_vertices_interseccion': len(vertices_interseccion),
                'card_aristas_union':       len(aristas_union),
                'card_aristas_interseccion': len(aristas_interseccion),
                'suma_union':               suma_union,
                'suma_interseccion':        suma_interseccion,
                'suma_diferencias':         suma_diferencias,
                'detalles_aristas':         detalles_aristas
            },
            'distancia': distancia
        }

        return distancia, detalles

    # ── Reporte HTML ─────────────────────────────────────────────────────────
    def generar_reporte_html(self, detalles):
        """Genera el reporte HTML completo, idéntico a la referencia."""
        if not detalles:
            return "<p>No hay datos disponibles</p>"

        a1   = detalles['arbol1']
        a2   = detalles['arbol2']
        ops  = detalles['operaciones']
        dist = detalles['distancia']

        html = "<div style='font-family:Arial; color:#2d1f15;'>"

        # Título
        html += ("<h3 style='color:#6C4E31; border-bottom:2px solid #bf8f62; "
                 "padding-bottom:5px;'>Cálculo de Distancia entre Árboles</h3>")

        # Árbol 1
        html += "<h4 style='color:#8B6342; margin-top:20px;'>Árbol T1</h4>"
        html += f"<p><b>ST1 =</b> {{{', '.join(sorted(a1['sv']))}}}</p>"
        html += "<p><b>AT1 =</b> {{"
        html += ', '.join(f"({a[0]},{a[1]}):w={w}" for a, w in sorted(a1['sa'].items()))
        html += (f"}}</p><p style='margin-left:20px;'>|ST1| = {a1['cardinalidad_sv']}, "
                 f"|AT1| = {a1['cardinalidad_sa']}, suma = {a1['suma_ponderaciones']}</p>")

        # Árbol 2
        html += "<h4 style='color:#8B6342; margin-top:20px;'>Árbol T2</h4>"
        html += f"<p><b>ST2 =</b> {{{', '.join(sorted(a2['sv']))}}}</p>"
        html += "<p><b>AT2 =</b> {{"
        html += ', '.join(f"({a[0]},{a[1]}):w={w}" for a, w in sorted(a2['sa'].items()))
        html += (f"}}</p><p style='margin-left:20px;'>|ST2| = {a2['cardinalidad_sv']}, "
                 f"|AT2| = {a2['cardinalidad_sa']}, suma = {a2['suma_ponderaciones']}</p>")

        # Tabla de aristas
        html += "<h4 style='color:#7a5a3e; margin-top:20px;'>Análisis de Aristas y Ponderaciones</h4>"
        html += "<table style='border-collapse:collapse; margin:10px 0; width:100%;'>"
        for cabecera in ["Arista", "w1(e)", "w2(e)", "|w1(e) - w2(e)|", "Ubicación"]:
            html += f"<th style='border:1px solid #8B6342; padding:8px; background:#E8D4B8; font-weight:bold;'>{cabecera}</th>"
        html = html.replace(
            "<table style='border-collapse:collapse; margin:10px 0; width:100%;'>",
            "<table style='border-collapse:collapse; margin:10px 0; width:100%;'><tr>"
        )
        html += "</tr>"

        for det in ops['detalles_aristas']:
            a    = det['arista']
            w1   = det['w1']
            w2   = det['w2']
            diff = det['diferencia']
            ub   = det['ubicacion']
            if ub == 'En ambos':
                bg = '#E8F5E9' if diff == 0 else '#FFF9C4'
            else:
                bg = '#d7ab8d'
            html += (f"<tr style='background-color:{bg};'>"
                     f"<td style='border:1px solid #8B6342;padding:8px;text-align:center;'>({a[0]},{a[1]})</td>"
                     f"<td style='border:1px solid #8B6342;padding:8px;text-align:center;'>{w1}</td>"
                     f"<td style='border:1px solid #8B6342;padding:8px;text-align:center;'>{w2}</td>"
                     f"<td style='border:1px solid #8B6342;padding:8px;text-align:center;font-weight:bold;'>{diff}</td>"
                     f"<td style='border:1px solid #8B6342;padding:8px;text-align:center;'>{ub}</td>"
                     f"</tr>")
        html += "</table>"

        # Cálculo
        html += "<h4 style='color:#8B6342; margin-top:20px;'>Cálculo de la Distancia</h4>"
        html += ("<div style='background:#FFFEF7; border:2px solid #bf8f62; "
                 "border-radius:8px; padding:15px; margin:10px 0;'>")
        html += ("<p style='margin:5px 0;'><b>Paso 1:</b> Calcular "
                 "(AT1 ∪ AT2) - (AT1 ∩ AT2)</p>")
        html += (f"<p style='margin:5px 0 5px 20px;'>"
                 f"(AT1 ∪ AT2) - (AT1 ∩ AT2) = {ops['suma_diferencias']}</p>")
        html += "<hr style='border:1px solid #bf8f62; margin:10px 0;'>"
        html += "<p style='margin:5px 0;'><b>Paso 2:</b> Dividir entre 2</p>"
        html += (f"<p style='margin:5px 0 5px 20px;'>"
                 f"D(T1,T2) = {ops['suma_diferencias']} / 2</p>")
        html += (f"<p style='margin:5px 0 5px 20px; font-size:18px;'>"
                 f"<b>D(T1,T2) = {dist}</b></p></div>")

        # Resultado final
        html += ("<div style='background:#FFFEF7; border:3px solid #6C4E31; "
                 "border-radius:8px; padding:15px; margin-top:20px;'>")
        html += f"<h3 style='color:#6C4E31; text-align:center; margin:0;'>DISTANCIA = {dist}</h3>"
        html += "</div>"

        # Interpretación
        html += "<h4 style='color:#8B6342; margin-top:20px;'>Interpretación</h4>"
        html += f"<p>La distancia entre los árboles T1 y T2 es <b>{dist}</b>.</p>"
        if dist == 0:
            html += ("<p style='color:#2E7D32;'><b>Los árboles son idénticos</b> - "
                     "tienen exactamente las mismas aristas con las mismas ponderaciones.</p>")
        else:
            html += (f"<p style='color:#F57C00;'>La suma total de diferencias absolutas "
                     f"de ponderaciones es <b>{ops['suma_diferencias']}</b>, "
                     f"lo que resulta en una distancia de <b>{dist}</b>.</p>")
            dif_count = sum(1 for d in ops['detalles_aristas'] if d['diferencia'] > 0)
            html += f"<p>Hay <b>{dif_count}</b> arista(s) con diferencias en ponderación.</p>"

        html += "</div>"
        return html
