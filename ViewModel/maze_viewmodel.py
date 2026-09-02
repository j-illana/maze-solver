from PySide6.QtCore import QObject, Slot, QUrl, Signal, Property, QTimer
from PySide6.QtQml import QmlElement, QmlSingleton
from Model.ucs import UCS
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
        self._flow_panel_visible = True

        self._log_text = "Esperando la carga de un laberinto..."
        self._stats = {"costo": "-", "visitados": "-", "frontera": "-", "longitud": "-"}
        self._status_message = "Inactivo"

        # DFS / UCS properties
        self._path = []
        self._start: tuple[int, int] | None = None
        self._goals: list[tuple[int, int]] = []
        self._running = False
        self._algorithm: SearchAlgorithm | None = None

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

    @Slot(QUrl)
    def load_maze(self, file_url):
        self._running = False
        self._algorithm = None
        self.runningChanged.emit()

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

        if self._start is None or not self._goals:
            self.errorOccurred.emit("Error: No hay entrada o metas en el laberinto")
            return

        if algorithm_name == 'UCS':
            self._algorithm = UCS(self._maze, self._start, self._goals)
            self._status_message = "Buscando (UCS)"
        elif algorithm_name == 'DFS':
            self._algorithm = DFS(self._maze, self._start, self._goals)
            self._status_message = "Buscando (DFS)"
        else:
            return

        self._path = [[UNVISITED_NODE for _ in row] for row in self._maze]
        self._running = True
        self.pathChanged.emit()
        self.runningChanged.emit()
        self.statsChanged.emit()

        if hasattr(self._algorithm, 'logs'):
            self._log_text = "\n".join(self._algorithm.logs)
            self.logChanged.emit()

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

        # Actualizar métricas y consola si es UCS
        if isinstance(self._algorithm, UCS):
            self._stats = {
                "costo": str(self._algorithm.costo_total) if self._algorithm.status == SearchStatus.FOUND else str(self._algorithm.costos_g.get(self._algorithm.stack[-1][0].position, 0) if self._algorithm.stack else 0),
                "visitados": str(self._algorithm.nodos_explorados),
                "frontera": str(len(self._algorithm.pq)),
                "longitud": str(len(self._algorithm.stack)) if self._algorithm.stack else "0"
            }
            self._log_text = "\n".join(self._algorithm.logs)
            self.logChanged.emit()
            self.statsChanged.emit()

        if self._algorithm.status == SearchStatus.FOUND:
            self._status_message = "¡Meta Alcanzada!"
            self._running = False
            self.runningChanged.emit()
            self.statsChanged.emit()
        elif self._algorithm.status == SearchStatus.NOT_FOUND:
            self._status_message = "Sin solución"
            self._running = False
            self.runningChanged.emit()
            self.statsChanged.emit()

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

