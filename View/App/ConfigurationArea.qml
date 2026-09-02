import QtQuick
import QtQuick.Layouts
import QmlModules.ViewModel

Item {
    id: root
    property int currentPage: 0

    Timer {
        id: searchTimer

        interval: 100
        repeat: true
        running: MazeViewModel.running

        onTriggered: {
            MazeViewModel.step_search()
        }
    }

    StackLayout {
        anchors.fill: parent
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        anchors.topMargin: 0
        anchors.bottomMargin: 0

        currentIndex: root.currentPage

        ColumnLayout {
            spacing: 0
            Layout.fillWidth: true
            Layout.fillHeight: true

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
                        text: "Ver árbol"
                        Layout.fillWidth: true
                        Layout.preferredWidth: 1

                        onClicked: {
                            MazeViewModel.show_search_tree()
                        }
                    }

                    SimulationButton {
                        text: "Reiniciar"
                        Layout.fillWidth: true
                        Layout.preferredWidth: 1

                        onClicked: {
                            MazeViewModel.reset_path()
                        }
                    }
                }
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 0

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.preferredHeight: 1

                AlgorithmSelector {
                    id: algorithmCheckbox
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
                            MazeViewModel.solve_algorithm(
                                algorithmCheckbox.currentText
                            )
                            MazeViewModel.show_search_tree()
                        }
                    }

                    SimulationButton {
                        text: "Reiniciar"
                        Layout.fillWidth: true
                        Layout.preferredWidth: 1

                        onClicked: {
                            MazeViewModel.reset_path()
                            MazeViewModel.reset_comparison_paths()
                        }
                    }
                }
            }
        }
    }

}