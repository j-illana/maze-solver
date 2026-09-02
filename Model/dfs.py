from Model.direction import DIRECTIONS
from Model.node import Node
from Model.search_algorithm import SearchAlgorithm
from Model.search_status import SearchStatus
from typing import override

class DFS(SearchAlgorithm):
    def __init__(self, maze: list[str],
                 start: tuple[int, int], goals: list[tuple[int, int]]):
        super().__init__(maze, start, goals)
        self.stack: list[tuple[Node, int]] = []
        self.stack.append((self.start_node, 0))
  
        
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

        self.parents[neighbor] = current_node

        self.visited_nodes.add(neighbor)
        self.visited_order.append(neighbor)
        self.stack.append((neighbor, 0))

        if neighbor.position in self.goals:
            self.status = SearchStatus.FOUND


    @override
    def get_current_node(self):
        if not self.stack:
            return None

        current_node, _ = self.stack[-1]
        return current_node


    @override
    def get_solution_path(self):
        if self.status != SearchStatus.FOUND:
            return []

        return [node for node, _ in self.stack]