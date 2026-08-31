import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import View.Style

Button {
    id: root
    property bool expanded: false
    Layout.fillWidth: true
    
    HoverHandler {
        cursorShape: Qt.PointingHandCursor
    }

    display: expanded
        ? AbstractButton.TextBesideIcon 
        : AbstractButton.IconOnly

    background: Rectangle {
        anchors.fill: parent
        color: root.hovered
            ? Colors.buttonHover
            : Colors.sideBar
    }
}