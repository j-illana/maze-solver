import QtQuick
import QtQuick.Layouts
import QmlModules.ViewModel
import View.Style

RowLayout {
    id: root
    spacing: 0

    ColumnLayout {
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.preferredWidth: 3

        spacing: 0

        MazeContainer {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredHeight: 3
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredHeight: 1

            color: Colors.background
        }
    }

    FlowPanel {
        id: flowPanel
        Layout.fillHeight: true
        Layout.preferredWidth: MazeViewModel.flowPanelVisible ? Math.min(root.width * 0.45, 550) : 0
        visible: Layout.preferredWidth > 0
        clip: true

        Behavior on Layout.preferredWidth {
            NumberAnimation {
                duration: 250
                easing.type: Easing.InOutQuad
            }
        }
    }
}