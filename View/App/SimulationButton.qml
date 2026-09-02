import QtQuick
import QtQuick.Controls
import QmlModules.ViewModel
import View.Style

Button {
    id: root
    enabled: !MazeViewModel.running
    
    HoverHandler {
        cursorShape: Qt.PointingHandCursor
    }

    font.pixelSize: 16

    background: Rectangle {
        anchors.fill: parent
        radius: 10
        color: root.hovered
            ? Colors.buttonHover
            : Colors.sideBar
    }
}