import QtQuick
import View.Style

Rectangle {
    property int cellType: 0
    property int currentPage: 0
    property color solutionPathCell

    color: {
        if (currentPage == 0) {
            switch (cellType) {
                case 0: 
                    return Colors.unvisitedCell
                case 1:
                    return Colors.visitedCell
                case 2:
                    return Colors.currentCell
                case 3:
                    return solutionPathCell
            }
        }
        
        else if (currentPage == 1) {
            return cellType == 3 ? solutionPathCell : "transparent"
        }
    }
}