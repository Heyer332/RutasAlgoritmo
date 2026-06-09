import sys, os, json, time

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QListWidget,
    QSplitter, QFrame, QSizePolicy, QMessageBox,
    QProgressBar, QStatusBar
)
from PyQt5.QtCore    import Qt, QUrl, QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel       import QWebChannel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from data.grafo          import PROVINCIAS, GRAFO
from algorithms.bfs      import bfs
from algorithms.dfs      import dfs
from algorithms.dijkstra import dijkstra
from algorithms.astar    import astar
from algorithms.greedy   import greedy
from algorithms.minimax  import minimax
from algorithms.tsp_ga   import tsp_ga

ALGORITMOS = {
    "BFS (Búsqueda en Anchura)":     "bfs",
    "DFS (Búsqueda en Profundidad)": "dfs",
    "Dijkstra (Camino Más Corto)":   "dijkstra",
    "A* (A-Star Heurístico)":        "astar",
    "Greedy (Best-First)":           "greedy",
    "Minimax (Adversarial)":         "minimax",
    "TSP - Algoritmo Genético":      "tsp_ga",
}
ALGORITMOS_CMP    = ["bfs","dfs","dijkstra","astar","greedy","minimax"]
NOMBRES_DISPLAY   = {"bfs":"BFS","dfs":"DFS","dijkstra":"Dijkstra",
                     "astar":"A*","greedy":"Greedy","minimax":"Minimax"}

ESTILOS = """
QMainWindow,QWidget{background:#1a1a2e;color:#e0e0e0;
  font-family:'Segoe UI',sans-serif;font-size:13px;}
QLabel#titulo{font-size:16px;font-weight:bold;color:#4fc3f7;padding:8px 0;}
QLabel#sub{font-size:12px;color:#90a4ae;padding:2px 0;}
QComboBox{background:#16213e;border:1px solid #4fc3f7;border-radius:4px;
  padding:6px 10px;color:#e0e0e0;min-height:28px;}
QComboBox::drop-down{border:none;width:24px;}
QComboBox QAbstractItemView{background:#16213e;color:#e0e0e0;
  selection-background-color:#4fc3f7;}
QPushButton{background:#4fc3f7;color:#1a1a2e;border:none;border-radius:4px;
  padding:8px 14px;font-weight:bold;min-height:32px;}
QPushButton:hover{background:#81d4fa;}
QPushButton:pressed{background:#0288d1;}
QPushButton#btn_limpiar{background:#37474f;color:#e0e0e0;}
QPushButton#btn_limpiar:hover{background:#546e7a;}
QPushButton#btn_mejor{background:#ffd600;color:#1a1a2e;}
QPushButton#btn_mejor:hover{background:#ffea00;}
QListWidget{background:#16213e;border:1px solid #37474f;
  border-radius:4px;color:#e0e0e0;padding:4px;}
QListWidget::item{padding:4px 6px;border-bottom:1px solid #263238;}
QListWidget::item:selected{background:#4fc3f7;color:#1a1a2e;}
QFrame#panel{background:#16213e;border-radius:6px;}
QSplitter::handle{background:#37474f;width:3px;}
QProgressBar{border:1px solid #37474f;border-radius:3px;background:#16213e;height:6px;}
QProgressBar::chunk{background:#4fc3f7;border-radius:3px;}
QStatusBar{background:#16213e;color:#90a4ae;font-size:11px;}
"""

# ── Bridge mínimo: solo para saber que el HTML cargó ─────────────────────
class Bridge(QObject):
    def __init__(self): super().__init__(); self._listo=False
    @pyqtSlot()
    def pagina_lista(self): self._listo=True

# ── Workers ───────────────────────────────────────────────────────────────
class WorkerAlgoritmo(QThread):
    terminado = pyqtSignal(list, float, float)
    error     = pyqtSignal(str)
    def __init__(self, alg, inicio, fin):
        super().__init__(); self.alg=alg; self.inicio=inicio; self.fin=fin
    def run(self):
        try:
            t0=time.time(); i,f=self.inicio,self.fin; alg=self.alg
            if   alg=="bfs":      c,k=bfs(GRAFO,i,f)
            elif alg=="dfs":      c,k=dfs(GRAFO,i,f)
            elif alg=="dijkstra": c,k=dijkstra(GRAFO,i,f)
            elif alg=="astar":    c,k=astar(GRAFO,i,f,PROVINCIAS)
            elif alg=="greedy":   c,k=greedy(GRAFO,i,f)
            elif alg=="minimax":  c,k=minimax(GRAFO,i,f,PROVINCIAS)
            elif alg=="tsp_ga":   c,k=tsp_ga(GRAFO,i,f,PROVINCIAS)
            else: self.error.emit("Algoritmo no reconocido"); return
            self.terminado.emit(c,k,time.time()-t0)
        except Exception as e: self.error.emit(str(e))

class WorkerComparar(QThread):
    terminado = pyqtSignal(list)
    progreso  = pyqtSignal(str)
    def __init__(self, inicio, fin):
        super().__init__(); self.inicio=inicio; self.fin=fin
    def run(self):
        res=[]; i,f=self.inicio,self.fin
        fns={"bfs":lambda:bfs(GRAFO,i,f),"dfs":lambda:dfs(GRAFO,i,f),
             "dijkstra":lambda:dijkstra(GRAFO,i,f),"astar":lambda:astar(GRAFO,i,f,PROVINCIAS),
             "greedy":lambda:greedy(GRAFO,i,f),"minimax":lambda:minimax(GRAFO,i,f,PROVINCIAS)}
        for key in ALGORITMOS_CMP:
            self.progreso.emit(f"Ejecutando {NOMBRES_DISPLAY[key]}...")
            try:
                t0=time.time(); c,k=fns[key](); e=round(time.time()-t0,3)
                res.append((NOMBRES_DISPLAY[key],c,k,e))
            except: res.append((NOMBRES_DISPLAY[key],[],float("inf"),0.0))
        self.terminado.emit(res)

# ── Ventana principal ─────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rutas entre Provincias del Perú — IA")
        self.setMinimumSize(1100,700); self.resize(1400,900)
        self.setStyleSheet(ESTILOS)
        self._worker=None; self._worker_cmp=None
        self._provincias_map = {p["id"]-1: p for p in PROVINCIAS}

        central=QWidget(); self.setCentralWidget(central)
        lp=QHBoxLayout(central); lp.setContentsMargins(0,0,0,0); lp.setSpacing(0)
        splitter=QSplitter(Qt.Horizontal); lp.addWidget(splitter)

        # ── Panel izquierdo ──
        panel=QFrame(); panel.setObjectName("panel"); panel.setFixedWidth(330)
        pl=QVBoxLayout(panel); pl.setContentsMargins(14,14,14,14); pl.setSpacing(8)

        t=QLabel("🗺  Rutas del Perú — IA"); t.setObjectName("titulo"); pl.addWidget(t)

        pl.addWidget(self._lbl("Provincia Origen"))
        self.combo_origen=QComboBox(); self.combo_origen.setEditable(True)
        self._fill(self.combo_origen); pl.addWidget(self.combo_origen)

        pl.addWidget(self._lbl("Provincia Destino"))
        self.combo_destino=QComboBox(); self.combo_destino.setEditable(True)
        self._fill(self.combo_destino); self.combo_destino.setCurrentIndex(162)
        pl.addWidget(self.combo_destino)

        pl.addWidget(self._lbl("Algoritmo"))
        self.combo_alg=QComboBox()
        for n in ALGORITMOS: self.combo_alg.addItem(n)
        pl.addWidget(self.combo_alg)

        self.btn_exec=QPushButton("▶  Usar Algoritmo")
        self.btn_exec.clicked.connect(self.ejecutar); pl.addWidget(self.btn_exec)

        self.btn_mejor=QPushButton("🏆  Mejor Algoritmo")
        self.btn_mejor.setObjectName("btn_mejor")
        self.btn_mejor.clicked.connect(self.comparar); pl.addWidget(self.btn_mejor)

        self.progress=QProgressBar(); self.progress.setRange(0,0)
        self.progress.setVisible(False); pl.addWidget(self.progress)

        btn_limpiar=QPushButton("✕  Limpiar Mapa")
        btn_limpiar.setObjectName("btn_limpiar")
        btn_limpiar.clicked.connect(self.limpiar); pl.addWidget(btn_limpiar)

        sep=QFrame(); sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color:#37474f;"); pl.addWidget(sep)

        pl.addWidget(self._lbl("Resultado"))
        self.lbl_res=QLabel("—"); self.lbl_res.setWordWrap(True)
        self.lbl_res.setStyleSheet("color:#4fc3f7;font-size:12px;padding:4px;")
        pl.addWidget(self.lbl_res)

        pl.addWidget(self._lbl("Recorrido / Comparación"))
        self.lista=QListWidget()
        self.lista.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        pl.addWidget(self.lista)

        splitter.addWidget(panel)

        # ── Mapa ──
        self.web=QWebEngineView()
        self.channel=QWebChannel()
        self.bridge=Bridge()
        self.channel.registerObject("bridge",self.bridge)
        self.web.page().setWebChannel(self.channel)
        html=os.path.join(os.path.dirname(__file__),"..","map","mapa.html")
        self.web.setUrl(QUrl.fromLocalFile(os.path.abspath(html)))
        splitter.addWidget(self.web)
        splitter.setStretchFactor(0,0); splitter.setStretchFactor(1,1)

        self.status=QStatusBar(); self.setStatusBar(self.status)
        self.status.showMessage(f"✅  {len(PROVINCIAS)} provincias | radio 150km | mín3/máx10 vecinos")
        self.web.loadFinished.connect(self._mapa_listo)

    # ── helpers ──
    def _lbl(self,t):
        l=QLabel(t); l.setObjectName("sub"); return l
    def _fill(self,combo):
        combo.clear()
        for p in PROVINCIAS:
            combo.addItem(f"{p['provincia']} ({p['departamento']})", userData=p["id"]-1)
    def _bloquear(self,b):
        self.btn_exec.setEnabled(not b); self.btn_mejor.setEnabled(not b)
        self.progress.setVisible(b)
    def _validar(self):
        i=self.combo_origen.currentData(); f=self.combo_destino.currentData()
        if i is None or f is None:
            QMessageBox.warning(self,"Error","Selecciona origen y destino."); return None,None
        if i==f:
            QMessageBox.warning(self,"Error","Origen y destino deben ser distintos."); return None,None
        return i,f
    def _js(self,code):
        self.web.page().runJavaScript(code)

    def _mapa_listo(self,ok):
        if not ok: return
        self._js(f"dibujarProvincias({json.dumps(PROVINCIAS,ensure_ascii=False)});")
        self.status.showMessage(f"✅  Mapa listo — {len(PROVINCIAS)} provincias")

    # ── Ejecutar un algoritmo ──
    def ejecutar(self):
        i,f=self._validar()
        if i is None: return
        alg=ALGORITMOS[self.combo_alg.currentText()]
        self._bloquear(True); self.lista.clear()
        self.lbl_res.setText("Calculando...")
        self.lbl_res.setStyleSheet("color:#4fc3f7;font-size:12px;padding:4px;")
        self.status.showMessage(f"⏳  {self.combo_alg.currentText()}...")
        self._worker=WorkerAlgoritmo(alg,i,f)
        self._worker.terminado.connect(self._on_resultado)
        self._worker.error.connect(self._on_error)
        self._worker.start()

    def _on_resultado(self,camino,costo,elapsed):
        self._bloquear(False)
        if not camino:
            self.lbl_res.setText("❌ Sin ruta.")
            self.status.showMessage("Sin resultado"); return
        alg=self.combo_alg.currentText()
        self.lbl_res.setText(
            f"✅  {len(camino)} provincias\n📏  {costo:,.1f} km\n⏱  {elapsed:.3f}s\n🔧  {alg}")
        self.lista.clear()
        for idx,nid in enumerate(camino):
            p=PROVINCIAS[nid]
            pre="🟢" if idx==0 else ("🔴" if idx==len(camino)-1 else f"{idx}.")
            self.lista.addItem(f"{pre}  {p['provincia']} ({p['departamento']})")
        pm_json=json.dumps(self._provincias_map,ensure_ascii=False)
        self._js(f"dibujarRuta({json.dumps(camino)},{pm_json});")
        self.status.showMessage(f"✅  {len(camino)} pasos | {costo:,.1f} km | {elapsed:.3f}s")

    def _on_error(self,msg):
        self._bloquear(False)
        QMessageBox.critical(self,"Error",msg)
        self.status.showMessage("❌ Error")

    # ── Comparar algoritmos ──
    def comparar(self):
        i,f=self._validar()
        if i is None: return
        self._bloquear(True); self.lista.clear()
        self.lbl_res.setText("Comparando...")
        self.lbl_res.setStyleSheet("color:#4fc3f7;font-size:12px;padding:4px;")
        self.status.showMessage("⏳  Ejecutando 6 algoritmos...")
        self._worker_cmp=WorkerComparar(i,f)
        self._worker_cmp.progreso.connect(lambda m:self.status.showMessage(f"⏳  {m}"))
        self._worker_cmp.terminado.connect(self._on_comparacion)
        self._worker_cmp.start()

    def _on_comparacion(self,resultados):
        self._bloquear(False)
        validos  =[(n,c,k,t) for n,c,k,t in resultados if c and k<float("inf")]
        sin_ruta =[(n,c,k,t) for n,c,k,t in resultados if not c or k==float("inf")]
        if not validos:
            self.lbl_res.setText("❌ Ningún algoritmo encontró ruta.")
            self.status.showMessage("Sin resultados"); return

        validos.sort(key=lambda x:x[2])
        mn,mc,mk,mt=validos[0]

        # Lista resumen
        medallas=["🥇","🥈","🥉"]
        self.lista.clear()
        self.lista.addItem("══ COMPARACIÓN DE ALGORITMOS ══")
        self.lista.addItem("  Algoritmo   Distancia  Pasos  Tiempo")
        self.lista.addItem("─"*44)
        for i,(nombre,camino,costo,elapsed) in enumerate(validos):
            m=medallas[i] if i<3 else f"  {i+1}."
            self.lista.addItem(
                f"{m} {nombre:9s}  {costo:>8,.0f}km  {len(camino):>4}  {elapsed:.3f}s")
        if sin_ruta:
            self.lista.addItem("─"*44)
            for nombre,_,_,_ in sin_ruta:
                self.lista.addItem(f"  ✗  {nombre} — Sin ruta")

        self.lbl_res.setText(
            f"🏆 MEJOR: {mn}\n📏 {mk:,.0f} km\n🔢 {len(mc)} pasos\n⏱  {mt:.3f}s")
        self.lbl_res.setStyleSheet(
            "color:#ffd600;font-size:12px;font-weight:bold;padding:4px;")

        # Payload animación — solo rutas válidas
        payload=[]
        for i,(nombre,camino,costo,elapsed) in enumerate(validos):
            payload.append({
                "nombre":nombre,"ruta_ids":camino,"costo":costo,
                "pasos":len(camino),"tiempo":f"{elapsed:.3f}",
                "es_ganador":(i==0),
                "provincias_map":self._provincias_map
            })

        self._js(f"animarRutas({json.dumps(payload,ensure_ascii=False)});")
        origen  = PROVINCIAS[self.combo_origen.currentData()]["provincia"]
        destino = PROVINCIAS[self.combo_destino.currentData()]["provincia"]
        self.status.showMessage(
            f"🏆 {mn} ({mk:,.0f} km) — {origen} → {destino}")

    def limpiar(self):
        self.lista.clear()
        self.lbl_res.setText("—")
        self.lbl_res.setStyleSheet("color:#4fc3f7;font-size:12px;padding:4px;")
        self._js("limpiarRuta();")
        self.status.showMessage("Mapa limpiado")
