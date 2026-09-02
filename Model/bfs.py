from collections import deque
from Model.direction import DIRECTIONS
from Model.node import Node
from Model.search_algorithm import SearchAlgorithm
from Model.search_status import SearchStatus
from typing import override

class BFS(SearchAlgorithm):
    def __init__(self, maze: list[str],
                 start: tuple[int, int], goals: list[tuple[int, int]]):
        super().__init__(maze, start, goals)
        self.queue: deque[Node] = deque()

        self.solution_path: list[Node] = []

        self.current_node: Node | None = None
        self.next_direction = 0

        self.queue.append(self.start_node)


    def step(self):
        if self.status != SearchStatus.SEARCHING:
            return

        if self.current_node is None:
            if not self.queue:
                self.status = SearchStatus.NOT_FOUND
                return

            self.current_node = self.queue.popleft()
            self.next_direction = 0

        if self.next_direction >= len(DIRECTIONS):
            self.current_node = None
            return

        direction = DIRECTIONS[self.next_direction]
        self.next_direction += 1

        neighbor = self.discover_neighbor(
            self.current_node,
            direction
        )

        if neighbor is None:
            return

        if neighbor in self.visited_nodes:
            return

        self.visited_nodes.add(neighbor)
        self.visited_order.append(neighbor)
        self.parents[neighbor] = self.current_node
        self.queue.append(neighbor)

        if neighbor.position in self.goals:
            self.status = SearchStatus.FOUND
            self.build_solution_path(neighbor)


    def build_solution_path(self, goal_node: Node):
        current_node: Node | None = goal_node
        path: list[Node] = []

        while current_node is not None:
            path.append(current_node)
            current_node = self.parents[current_node]

        path.reverse()
        self.solution_path = path


    @override
    def get_current_node(self):
        return self.current_node

    @override
    def get_solution_path(self):
        return self.solution_path