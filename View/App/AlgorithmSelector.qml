import QtQuick
import QtQuick.Controls
import QmlModules.ViewModel

ComboBox {
    id: comboBox

    verticalPadding: 10
    leftPadding: 12

    model: [
        "DFS",
        "BFS",
        "UCS"
    ]

    enabled: !MazeViewModel.running

    background: Rectangle {
        radius: 8
        color: "white"
        border.width: 1
        border.color: "gray"
    }

    contentItem: Text {
        text: comboBox.displayText

        verticalAlignment: Text.AlignVCenter

        font.family: "Jetbrains Mono"
        font.pixelSize: 16
    }
}