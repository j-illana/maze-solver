from Model.direction import DIRECTIONS
from Model.node import Node
from Model.search_algorithm import SearchAlgorithm
from Model.search_status import SearchStatus

class DFS(SearchAlgorithm):
    def __init__(self, maze: list[str],
                 start: tuple[int, int], goals: list[tuple[int, int]]):
        super().__init__(maze, start, goals)

        self.visited_nodes: set[Node] = set()
        self.stack: list[tuple[Node, int]] = []

        start_node = self.graph.add_node(*self.start)
        self.visited_nodes.add(start_node)
        self.stack.append((start_node, 0))

        self.status = (
            SearchStatus.FOUND if self.start in self.goals
            else SearchStatus.SEARCHING
        )
        
    def step(self):
        if self.status != SearchStatus.SEARCHING:
            return

        if not self.stack:
            self.status = SearchStatus.NOT_FOUND
            return

        current_node, next_direction = self.stack[-1]

        if next_direction >= len(DIRECTIONS):
            self.stack.pop()
            return

        direction = DIRECTIONS[next_direction]

        self.stack[-1] = (current_node, next_direction + 1)
        neighbor = self.discover_neighbor(current_node, direction)

        if neighbor is None:
            return

        if neighbor in self.visited_nodes:
            return

        self.visited_nodes.add(neighbor)
        self.stack.append((neighbor, 0))

        if neighbor.position in self.goals:
            self.status = SearchStatus.FOUND