import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QmlModules.ViewModel
import View.Style

Rectangle {
    id: root
    color: Colors.background

    // Componente reutilizable para tarjetas de métricas
    component MetricCard: Rectangle {
        property string title: ""
        property string value: ""
        property color valueColor: "#FFFFFF"

        Layout.fillWidth: true
        Layout.fillHeight: true
        radius: 6
        color: "#232D3B"

        ColumnLayout {
            anchors.centerIn: parent
            spacing: 2

            Text {
                text: title
                font.family: "JetBrains Mono"
                font.pixelSize: 10
                color: Colors.mazeCellEmpty2
                Layout.alignment: Qt.AlignHCenter
            }
            Text {
                text: value
                font.family: "JetBrains Mono"
                font.pixelSize: 14
                font.bold: true
                color: valueColor
                Layout.alignment: Qt.AlignHCenter
            }
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 14
        spacing: 12

        // ==========================================
        // 1. TARJETA DE MÉTRICAS Y ESTADO
        // ==========================================
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 120
            radius: 8
            color: "#2C3848"
            border.color: Colors.buttonHover
            border.width: 1

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 12
                spacing: 8

                RowLayout {
                    Layout.fillWidth: true

                    Text {
                        text: "MÉTRICAS DEL ALGORITMO (UCS)"
                        font.family: "JetBrains Mono"
                        font.pixelSize: 13
                        font.bold: true
                        color: Colors.mazePath
                        Layout.fillWidth: true
                    }

                    Rectangle {
                        radius: 4
                        color: Colors.buttonHover
                        implicitWidth: statusText.implicitWidth + 12
                        implicitHeight: statusText.implicitHeight + 6

                        Text {
                            id: statusText
                            anchors.centerIn: parent
                            text: MazeViewModel.statusMessage
                            font.family: "JetBrains Mono"
                            font.pixelSize: 10
                            font.bold: true
                            color: "#FFFFFF"
                        }
                    }
                }

                GridLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    columns: 4
                    columnSpacing: 8

                    MetricCard {
                        title: "Costo Total"
                        value: MazeViewModel.statsCosto
                        valueColor: Colors.mazePath
                    }

                    MetricCard {
                        title: "Visitados"
                        value: MazeViewModel.statsVisitados
                        valueColor: "#FFFFFF"
                    }

                    MetricCard {
                        title: "Máx. Cola"
                        value: MazeViewModel.statsFrontera
                        valueColor: Colors.mazeStart
                    }

                    MetricCard {
                        title: "Longitud"
                        value: MazeViewModel.statsLongitud
                        valueColor: Colors.mazeGoal
                    }
                }
            }
        }

        // ==========================================
        // 2. CONSOLA DE REGISTRO / FLUJO Y COLA
        // ==========================================
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: 8
            color: "#1E2631"
            border.color: Colors.buttonHover
            border.width: 1
            clip: true

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 10
                spacing: 8

                RowLayout {
                    Layout.fillWidth: true

                    Text {
                        text: "Flujo del Programa & Cola de Prioridad"
                        font.family: "JetBrains Mono"
                        font.pixelSize: 12
                        font.bold: true
                        color: Colors.mazeCellEmpty1
                        Layout.fillWidth: true
                    }

                    Text {
                        text: "min-heap: g(n)"
                        font.family: "JetBrains Mono"
                        font.pixelSize: 10
                        color: Colors.mazeCellEmpty2
                    }
                }

                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    ScrollBar.vertical.policy: ScrollBar.AsNeeded
                    ScrollBar.horizontal.policy: ScrollBar.AsNeeded

                    TextArea {
                        text: MazeViewModel.logText
                        readOnly: true
                        selectByMouse: true
                        font.family: "JetBrains Mono"
                        font.pixelSize: 11
                        color: "#D6DEEB"
                        background: null
                        wrapMode: TextEdit.Wrap
                        topPadding: 4
                        leftPadding: 4
                        rightPadding: 4
                        bottomPadding: 4

                        onTextChanged: cursorPosition = text.length
                    }
                }
            }
        }
    }
}
