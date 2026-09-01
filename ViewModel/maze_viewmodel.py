from PySide6.QtCore import QObject, Slot, QUrl, Signal, Property
from PySide6.QtQml import QmlElement, QmlSingleton
from Model.ucs import costo_uniforme

QML_IMPORT_NAME = "QmlModules.ViewModel"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
@QmlSingleton
class MazeViewModel(QObject):
    mazeChanged = Signal()
    errorOccurred = Signal(str)

    def __init__(self):
        super().__init__()
        self._maze = []
        self._maze_original = []

    @Property("QVariantList", notify=mazeChanged)
    def maze(self):
        return self._maze

    @Slot(QUrl)
    def load_maze(self, file_url):
        file_path = file_url.toLocalFile()

        with open(file_path, "r", encoding="utf-8") as file:
            maze = file.read().splitlines()

        if len(maze) > 15:
            self.errorOccurred.emit(
                "Error: El laberinto no puede tener más de 15 filas"
            )
            return

        for row in maze:
            if len(row) > 25:
                self.errorOccurred.emit(
                    "Error: El laberinto no puede tener más de 25 columnas"
                )
                return

        self._maze_original = list(maze)
        self._maze = list(maze)
        self.mazeChanged.emit()

    @Slot()
    def solve_ucs(self):
        if not self._maze_original:
            self.errorOccurred.emit("Error: Primero debes cargar un laberinto.")
            return

        ruta, costo = costo_uniforme(self._maze_original)

        if not ruta:
            self.errorOccurred.emit("No se encontró ningún camino hacia la meta.")
            return

        # Generar matriz con la ruta marcada (sin sobreescribir 'S' ni 'G')
        maze_matriz = [list(fila) for fila in self._maze_original]
        for f, c in ruta:
            if maze_matriz[f][c] not in ('S', 'G'):
                maze_matriz[f][c] = '*'

        self._maze = ["".join(fila) for fila in maze_matriz]
        self.mazeChanged.emit()