pragma ComponentBehavior: Bound

import QtQuick
import QmlModules.ViewModel

Grid {
    id: root
    property var path: []

    property int currentPage
    property color solutionPathCell

    Repeater {
        model: root.rows * root.columns

        PathCell {
            required property int index
            
            currentPage: root.currentPage
            solutionPathCell: root.solutionPathCell

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