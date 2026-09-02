import QtQuick
import View.Style

Rectangle {
    id: root
    color: Colors.background

    property real mazeScale: 0.9

    Item {
        id: gridContainer

        property int rows: 15
        property int columns: 25

        property real cellSize: Math.min(
            parent.width * root.mazeScale / columns,
            parent.height * root.mazeScale / rows
        )

        anchors.centerIn: parent
        width: columns * cellSize
        height: rows * cellSize

        MazeGrid {
            anchors.fill: parent
            rows: gridContainer.rows
            columns: gridContainer.columns
        }

        PathGrid {
            anchors.fill: parent
            rows: gridContainer.rows
            columns: gridContainer.columns
        }
    }
}