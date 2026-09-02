import QtQuick
import QtQuick.Layouts
import QmlModules.ViewModel

Item {
    Timer {
        id: searchTimer

        interval: 200
        repeat: true
        running: MazeViewModel.running

        onTriggered: {
            MazeViewModel.step_search()
        }
    }

    ColumnLayout {
        spacing: 0
        anchors.fill: parent
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        anchors.topMargin: 0
        anchors.bottomMargin: 0

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredHeight: 1

            AlgorithmSelector {
                id: algorithmSelector
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredHeight: 1

            RowLayout {
                anchors.fill: parent
                spacing: 10

                SimulationButton {
                    text: "Iniciar"
                    Layout.fillWidth: true
                    Layout.preferredWidth: 1

                    onClicked: {
                        MazeViewModel.start_search(
                            algorithmSelector.currentText
                        )
                    }
                }

                SimulationButton {
                    text: "Reiniciar"
                    Layout.fillWidth: true
                    Layout.preferredWidth: 1
                }
            }
        }
    }
}