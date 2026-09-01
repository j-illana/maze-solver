import QtQuick
import View.Style

Rectangle {
    id: root

    required property string cellType

    color: {
        switch(cellType) {
            case "#":
                return Colors.mazeWall
            case ".":
                return Colors.mazeFloorEmpty
            case ",":
                return Colors.mazeFloorRocks
            case "~":
                return Colors.mazeFloorWater
            case "S":
                return Colors.mazeStart
            case "G":
                return Colors.mazeGoal
            case "1":
                return Colors.mazeCellEmpty1
            case "2":
                return Colors.mazeCellEmpty2
            case "*":
                return Colors.mazePath
        }
    }
}