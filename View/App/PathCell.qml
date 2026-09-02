import QtQuick
import View.Style

Rectangle {
    property int cellType: 0

    color: {
        switch (cellType) {
            case 0: 
                return Colors.unvisitedCell
            case 1:
                return Colors.visitedCell
            case 2:
                return Colors.currentCell
            case 3:
                return Colors.solutionPathCell
        }
    }
}