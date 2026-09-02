pragma Singleton

import QtQuick

QtObject {
    readonly property color sideBar: "#C1CBD7"
    readonly property color buttonHover: "#8399AF"
    readonly property color background: "#384657"

    readonly property color mazeCellEmpty1: "#CDD5DF"
    readonly property color mazeCellEmpty2: "#A8B6C7"

    readonly property color mazeWall: "#35281C"
    readonly property color mazeFloorEmpty: "#B99879"
    readonly property color mazeFloorRocks: "#4E4E4E"
    readonly property color mazeFloorWater: "#7EA3CC"
    readonly property color mazeStart: "#F67728"
    readonly property color mazeGoal: "#0C6F32"
    readonly property color mazePath: "#F1C40F"

    readonly property color currentCell: "#80FFDD1F"
    readonly property color visitedCell: "#8001148D"
    readonly property color unvisitedCell: "transparent"
    readonly property color solutionPathCell: "#800A852B"
}
