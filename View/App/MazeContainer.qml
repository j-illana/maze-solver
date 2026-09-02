import QtQuick
import QtQuick.Layouts
import View.Style
import QmlModules.ViewModel

Rectangle {
    id: root
    color: Colors.background

    property real mazeScale: 0.9
    property int currentPage: 0

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

        StackLayout {
            anchors.fill: parent
            currentIndex: root.currentPage
            
            PathGrid {
                path: MazeViewModel.path
                rows: gridContainer.rows
                columns: gridContainer.columns
                currentPage: root.currentPage
                solutionPathCell: Colors.solutionPathCell1
            }

            Item {
                PathGrid {
                    anchors.fill: parent
                    
                    path: MazeViewModel.dfsPath
                    rows: gridContainer.rows
                    columns: gridContainer.columns
                    currentPage: root.currentPage
                    solutionPathCell: Colors.solutionPathCell1
                }

                PathGrid {
                    anchors.fill: parent
                    
                    path: MazeViewModel.bfsPath
                    rows: gridContainer.rows
                    columns: gridContainer.columns
                    currentPage: root.currentPage
                    solutionPathCell: Colors.solutionPathCell2
                }

                PathGrid {
                    anchors.fill: parent
                    
                    path: MazeViewModel.ucsPath
                    rows: gridContainer.rows
                    columns: gridContainer.columns
                    currentPage: root.currentPage
                    solutionPathCell: Colors.solutionPathCell3
                }
            }
        }

    }
}