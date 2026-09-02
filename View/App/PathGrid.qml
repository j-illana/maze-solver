pragma ComponentBehavior: Bound

import QtQuick
import QmlModules.ViewModel

Grid {
    id: root
    readonly property var path: MazeViewModel.path

    Repeater {
        model: root.rows * root.columns

        PathCell {
            required property int index

            property int row: Math.floor(index / root.columns)
            property int column: index % root.columns

            property bool hasPathData: (
                row < root.path.length && 
                column < root.path[row].length
            )

            width: root.width / root.columns
            height: root.height / root.rows

            cellType: hasPathData ? root.path[row][column] : 0
        }
    }
}