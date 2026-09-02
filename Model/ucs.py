import heapq
from typing import override
from Model.direction import DIRECTIONS
from Model.node import Node
from Model.search_algorithm import SearchAlgorithm
from Model.search_status import SearchStatus
from Model.constants import (
    FLOOR_EMPTY_COST,
    FLOOR_ROCKS_COST,
    FLOOR_WATER_COST
)

COST_MAP = {
    ".": FLOOR_EMPTY_COST,
    "G": FLOOR_EMPTY_COST,
    ",": FLOOR_ROCKS_COST,
    "~": FLOOR_WATER_COST
}

class UCS(SearchAlgorithm):
    def __init__(self, maze: list[str],
                 start: tuple[int, int], goals: list[tuple[int, int]]):
        super().__init__(maze, start, goals)

        self.pq: list[tuple[int, int, Node]] = []
        self.counter = 0
        self.cost_so_far: dict[tuple[int, int], int] = {self.start: 0}
        self.closed_set: set[tuple[int, int]] = set()

        self.current_node: Node | None = None
        self.current_cost = 0
        self.next_direction = 0
        self.solution_path: list[Node] = []

        heapq.heappush(self.pq, (0, self.counter, self.start_node))

    def step(self):
        if self.status != SearchStatus.SEARCHING:
            return

        if self.current_node is None:
            while self.pq:
                cost, _, node = heapq.heappop(self.pq)
                if node.position not in self.closed_set:
                    self.current_node = node
                    self.current_cost = cost
                    self.closed_set.add(node.position)
                    self.next_direction = 0
                    break

            if self.current_node is None:
                self.status = SearchStatus.NOT_FOUND
                return

            if self.current_node.position in self.goals:
                self.status = SearchStatus.FOUND
                self.build_solution_path(self.current_node)
                return

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

        if neighbor.position in self.closed_set:
            return

        cell_type = self.maze[neighbor.row][neighbor.column]
        step_cost = COST_MAP.get(cell_type, FLOOR_EMPTY_COST)
        new_cost = self.current_cost + step_cost

        if neighbor.position not in self.cost_so_far or new_cost < self.cost_so_far[neighbor.position]:
            self.cost_so_far[neighbor.position] = new_cost
            self.parents[neighbor] = self.current_node

            if neighbor not in self.visited_nodes:
                self.visited_nodes.add(neighbor)
                self.visited_order.append(neighbor)

            self.counter += 1
            heapq.heappush(self.pq, (new_cost, self.counter, neighbor))

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
