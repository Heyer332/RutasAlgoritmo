import math
import heapq

def _haversine(p1, p2):
    R = 6371.0
    phi1, phi2 = math.radians(p1["lat"]), math.radians(p2["lat"])
    dphi = math.radians(p2["lat"] - p1["lat"])
    dlam = math.radians(p2["lon"] - p1["lon"])
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def minimax(grafo, inicio, fin, provincias):
    """
    Minimax adversarial sobre rutas:
    - MAX (viajero): elige el vecino que MINIMIZA el costo total estimado
    - MIN (adversario): elige el vecino que MAXIMIZA el costo total estimado
    Usa A* como guía inicial para tener un bound superior, luego aplica
    minimax con poda alpha-beta desde ese bound.
    """

    # Primero obtenemos un bound con Dijkstra para la poda
    dist = {n: float("inf") for n in grafo}
    dist[inicio] = 0.0
    prev = {inicio: None}
    heap = [(0.0, inicio)]
    while heap:
        c, n = heapq.heappop(heap)
        if n == fin: break
        if c > dist[n]: continue
        for v, p in grafo[n].items():
            nc = c + p
            if nc < dist[v]:
                dist[v] = nc
                prev[v] = n
                heapq.heappush(heap, (nc, v))

    # Reconstruir camino Dijkstra como bound
    bound_camino = []
    n = fin
    while n is not None:
        bound_camino.append(n)
        n = prev.get(n)
    bound_camino.reverse()
    bound_costo = dist[fin]

    if bound_costo == float("inf"):
        return [], float("inf")

    mejor = {"camino": bound_camino[:], "costo": bound_costo}

    def h(n):
        return _haversine(provincias[n], provincias[fin])

    MAX_DEPTH = 10

    def _mm(nodo, camino, costo, depth, es_max, alpha, beta):
        if nodo == fin:
            if costo < mejor["costo"]:
                mejor["camino"] = camino[:]
                mejor["costo"]  = costo
            return costo

        if depth == 0:
            return costo + h(nodo)

        if costo + h(nodo) >= mejor["costo"]:
            return mejor["costo"]

        visitados = set(camino)
        vecinos = [(v, p) for v, p in grafo[nodo].items() if v not in visitados]
        if not vecinos:
            return float("inf")

        # Ordenar por heurística para podar mejor
        vecinos = sorted(vecinos, key=lambda x: x[1] + h(x[0]))[:5]

        if es_max:
            valor = float("inf")
            for vecino, peso in vecinos:
                camino.append(vecino)
                r = _mm(vecino, camino, costo + peso, depth-1, False, alpha, beta)
                camino.pop()
                valor = min(valor, r)
                beta = min(beta, valor)
                if beta <= alpha:
                    break
            return valor
        else:
            valor = float("-inf")
            for vecino, peso in vecinos:
                camino.append(vecino)
                r = _mm(vecino, camino, costo + peso, depth-1, True, alpha, beta)
                camino.pop()
                valor = max(valor, r)
                alpha = max(alpha, valor)
                if beta <= alpha:
                    break
            return valor

    _mm(inicio, [inicio], 0.0, MAX_DEPTH, True, float("-inf"), float("inf"))
    return mejor["camino"], round(mejor["costo"], 2)
