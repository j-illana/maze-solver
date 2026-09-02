import QtQuick
import QtQuick.Layouts
import QtQuick.Dialogs
import QmlModules.ViewModel
import View.Style

Rectangle {
    id: root
    property bool expanded: false
    property real sideBarWidth: expanded ? 240 : 60
    Layout.preferredWidth: sideBarWidth
    color: Colors.sideBar

    Behavior on sideBarWidth {
        NumberAnimation {
            duration: 200
        }
    }

    ColumnLayout {
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        spacing: 0

        SideBarButton {
            icon.source: "../../assets/icons/menu.svg"
            text: "Menú"
            expanded: root.expanded

            onClicked: root.expanded = !root.expanded
        }

        SideBarButton {
            icon.source: "../../assets/icons/upload_file.svg"
            text: "Cargar laberinto"
            expanded: root.expanded
            enabled: !MazeViewModel.running

            onClicked: mazeFileDialog.open()
        }

        SideBarButton {
            icon.source: "../../assets/icons/graph.svg"
            text: "Resolver laberinto"
            expanded: root.expanded
            enabled: !MazeViewModel.running

            onClicked: mazeFileDialog.open()
        }

        SideBarButton {
            icon.source: "../../assets/icons/bar_chart.svg"
            text: "Comparar algoritmos"
            expanded: root.expanded
            enabled: !MazeViewModel.running

            onClicked: mazeFileDialog.open()
        }
    }

    FileDialog {
        id: mazeFileDialog
        title: "Selecciona el laberinto"
        nameFilters: ["Archivos de texto (*.txt)"]

        onAccepted: {
            MazeViewModel.load_maze(selectedFile)
        }
    }
}