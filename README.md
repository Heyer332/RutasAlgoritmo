# 🗺 Rutas entre Provincias del Perú — IA

Aplicación de escritorio que visualiza y compara **7 algoritmos de Inteligencia Artificial** para encontrar rutas entre las 196 provincias del Perú, usando distancias aéreas directas (vuelos en línea recta, calculadas con la fórmula Haversine).

Desarrollado como proyecto del curso de **Inteligencia Artificial** — Ingeniería de Sistemas.

---

##  Vista previa

> La aplicación muestra el mapa del Perú con todas las provincias. Al ejecutar un algoritmo, la ruta se dibuja animada sobre el mapa. El botón **Mejor Algoritmo** compara los 6 algoritmos de punto a punto y los anima uno por uno con colores distintos.

---

##  Algoritmos implementados

| # | Algoritmo | Tipo | Descripción |
|---|-----------|------|-------------|
| 1 | **BFS** | Búsqueda ciega | Menor número de escalas |
| 2 | **DFS** | Búsqueda ciega | Exploración en profundidad con poda |
| 3 | **Dijkstra** | Costo uniforme | Ruta de menor distancia garantizada |
| 4 | **A\*** | Heurístico | Dijkstra + heurística Haversine al destino |
| 5 | **Greedy** | Best-First | Siempre elige el vecino más prometedor |
| 6 | **Minimax** | Adversarial | Viajero vs. adversario con poda alfa-beta |
| 7 | **TSP — Genético** | Optimización | Recorre **todas** las provincias con algoritmo genético (OX crossover) |

> **Nota:** El TSP tiene un objetivo distinto a los demás — no busca la ruta más corta de A→B, sino la ruta que visita todas las provincias con la menor distancia total.

---

##  Estructura del proyecto

```
proyecto_rutas/
├── main.py                  # Punto de entrada — ejecutar esto
├── data/
│   ├── provincias.json      # 196 provincias con lat/lon
│   └── grafo.py             # Construcción del grafo con distancias Haversine
├── algorithms/
│   ├── bfs.py
│   ├── dfs.py
│   ├── dijkstra.py
│   ├── astar.py
│   ├── greedy.py
│   ├── minimax.py
│   └── tsp_ga.py            # TSP con Algoritmo Genético
├── ui/
│   └── main_window.py       # Ventana principal PyQt5
└── map/
    └── mapa.html            # Mapa Leaflet + OpenStreetMap
```

---

##  Requisitos

- **Python 3.10 o superior**
- **Windows 10/11** (también funciona en Linux/macOS con los mismos pasos)
- Conexión a internet la primera vez que abras el mapa (para cargar los tiles de OpenStreetMap)

---

##  Instalación y uso

### 1. Clonar el repositorio

Abre una terminal (CMD o PowerShell en Windows) y ejecuta:

```bash
git clone https://github.com/tu-usuario/proyecto_rutas.git
cd proyecto_rutas
```

> Reemplaza `tu-usuario` con tu nombre de usuario de GitHub.

---

### 2. Crear un entorno virtual (recomendado)

```bash
python -m venv venv
```

Activar el entorno:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

---

### 3. Instalar dependencias

```bash
pip install PyQt5 PyQtWebEngine
```

> Si tienes problemas con `PyQtWebEngine` en Windows, instala también:
> ```bash
> pip install PyQt5-Qt5 PyQt5-sip
> ```

---

### 4. Ejecutar la aplicación

```bash
python main.py
```

La ventana se abrirá **maximizada** automáticamente con el mapa del Perú cargado.

---

## 🖥 Cómo usar la aplicación

### Interfaz principal

La ventana está dividida en dos zonas:

- **Panel izquierdo** — controles de selección y resultados
- **Panel derecho** — mapa interactivo del Perú

---

### Ejecutar un algoritmo (punto a punto)

1. En el panel izquierdo, selecciona la **Provincia Origen** en el primer desplegable.
   - Puedes escribir el nombre para filtrar más rápido.
2. Selecciona la **Provincia Destino** en el segundo desplegable.
3. Elige el **Algoritmo** que quieres usar.
4. Presiona el botón **▶ Usar Algoritmo**.
5. La ruta aparecerá dibujada en el mapa:
   - 🟢 **Verde** — provincia de origen
   - 🔴 **Rojo** — provincia de destino
   - 🟡 **Naranja** — provincias intermedias (escalas)
6. En el panel izquierdo verás el **resultado**: distancia total en km, número de pasos y tiempo de ejecución.
7. La lista debajo muestra **cada provincia** por la que pasa la ruta en orden.

---

### Comparar todos los algoritmos — Mejor Algoritmo

1. Selecciona origen y destino como siempre.
2. Presiona el botón **🏆 Mejor Algoritmo**.
3. La aplicación ejecuta automáticamente los **6 algoritmos de punto a punto** (BFS, DFS, Dijkstra, A\*, Greedy, Minimax).
4. En el mapa se animará cada ruta **una por una en secuencia**, cada una con su propio color:

   | Algoritmo | Color |
   |-----------|-------|
   | BFS | Azul claro |
   | DFS | Lila |
   | Dijkstra | Verde |
   | A\* | Amarillo |
   | Greedy | Naranja |
   | Minimax | Rojo claro |

5. Al terminar, la ruta ganadora queda resaltada más gruesa y aparece una leyenda en el mapa.
6. En el panel izquierdo verás el **ranking completo** con distancia, número de pasos y tiempo de cada algoritmo, con medallas 🥇🥈🥉.

---

### TSP — Algoritmo Genético

1. En el desplegable de algoritmos selecciona **TSP — Algoritmo Genético**.
2. Presiona **▶ Usar Algoritmo**.
3. El algoritmo encontrará la ruta que **visita todas las provincias del Perú** partiendo desde el origen y terminando en el destino.
4. Tarda aproximadamente **1-2 segundos** ya que evoluciona una población de rutas por generaciones.

> El TSP no aparece en la comparación de "Mejor Algoritmo" porque su objetivo es diferente: no es ruta más corta de A→B, sino cobertura total del país.

---

### Limpiar el mapa

Presiona el botón **✕ Limpiar Mapa** para borrar todas las rutas dibujadas y volver al estado inicial.

---

## 📐 Detalles técnicos del grafo

- **196 provincias** del Perú con coordenadas geográficas reales.
- Cada provincia se conecta con sus vecinas dentro de un **radio de 150 km**.
- Para garantizar conectividad total: **mínimo 3 conexiones** y **máximo 10** por provincia.
- Las distancias se calculan con la **fórmula Haversine** (distancia real sobre la curvatura de la Tierra).
- El grafo es **bidireccional**: si A conecta con B, B conecta con A con la misma distancia.
- **196/196 nodos alcanzables** desde cualquier punto del grafo.

---

## ❓ Preguntas frecuentes

**¿Por qué DFS a veces no encuentra ruta?**
DFS explora en profundidad sin heurística. En rutas que requieren muchas escalas, el presupuesto de estados explorados se agota antes de encontrar el camino. Es una limitación conocida del algoritmo en grafos grandes.

**¿Por qué Greedy no siempre es el más rápido?**
Greedy elige siempre el vecino más prometedor según distancia acumulada, pero puede alejarse del destino en zonas geográficamente complejas.

**¿Por qué Dijkstra y A\* dan el mismo resultado?**
Ambos garantizan la ruta óptima. A\* llega al mismo resultado pero más rápido gracias a la heurística que lo guía hacia el destino.

**¿El mapa necesita internet?**
Sí, los tiles del mapa (imágenes del territorio) se cargan desde los servidores de OpenStreetMap. Los datos de provincias y el grafo son locales.

---

## 📦 Dependencias

```
PyQt5
PyQtWebEngine
```

El mapa usa **Leaflet.js** y **OpenStreetMap**, cargados desde CDN.


