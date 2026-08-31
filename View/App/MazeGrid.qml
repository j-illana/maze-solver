pragma ComponentBehavior: Bound

import QtQuick
import QmlModules.ViewModel

Grid {
    id: root

    rows: 15
    columns: 25

    readonly property var maze: MazeViewModel.maze

    Repeater {
        model: root.rows * root.columns 

        MazeCell {
            required property int index

            property int row: Math.floor(index / root.columns)
            property int column: index % root.columns

            property string cellEmptyColor:
                (row + column) % 2 === 0
                    ? "1"
                    : "2"

            property bool hasMazeData:
                (row < root.maze.length) && (column < root.maze[row].length)

            width: root.width / root.columns
            height: root.height / root.rows

            cellType: hasMazeData
                ? root.maze[row][column]
                : cellEmptyColor
        }
    }
}