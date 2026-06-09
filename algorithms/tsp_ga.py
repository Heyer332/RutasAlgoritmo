import random
import math

def tsp_ga(grafo, inicio, fin, provincias,
           poblacion_size=80, generaciones=150,
           prob_mutacion=0.02, prob_cruce=0.8):

    n = len(provincias)
    intermedios = [x for x in range(n) if x != inicio and x != fin]

    def costo_ruta(ruta):
        total = 0.0
        for i in range(len(ruta) - 1):
            a, b = ruta[i], ruta[i+1]
            if b in grafo[a]:
                total += grafo[a][b]
            else:
                # Penalización: haversine * 2 si no hay conexión directa
                p1, p2 = provincias[a], provincias[b]
                R = 6371.0
                phi1 = math.radians(p1["lat"]); phi2 = math.radians(p2["lat"])
                dphi = math.radians(p2["lat"] - p1["lat"])
                dlam = math.radians(p2["lon"] - p1["lon"])
                aa = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
                total += 2 * 6371.0 * math.asin(math.sqrt(aa)) * 2
        return total

    def individuo_aleatorio():
        orden = intermedios[:]
        random.shuffle(orden)
        return [inicio] + orden + [fin]

    def cruce_ox(p1, p2):
        # Order Crossover (OX) sobre la parte intermedia
        size = len(intermedios)
        if size < 2:
            return p1[:], p2[:]
        a, b = sorted(random.sample(range(size), 2))
        seg1 = p1[1:1+size]
        seg2 = p2[1:1+size]
        hijo1_mid = seg1[a:b+1]
        resto = [x for x in seg2 if x not in hijo1_mid]
        hijo1_mid = resto[:a] + hijo1_mid + resto[a:]
        hijo2_mid = seg2[a:b+1]
        resto2 = [x for x in seg1 if x not in hijo2_mid]
        hijo2_mid = resto2[:a] + hijo2_mid + resto2[a:]
        return [inicio] + hijo1_mid + [fin], [inicio] + hijo2_mid + [fin]

    def mutar(ind):
        ind = ind[:]
        if len(intermedios) < 2:
            return ind
        if random.random() < prob_mutacion:
            i, j = random.sample(range(1, len(ind)-1), 2)
            ind[i], ind[j] = ind[j], ind[i]
        return ind

    def seleccion_torneo(poblacion, costos, k=3):
        candidatos = random.sample(list(zip(poblacion, costos)), min(k, len(poblacion)))
        return min(candidatos, key=lambda x: x[1])[0]

    # Población inicial
    poblacion = [individuo_aleatorio() for _ in range(poblacion_size)]
    costos = [costo_ruta(ind) for ind in poblacion]

    mejor_ruta = min(zip(poblacion, costos), key=lambda x: x[1])
    mejor_ind, mejor_costo = mejor_ruta[0][:], mejor_ruta[1]

    for gen in range(generaciones):
        nueva_poblacion = []
        nueva_costos = []

        # Elitismo: conservar el mejor
        nueva_poblacion.append(mejor_ind[:])
        nueva_costos.append(mejor_costo)

        while len(nueva_poblacion) < poblacion_size:
            p1 = seleccion_torneo(poblacion, costos)
            p2 = seleccion_torneo(poblacion, costos)
            if random.random() < prob_cruce:
                h1, h2 = cruce_ox(p1, p2)
            else:
                h1, h2 = p1[:], p2[:]
            h1 = mutar(h1)
            h2 = mutar(h2)
            for h in [h1, h2]:
                if len(nueva_poblacion) < poblacion_size:
                    nueva_poblacion.append(h)
                    nueva_costos.append(costo_ruta(h))

        poblacion = nueva_poblacion
        costos = nueva_costos

        gen_mejor = min(zip(poblacion, costos), key=lambda x: x[1])
        if gen_mejor[1] < mejor_costo:
            mejor_ind = gen_mejor[0][:]
            mejor_costo = gen_mejor[1]

    return mejor_ind, round(mejor_costo, 2)
