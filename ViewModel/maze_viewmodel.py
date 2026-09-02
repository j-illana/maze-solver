from PySide6.QtCore import QObject, Slot, QUrl, Signal, Property
from PySide6.QtQml import QmlElement, QmlSingleton
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
    pathChanged = Signal()
    runningChanged = Signal()
    errorOccurred = Signal(str)

    def __init__(self):
        super().__init__()
        self._maze = []
        self._path = []
        self._start: tuple[int, int] | None = None
        self._goals: list[tuple[int, int]] = []
        self._running = False
        self._algorithm: SearchAlgorithm | None = None

    @Property("QVariantList", notify=mazeChanged)
    def maze(self):
        return self._maze

    @Property("QVariantList", notify=pathChanged)
    def path(self):
        return self._path

    @Property(bool, notify=runningChanged)
    def running(self):
        return self._running


    @Slot(QUrl)
    def load_maze(self, file_url):
        start: tuple[int, int] | None = None
        goals: list[tuple[int, int]] = []
        file_path = file_url.toLocalFile()

        with open(file_path, "r") as file:
            maze = file.read().splitlines()

        if len(maze) > 15:
            self.errorOccurred.emit(
                "Error: El laberinto no puede tener más de 15 filas"
            )
            return

        for row_index, row in enumerate(maze):
            if len(row) > 25:
                self.errorOccurred.emit(
                    "Error: El laberinto no puede tener más de 25 columnas"
                )
                return

            for column_index, cell in enumerate(row):
                if cell == "S":
                    start = (row_index, column_index)

                elif cell == "G":
                    goals.append((row_index, column_index))

        if start is None:
            self.errorOccurred.emit("Error: El laberinto no contiene entrada")
            return

        if not goals:
            self.errorOccurred.emit("Error: El laberinto no contiene metas")
            return

        self._maze = maze
        self._start = start
        self._goals = goals

        self._path = [[UNVISITED_NODE for _ in row] for row in maze]

        self.mazeChanged.emit()
        self.pathChanged.emit()


    @Slot(str)
    def start_search(self, algorithm_name):
        if not self._maze:
            self.errorOccurred.emit("Error: Se debe cargar un laberinto primero")
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

        print(f"Algoritmo seleccionado: {algorithm_name}")
        print(f"Salida: {self._start}")
        print(f"Metas: {self._goals}")

        self._path = [[UNVISITED_NODE for _ in row] for row in self._maze]
        self._running = True
        self.pathChanged.emit()
        self.runningChanged.emit()

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