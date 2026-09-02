pragma ComponentBehavior: Bound

import QtQuick
import QmlModules.ViewModel

Grid {
    id: root

    readonly property var maze: MazeViewModel.maze

    columns: (maze.length > 0 && maze[0].length > 0) ? maze[0].length : 1

    Repeater {
        model: maze.length > 0 ? (maze.length * root.columns) : 0

        MazeCell {
            required property int index

            property int row: Math.floor(index / root.columns)
            property int column: index % root.columns

            width: root.width / root.columns
            height: root.height / (maze.length > 0 ? maze.length : 1)

            cellType: (row < root.maze.length && column < root.maze[row].length)
                ? root.maze[row][column]
                : "."
        }
    }
}
