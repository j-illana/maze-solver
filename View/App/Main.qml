import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts
import QmlModules.ViewModel
import View.Style

ApplicationWindow {
    title: "Prueba"
    visible: true
    width: 1920
    height: 1080
    font.family: "JetBrains Mono"
    Material.accent: Material.Blue
    color: Colors.background

    RowLayout {
        anchors.fill: parent
        spacing: 0

        SideBar {
            id: sideBar
            Layout.fillHeight: true
        }

        ContentArea {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

    Dialog {
        id: errorDialog
        title: "Laberinto inválido"
        modal: true
        implicitWidth: 400
        anchors.centerIn: parent
        standardButtons: Dialog.Ok

        property string message: ""

        Text {
            text: errorDialog.message
            font.family: "Jetbrains Mono"
            width: errorDialog.availableWidth
            wrapMode: Text.WordWrap
        }
    }

    Connections {
        target: MazeViewModel
        function onErrorOccurred(message) {
            errorDialog.message = message
            errorDialog.open()
        }
    }
}