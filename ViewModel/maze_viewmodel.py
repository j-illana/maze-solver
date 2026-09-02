from PySide6.QtCore import QObject, Slot, QUrl, Signal, Property
from PySide6.QtQml import QmlElement, QmlSingleton
from Model.search_status import SearchStatus
from Model.search_algorithm import SearchAlgorithm
from Model.dfs import DFS
from Model.bfs import BFS
from graph_visualizer import show_search_tree
import time

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
    dfsPathChanged = Signal()
    bfsPathChanged = Signal()
    ucsPathChanged = Signal()
    runningChanged = Signal()
    errorOccurred = Signal(str)

    def __init__(self):
        super().__init__()
        self._maze = []
        self._path = []
        self._dfsPath = []
        self._bfsPath = []
        self._ucsPath = []
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

    @Property("QVariantList", notify=dfsPathChanged)
    def dfsPath(self):
        return self._dfsPath

    @Property("QVariantList", notify=bfsPathChanged)
    def bfsPath(self):
        return self._bfsPath

    @Property("QVariantList", notify=ucsPathChanged)
    def ucsPath(self):
        return self._ucsPath

    @Property(bool, notify=runningChanged)
    def running(self):
        return self._running


    @Slot()
    def reset_path(self):
        self._path = [[UNVISITED_NODE for _ in row] for row in self._maze]

        self.pathChanged.emit()

    @Slot()
    def reset_comparison_paths(self):
        self._dfsPath = [[UNVISITED_NODE for _ in row] for row in self._maze]
        self._bfsPath = [[UNVISITED_NODE for _ in row] for row in self._maze]
        self._ucsPath = [[UNVISITED_NODE for _ in row] for row in self._maze]
        self.dfsPathChanged.emit()
        self.bfsPathChanged.emit()
        self.ucsPathChanged.emit()


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

        self.reset_path()
        self.reset_comparison_paths()

        self.mazeChanged.emit()


    @Slot(str)
    def start_search(self, algorithm_name):
        if not self._maze:
            self.errorOccurred.emit("Error: Se debe cargar un laberinto primero")
            return

        if self._start is None or not self._goals:
            self.errorOccurred.emit("Error: No hay entrada o metas en el laberinto")
            return

        if algorithm_name == "DFS":
            self._algorithm = DFS(
                self._maze,
                self._start,
                self._goals
            )

        elif algorithm_name == "BFS":
            self._algorithm = BFS(
                self._maze,
                self._start,
                self._goals
            )

        else:
            return

        self.reset_path()
        self._running = True
        self.runningChanged.emit()


    @Slot()
    def step_search(self):
        if self._algorithm is None:
            return

        if self._algorithm.status != SearchStatus.SEARCHING:
            self._running = False
            self.runningChanged.emit()
            self.show_results()
            return

        self._algorithm.step()
        self.update_path()

        if self._algorithm.status != SearchStatus.SEARCHING:
            self._running = False
            self.runningChanged.emit()
            self.show_results()
            print("-----------------------------------------")


    @Slot(str)
    def solve_algorithm(self, algorithm_name):
        if not self._maze:
            self.errorOccurred.emit("Error: Se debe cargar un laberinto primero")
            return

        if self._start is None or not self._goals:
            self.errorOccurred.emit("Error: No hay entrada o metas en el laberinto")
            return

        if algorithm_name == "DFS":
            self._algorithm = DFS(
                self._maze,
                self._start,
                self._goals
            )

        elif algorithm_name == "BFS":
            self._algorithm = BFS(
                self._maze,
                self._start,
                self._goals
            )

        else:
            return

        self.reset_path()

        start_time = time.perf_counter()

        while(self._algorithm.status == SearchStatus.SEARCHING):
            self._algorithm.step()

        end_time = time.perf_counter()

        elapsed_time = end_time - start_time

        self.update_path()
        self.show_results()
        print(f"Tiempo de ejecución: {elapsed_time} segundos")
        print("-----------------------------------------")


    @Slot()
    def show_search_tree(self):
        if self._algorithm is None:
            self.errorOccurred.emit(
                "Error: Primero se debe ejecutar un algoritmo"
            )
            return

        show_search_tree(self._algorithm)


    def update_path(self):
        if self._algorithm is None:
            return

        visited_nodes = self._algorithm.visited_nodes
        current_node = self._algorithm.get_current_node()
        solution_path = self._algorithm.get_solution_path()

        for node in visited_nodes:
            self._path[node.row][node.column] = VISITED_NODE

        if current_node is not None:
            self._path[current_node.row][current_node.column] = CURRENT_NODE

        if self._algorithm.status == SearchStatus.FOUND:
            for node in solution_path:
                self._path[node.row][node.column] = PATH

            if isinstance(self._algorithm, DFS):
                self._dfsPath = [row.copy() for row in self._path]
                self.dfsPathChanged.emit()

            elif isinstance(self._algorithm, BFS):
                self._bfsPath = [row.copy() for row in self._path]
                self.bfsPathChanged.emit()

        self.pathChanged.emit()


    def show_results(self):
        if self._algorithm is None:
            return

        algorithm_name = type(self._algorithm).__name__
        solution_path = self._algorithm.get_solution_path()
        steps_number = max(0, len(solution_path) - 1)
        visited_order = self._algorithm.visited_order
        visited_nodes = [node.position for node in visited_order]
        cost = self._algorithm.get_path_cost()

        print("\n-----------------------------------------")
        print("Resultados")
        print("-----------------------------------------")
        print(f"Algoritmo elegido: {algorithm_name}")
        print(f"Nodo de salida: {self._start}")
        print(f"Nodos de meta: {self._goals}")
        print(f"Longitud del camino: {steps_number}")
        print(f"Costo total del camino: {cost}")
        print(f"Cantidad de nodos visitados: {len(visited_nodes)}")
        print(f"Nodos visitados: {visited_nodes}")