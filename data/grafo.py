import json
import math
import os

_BASE = os.path.dirname(__file__)
_PROVINCIAS_PATH = os.path.join(_BASE, "provincias.json")

RADIO_KM  = 150
MIN_VEC   = 3
MAX_VEC   = 10

def cargar_provincias():
    with open(_PROVINCIAS_PATH, encoding="utf-8") as f:
        return json.load(f)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def construir_grafo(provincias, radio_km=RADIO_KM, min_vec=MIN_VEC, max_vec=MAX_VEC):
    n = len(provincias)
    # Precalcular todas las distancias
    dist = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            d = haversine(provincias[i]["lat"], provincias[i]["lon"],
                          provincias[j]["lat"], provincias[j]["lon"])
            dist[i][j] = dist[j][i] = round(d, 2)

    grafo = {i: {} for i in range(n)}

    for i in range(n):
        # Todos los vecinos dentro del radio, ordenados por distancia
        dentro = sorted([(dist[i][j], j) for j in range(n) if i != j and dist[i][j] <= radio_km],
                        key=lambda x: x[0])
        # Limitar al máximo
        dentro = dentro[:max_vec]

        # Si hay menos del mínimo, completar con los más cercanos fuera del radio
        if len(dentro) < min_vec:
            fuera = sorted([(dist[i][j], j) for j in range(n) if i != j and dist[i][j] > radio_km],
                           key=lambda x: x[0])
            dentro += fuera[:min_vec - len(dentro)]

        for d, j in dentro:
            grafo[i][j] = d
            grafo[j][i] = d  # asegurar bidireccional

    return grafo

def nombre_a_idx(provincias, nombre):
    nombre = nombre.lower()
    for i, p in enumerate(provincias):
        if p["provincia"].lower() == nombre:
            return i
    return None

PROVINCIAS = cargar_provincias()
GRAFO = construir_grafo(PROVINCIAS)
