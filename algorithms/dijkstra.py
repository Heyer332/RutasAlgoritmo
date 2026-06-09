import heapq

def dijkstra(grafo, inicio, fin):
    distancias = {n: float("inf") for n in grafo}
    distancias[inicio] = 0.0
    previo = {inicio: None}
    heap = [(0.0, inicio)]

    while heap:
        costo, nodo = heapq.heappop(heap)
        if nodo == fin:
            break
        if costo > distancias[nodo]:
            continue
        for vecino, peso in grafo[nodo].items():
            nuevo = costo + peso
            if nuevo < distancias[vecino]:
                distancias[vecino] = nuevo
                previo[vecino] = nodo
                heapq.heappush(heap, (nuevo, vecino))

    if distancias[fin] == float("inf"):
        return [], float("inf")

    camino = []
    nodo = fin
    while nodo is not None:
        camino.append(nodo)
        nodo = previo.get(nodo)
    camino.reverse()
    return camino, round(distancias[fin], 2)
