from Model.direction import Direction
from Model.graph import Graph
from Model.node import Node
from Model.search_status import SearchStatus
from Model.constants import (
    FLOOR_EMPTY_COST, FLOOR_START_COST,
    FLOOR_ROCKS_COST, FLOOR_WATER_COST
)

class SearchAlgorithm:
    def __init__(self, maze: list[str],
                 start: tuple[int, int], goals: list[tuple[int, int]]):
        self.maze = maze.copy()
        self.start = start
        self.goals = goals
        self.graph = Graph()
        self.visited_nodes: set[Node] = set()
        self.visited_order: list[Node] = []
        self.start_node = self.graph.add_node(*self.start)

        self.visited_nodes.add(self.start_node)
        self.visited_order.append(self.start_node)

        self.parents: dict[Node, Node | None] = {
            self.start_node: None
        }

        self.status = (
            SearchStatus.FOUND if self.start in self.goals
            else SearchStatus.SEARCHING
        )


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


    def get_current_node(self) -> Node | None:
        raise NotImplementedError


    def get_solution_path(self) -> list[Node]:
        return []


    def get_path_cost(self) -> int:
        solution_path = self.get_solution_path()
        cost = 0

        for node in solution_path:
            cell = self.maze[node.row][node.column]

            if cell == "S":
                cost += FLOOR_START_COST

            elif cell == "." or cell == "G":
                cost += FLOOR_EMPTY_COST

            elif cell == ",":
                cost += FLOOR_ROCKS_COST

            elif cell == "~":
                cost += FLOOR_WATER_COST
                
        return cost