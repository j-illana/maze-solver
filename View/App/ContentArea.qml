import QtQuick
import QtQuick.Layouts
import QmlModules.ViewModel

ColumnLayout {
    id: root
    spacing: 0
    property int currentPage: 0

    RowLayout {
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.preferredHeight: 3

        spacing: 0

        MazeContainer {
            currentPage: root.currentPage

            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredWidth: 3
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredWidth: 1

            ConfigurationArea {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.preferredWidth: 1
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                height: parent.height * 0.5

                currentPage: root.currentPage
            }
        }
    }

    StackLayout {
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.preferredHeight: 1

        currentIndex: root.currentPage

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true

            ColumnLayout {
                anchors.fill: parent
                spacing: 0
                anchors.leftMargin: 20
                anchors.rightMargin: 20
                anchors.topMargin: 10
                anchors.bottomMargin: 10

                Text {
                    text: "Algoritmo elegido: " + MazeViewModel.algorithmName

                    Layout.fillHeight: true
                    Layout.preferredHeight: 1
                    verticalAlignment: Text.AlignVCenter

                    color: "white"
                    font.pixelSize: 20
                    font.bold: true
                }

                Text {
                    text: "Longitud del camino: " + MazeViewModel.stepsNumber

                    Layout.fillHeight: true
                    Layout.preferredHeight: 1
                    verticalAlignment: Text.AlignVCenter

                    color: "white"
                    font.pixelSize: 20
                    font.bold: true
                }

                Text {
                    text: "Costo total del camino: " + MazeViewModel.pathCost

                    Layout.fillHeight: true
                    Layout.preferredHeight: 1
                    verticalAlignment: Text.AlignVCenter

                    color: "white"
                    font.pixelSize: 20
                    font.bold: true
                }

                Text {
                    text: ("Cantidad de nodos visitados: " + 
                        MazeViewModel.visitedNodesCount)

                    Layout.fillHeight: true
                    Layout.preferredHeight: 1
                    verticalAlignment: Text.AlignVCenter

                    color: "white"
                    font.pixelSize: 20
                    font.bold: true
                }
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true

            ColumnLayout {
                anchors.fill: parent
                spacing: 0
                anchors.leftMargin: 20
                anchors.rightMargin: 20
                anchors.topMargin: 10
                anchors.bottomMargin: 10

                Text {
                    text: "Algoritmo elegido: " + MazeViewModel.algorithmName

                    Layout.fillHeight: true
                    Layout.preferredHeight: 1
                    verticalAlignment: Text.AlignVCenter

                    color: "white"
                    font.pixelSize: 20
                    font.bold: true
                }

                Text {
                    text: "Longitud del camino: " + MazeViewModel.stepsNumber

                    Layout.fillHeight: true
                    Layout.preferredHeight: 1
                    verticalAlignment: Text.AlignVCenter

                    color: "white"
                    font.pixelSize: 20
                    font.bold: true
                }

                Text {
                    text: "Costo total del camino: " + MazeViewModel.pathCost

                    Layout.fillHeight: true
                    Layout.preferredHeight: 1
                    verticalAlignment: Text.AlignVCenter

                    color: "white"
                    font.pixelSize: 20
                    font.bold: true
                }

                Text {
                    text: "Cantidad de nodos visitados: " + MazeViewModel.visitedNodesCount

                    Layout.fillHeight: true
                    Layout.preferredHeight: 1
                    verticalAlignment: Text.AlignVCenter

                    color: "white"
                    font.pixelSize: 20
                    font.bold: true
                }

                Text {
                    text: ("Tiempo: " + 
                        MazeViewModel.elapsedTime.toFixed(5) + " segundos")

                    Layout.fillHeight: true
                    Layout.preferredHeight: 1
                    verticalAlignment: Text.AlignVCenter

                    color: "white"
                    font.pixelSize: 20
                    font.bold: true
                }
            }
        }
    }
}