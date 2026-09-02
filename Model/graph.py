from Model.node import Node

class Graph:
    def __init__(self):
        self.nodes: dict[tuple[int, int], Node] = {}

    def add_node(self, row: int, column: int):
        position = (row, column)

        if position not in self.nodes:
            self.nodes[position] = Node(row, column)

        return self.nodes[position]

    def get_node(self, row: int, column: int):
        return self.nodes.get((row, column))

    def connect_nodes(self, node_a: Node, node_b: Node):
        node_a.add_neighbor(node_b)
        node_b.add_neighbor(node_a)