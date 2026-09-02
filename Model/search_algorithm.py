from Model.direction import Direction
from Model.graph import Graph
from Model.node import Node

class SearchAlgorithm:
    def __init__(self, maze: list[str],
                 start: tuple[int, int], goals: list[tuple[int, int]]):
        self.maze = maze.copy()
        self.start = start
        self.goals = goals
        self.graph = Graph()

    def is_valid_position(self, row: int, column: int) -> bool:
        return (
            (0 <= row < len(self.maze)) and
            (0 <= column < len(self.maze[row])) and
            (self.maze[row][column] != "#")
        )

    def get_neighbor_position(self, node: Node, 
                              direction: Direction) -> tuple[int, int]: 
        row_offset, column_offset = direction.value

        return (
            node.row + row_offset,
            node.column + column_offset
        )

    def discover_neighbor(self,node: Node, direction: Direction) -> Node | None:
        row, column = self.get_neighbor_position(node, direction)

        if not self.is_valid_position(row, column):
            return None

        neighbor = self.graph.add_node(row, column)
        self.graph.connect_nodes(node, neighbor)

        return neighbor