import QtQuick
import View.Style
import QmlModules.ViewModel

Rectangle {
    id: root
    color: Colors.background

    property real mazeScale: 0.9

    Text {
        anchors.centerIn: parent
        text: "Carga un laberinto para comenzar"
        color: "#8399AF"
        font.pixelSize: 18
        font.family: "JetBrains Mono"
        visible: MazeViewModel.maze.length === 0
    }

    MazeGrid {
        id: grid
        anchors.centerIn: parent
        visible: MazeViewModel.maze.length > 0

        readonly property int mazeRows: MazeViewModel.maze.length
        readonly property real cellSize: (columns > 0 && mazeRows > 0)
            ? Math.min(
                parent.width * root.mazeScale / columns,
                parent.height * root.mazeScale / mazeRows
            )
            : 0

        width: columns * cellSize
        height: mazeRows * cellSize
    }
}