import heapq

def greedy(grafo, inicio, fin):
    # Greedy best-first: siempre expande el nodo con menor distancia acumulada al destino
    # Usa distancia al vecino más cercano como heurística (sin haversine explícita)
    visitados = set()
    # heap: (costo_acumulado, nodo, camino)
    heap = [(0.0, inicio, [inicio])]

    while heap:
        costo, nodo, camino = heapq.heappop(heap)

        if nodo in visitados:
            continue
        visitados.add(nodo)

        if nodo == fin:
            return camino, round(costo, 2)

        # Si el destino es vecino directo, ir inmediatamente
        if fin in grafo[nodo]:
            return camino + [fin], round(costo + grafo[nodo][fin], 2)

        for vecino, peso in sorted(grafo[nodo].items(), key=lambda x: x[1]):
            if vecino not in visitados:
                heapq.heappush(heap, (costo + peso, vecino, camino + [vecino]))

    return [], float("inf")
