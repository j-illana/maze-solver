import QtQuick
import QtQuick.Layouts
import View.Style

RowLayout {
    id: root
    spacing: 0
    property int currentPage: 0

    ColumnLayout {
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.preferredWidth: 3

        spacing: 0

        MazeContainer {
            currentPage: root.currentPage

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

    ColumnLayout {
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.preferredWidth: 1

        spacing: 0

        ConfigurationArea {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredHeight: 1

            currentPage: root.currentPage
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredHeight: 5

            color: Colors.background
        }
    }
}