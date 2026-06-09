def dfs(grafo, inicio, fin):
    """
    DFS con poda por costo (branch and bound iterativo).
    Budget máximo de estados para garantizar tiempo acotado.
    """
    mejor = {"camino": [], "costo": float("inf")}
    MAX_ESTADOS = 200_000
    estados = 0

    pila = [(inicio, [inicio], 0.0)]

    while pila and estados < MAX_ESTADOS:
        nodo, camino, costo = pila.pop()
        estados += 1

        if costo >= mejor["costo"]:
            continue

        if nodo == fin:
            mejor["camino"] = camino[:]
            mejor["costo"]  = costo
            continue

        visitados = set(camino)
        for vecino, peso in sorted(grafo[nodo].items(), key=lambda x: x[1]):
            if vecino not in visitados:
                pila.append((vecino, camino + [vecino], costo + peso))

    return mejor["camino"], round(mejor["costo"], 2)
