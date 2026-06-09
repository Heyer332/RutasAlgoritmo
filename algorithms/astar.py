import heapq
import math

def _haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def astar(grafo, inicio, fin, provincias):
    pf = provincias[fin]

    def h(n):
        pn = provincias[n]
        return _haversine(pn["lat"], pn["lon"], pf["lat"], pf["lon"])

    g = {n: float("inf") for n in grafo}
    g[inicio] = 0.0
    previo = {inicio: None}
    heap = [(h(inicio), 0.0, inicio)]

    while heap:
        f, costo, nodo = heapq.heappop(heap)
        if nodo == fin:
            break
        if costo > g[nodo]:
            continue
        for vecino, peso in grafo[nodo].items():
            nuevo_g = costo + peso
            if nuevo_g < g[vecino]:
                g[vecino] = nuevo_g
                previo[vecino] = nodo
                heapq.heappush(heap, (nuevo_g + h(vecino), nuevo_g, vecino))

    if g[fin] == float("inf"):
        return [], float("inf")

    camino = []
    nodo = fin
    while nodo is not None:
        camino.append(nodo)
        nodo = previo.get(nodo)
    camino.reverse()
    return camino, round(g[fin], 2)
