from PySide6.QtCore import QObject, Slot, QUrl, Signal, Property
from PySide6.QtQml import QmlElement, QmlSingleton

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

    @Property("QVariantList", notify=mazeChanged)
    def maze(self):
        return self._maze

    @Slot(QUrl)
    def load_maze(self, file_url):
        file_path = file_url.toLocalFile()

        with open(file_path, "r") as file:
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

        self._maze = maze
        self.mazeChanged.emit()