import QtQuick
import QtQuick.Layouts

StackLayout {
    id: contentStack
    currentIndex: 0

    SolveMazeView {
        currentPage: contentStack.currentIndex
    }

    SolveMazeView {
        currentPage: contentStack.currentIndex
    }
}