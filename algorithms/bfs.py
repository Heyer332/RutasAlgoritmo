from collections import deque

def bfs(grafo, inicio, fin):
    if inicio == fin:
        return [inicio], 0.0

    visitados = {inicio}
    cola = deque()
    cola.append((inicio, [inicio], 0.0))

    while cola:
        nodo, camino, costo = cola.popleft()
        for vecino, peso in sorted(grafo[nodo].items(), key=lambda x: x[1]):
            if vecino == fin:
                return camino + [vecino], round(costo + peso, 2)
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, camino + [vecino], costo + peso))

    return [], float("inf")
