from PySide6.QtCore import QObject, Slot, QUrl, Signal, Property, QTimer
from PySide6.QtQml import QmlElement, QmlSingleton
from Model.ucs import costo_uniforme
from Model.dfs import DFS
from Model.search_status import SearchStatus
from Model.search_algorithm import SearchAlgorithm

QML_IMPORT_NAME = "QmlModules.ViewModel"
QML_IMPORT_MAJOR_VERSION = 1

UNVISITED_NODE = 0
VISITED_NODE = 1
CURRENT_NODE = 2
PATH = 3

@QmlElement
@QmlSingleton
class MazeViewModel(QObject):
    mazeChanged = Signal()
    logChanged = Signal()
    statsChanged = Signal()
    flowPanelVisibleChanged = Signal()
    errorOccurred = Signal(str)
    pathChanged = Signal()
    runningChanged = Signal()

    def __init__(self):
        super().__init__()
        self._maze = []
        self._maze_original = []
        self._maze_matrix = []
        self._path_ucs = []
        self._current_step = 0
        self._flow_panel_visible = True

        self._log_text = "Esperando la carga de un laberinto..."
        self._stats = {"costo": "-", "visitados": "-", "frontera": "-", "longitud": "-"}
        self._status_message = "Inactivo"

        self._timer = QTimer(self)
        self._timer.setInterval(70)
        self._timer.timeout.connect(self._animation_tick)

        # DFS / Path properties
        self._path = []
        self._start: tuple[int, int] | None = None
        self._goals: list[tuple[int, int]] = []
        self._running = False
        self._algorithm: DFS | None = None

    # --- Propiedades QML ---
    @Property("QVariantList", notify=mazeChanged)
    def maze(self):
        return self._maze

    @Property("QVariantList", notify=pathChanged)
    def path(self):
        return self._path

    @Property(bool, notify=runningChanged)
    def running(self):
        return self._running

    @Property(str, notify=logChanged)
    def logText(self):
        return self._log_text

    @Property(bool, notify=flowPanelVisibleChanged)
    def flowPanelVisible(self):
        return self._flow_panel_visible

    @Property(str, notify=statsChanged)
    def statsCosto(self):
        return self._stats["costo"]

    @Property(str, notify=statsChanged)
    def statsVisitados(self):
        return self._stats["visitados"]

    @Property(str, notify=statsChanged)
    def statsFrontera(self):
        return self._stats["frontera"]

    @Property(str, notify=statsChanged)
    def statsLongitud(self):
        return self._stats["longitud"]

    @Property(str, notify=statsChanged)
    def statusMessage(self):
        return self._status_message

    @Slot()
    def toggle_flow_panel(self):
        self._flow_panel_visible = not self._flow_panel_visible
        self.flowPanelVisibleChanged.emit()

    # --- Métodos de Control ---
    def _stop_animation(self):
        if self._timer.isActive():
            self._timer.stop()
        self._path_ucs.clear()
        self._current_step = 0

    @Slot(QUrl)
    def load_maze(self, file_url):
        self._stop_animation()
        file_path = file_url.toLocalFile()

        with open(file_path, "r", encoding="utf-8") as file:
            maze = file.read().splitlines()

        if len(maze) > 15 or any(len(r) > 25 for r in maze):
            self.errorOccurred.emit("Error: El laberinto excede el tamaño máximo (15x25).")
            return

        start: tuple[int, int] | None = None
        goals: list[tuple[int, int]] = []
        for row_index, row in enumerate(maze):
            for column_index, cell in enumerate(row):
                if cell == "S":
                    start = (row_index, column_index)
                elif cell == "G":
                    goals.append((row_index, column_index))

        self._maze_original = list(maze)
        self._maze = list(maze)
        self._start = start
        self._goals = goals
        self._path = [[UNVISITED_NODE for _ in row] for row in maze]

        self.mazeChanged.emit()
        self.pathChanged.emit()

        filename = file_path.replace("\\", "/").split("/")[-1]
        self._stats = {"costo": "-", "visitados": "-", "frontera": "-", "longitud": "-"}
        self._status_message = "Laberinto cargado"
        self._log_text = (
            f"[SISTEMA] Laberinto cargado exitosamente:\n"
            f"  * Archivo: {filename}\n"
            f"  * Dimensiones: {len(maze)} filas x {len(maze[0]) if maze else 0} columnas\n"
            f"  * Selecciona un algoritmo para iniciar la búsqueda."
        )
        self.logChanged.emit()
        self.statsChanged.emit()

    @Slot(str)
    def start_search(self, algorithm_name):
        if not self._maze:
            self.errorOccurred.emit("Error: Se debe cargar un laberinto primero")
            return

        if algorithm_name == 'UCS':
            self.solve_ucs()
            return

        if self._start is None or not self._goals:
            self.errorOccurred.emit("Error: No hay entrada o metas en el laberinto")
            return

        if algorithm_name == 'DFS':
            self._algorithm = DFS(
                self._maze,
                self._start,
                self._goals
            )
        else:
            return

        self._path = [[UNVISITED_NODE for _ in row] for row in self._maze]
        self._running = True
        self.pathChanged.emit()
        self.runningChanged.emit()

    @Slot()
    def solve_ucs(self):
        if not self._maze_original:
            self.errorOccurred.emit("Error: Primero debes cargar un laberinto.")
            return

        self._stop_animation()
        ruta, costo, stats, logs = costo_uniforme(self._maze_original, recopilar_trazas=True)

        if not ruta:
            self._status_message = "Sin solución"
            self._log_text = "\n".join(logs)
            self.logChanged.emit()
            self.statsChanged.emit()
            self.errorOccurred.emit("No se encontró ningún camino hacia la meta.")
            return

        self._stats = {
            "costo": str(costo),
            "visitados": str(stats["nodos_explorados"]),
            "frontera": str(stats["max_frontera"]),
            "longitud": str(stats["longitud_ruta"])
        }
        self._status_message = "Ruta óptima calculada"
        self._log_text = "\n".join(logs)
        self.logChanged.emit()
        self.statsChanged.emit()

        self._maze_matrix = [list(fila) for fila in self._maze_original]
        self._path_ucs = ruta
        self._current_step = 0
        self._timer.start()

    def _animation_tick(self):
        if not self._path_ucs or self._current_step >= len(self._path_ucs):
            self._timer.stop()
            return

        if self._current_step > 0:
            prev_f, prev_c = self._path_ucs[self._current_step - 1]
            if self._maze_matrix[prev_f][prev_c] not in ('S', 'G'):
                self._maze_matrix[prev_f][prev_c] = '*'

        curr_f, curr_c = self._path_ucs[self._current_step]
        if self._maze_matrix[curr_f][curr_c] not in ('S', 'G'):
            self._maze_matrix[curr_f][curr_c] = '@'

        if self._current_step == len(self._path_ucs) - 1:
            if self._current_step > 0:
                prev_f, prev_c = self._path_ucs[self._current_step - 1]
                if self._maze_matrix[prev_f][prev_c] not in ('S', 'G'):
                    self._maze_matrix[prev_f][prev_c] = '*'
            self._timer.stop()

        self._maze = ["".join(fila) for fila in self._maze_matrix]
        self.mazeChanged.emit()
        self._current_step += 1

    @Slot()
    def step_search(self):
        if self._algorithm is None:
            return

        if self._algorithm.status != SearchStatus.SEARCHING:
            self._running = False
            self.runningChanged.emit()
            return

        self._algorithm.step()
        self.update_path()

        if self._algorithm.status != SearchStatus.SEARCHING:
            self._running = False
            self.runningChanged.emit()

    def update_path(self):
        if self._algorithm is None:
            return

        for node in self._algorithm.visited_nodes:
            self._path[node.row][node.column] = VISITED_NODE

        if self._algorithm.stack:
            current_node, _ = self._algorithm.stack[-1]
            self._path[current_node.row][current_node.column] = CURRENT_NODE

        if self._algorithm.status == SearchStatus.FOUND:
            for node, _ in self._algorithm.stack:
                self._path[node.row][node.column] = PATH

        self.pathChanged.emit()
