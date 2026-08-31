import QtQuick
import View.Style

Rectangle {
    id: root
    color: Colors.background

    property real mazeScale: 0.9

    MazeGrid {
        anchors.centerIn: parent

        property real cellSize: Math.min(
            parent.width * root.mazeScale / columns,
            parent.height * root.mazeScale / rows
        )

        width: columns * cellSize
        height: rows * cellSize
    }
}