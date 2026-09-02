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

    Item {
        id: gridContainer
        anchors.centerIn: parent
        visible: MazeViewModel.maze.length > 0

        readonly property int mazeRows: MazeViewModel.maze.length
        readonly property int mazeCols: (MazeViewModel.maze.length > 0 && MazeViewModel.maze[0].length > 0) ? MazeViewModel.maze[0].length : 1

        readonly property real cellSize: (mazeCols > 0 && mazeRows > 0)
            ? Math.min(
                parent.width * root.mazeScale / mazeCols,
                parent.height * root.mazeScale / mazeRows
            )
            : 0

        width: mazeCols * cellSize
        height: mazeRows * cellSize

        MazeGrid {
            anchors.fill: parent
        }

        PathGrid {
            anchors.fill: parent
            rows: gridContainer.mazeRows
            columns: gridContainer.mazeCols
        }
    }
}