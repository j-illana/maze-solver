import QtQuick
import QtQuick.Layouts
import View.Style

GridLayout {
    rows: 2
    columns: 2

    rowSpacing: 0
    columnSpacing: 0

    MazeWrapper {
        Layout.row: 0
        Layout.column: 0

        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.preferredWidth: 3
        Layout.preferredHeight: 2
    }

    Rectangle {
        Layout.row: 0
        Layout.column: 1

        Layout.rowSpan: 2

        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.preferredWidth: 1

        color: Colors.background
    }

    Rectangle {
        Layout.row: 1
        Layout.column: 0

        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.preferredHeight: 1

        color: Colors.background
    }
}