class Node:
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column
        self.neighbors: list["Node"] = []

    @property
    def position(self) -> tuple[int, int]:
        return self.row, self.column

    def add_neighbor(self, node: "Node"):
        if node not in self.neighbors:
            self.neighbors.append(node)

    def __repr__(self):
        return f"Nodo({self.row}, {self.column})"