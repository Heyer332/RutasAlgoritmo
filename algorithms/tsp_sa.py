import random
import math

def tsp_sa(grafo, inicio, fin, provincias, max_iter=5000, temp_init=1000.0, enfriamiento=0.995):
    # Solo usar nodos alcanzables desde inicio (grafo con radio limitado)
    # Construir ruta inicial via greedy
    nodos_alcanzables = set()
    cola = [inicio]
    while cola:
        n = cola.pop()
        if n in nodos_alcanzables:
            continue
        nodos_alcanzables.add(n)
        for v in grafo[n]:
            if v not in nodos_alcanzables:
                cola.append(v)

    intermedios = [x for x in nodos_alcanzables if x != inicio and x != fin]
    random.shuffle(intermedios)
    ruta = [inicio] + intermedios + [fin]

    def costo_ruta(r):
        total = 0.0
        for i in range(len(r) - 1):
            a, b = r[i], r[i+1]
            # Si no hay conexión directa, usar distancia haversine como penalización
            if b in grafo[a]:
                total += grafo[a][b]
            else:
                p1, p2 = provincias[a], provincias[b]
                R = 6371.0
                phi1, phi2 = math.radians(p1["lat"]), math.radians(p2["lat"])
                dphi = math.radians(p2["lat"] - p1["lat"])
                dlam = math.radians(p2["lon"] - p1["lon"])
                a2 = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
                total += 2 * R * math.asin(math.sqrt(a2)) * 3  # penalización x3
        return total

    mejor_ruta = ruta[:]
    mejor_costo = costo_ruta(mejor_ruta)
    actual_ruta = mejor_ruta[:]
    actual_costo = mejor_costo
    temp = temp_init

    for _ in range(max_iter):
        if len(actual_ruta) <= 3:
            break
        i = random.randint(1, len(actual_ruta) - 2)
        j = random.randint(1, len(actual_ruta) - 2)
        if i == j:
            continue
        nueva_ruta = actual_ruta[:]
        nueva_ruta[i], nueva_ruta[j] = nueva_ruta[j], nueva_ruta[i]
        nueva_ruta[0] = inicio
        nueva_ruta[-1] = fin

        nuevo_costo = costo_ruta(nueva_ruta)
        delta = nuevo_costo - actual_costo

        if delta < 0 or random.random() < math.exp(-delta / max(temp, 0.001)):
            actual_ruta = nueva_ruta
            actual_costo = nuevo_costo
            if actual_costo < mejor_costo:
                mejor_ruta = actual_ruta[:]
                mejor_costo = actual_costo

        temp *= enfriamiento

    return mejor_ruta, round(mejor_costo, 2)
