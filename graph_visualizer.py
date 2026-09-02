import matplotlib.pyplot as plt
import networkx as nx

from Model.search_algorithm import SearchAlgorithm


def calculate_tree_positions(algorithm: SearchAlgorithm):
    children = {
        node: []
        for node in algorithm.visited_order
    }

    for node in algorithm.visited_order:
        parent = algorithm.parents[node]

        if parent is not None:
            children[parent].append(node)

    positions = {}
    next_x = 0

    def position_node(node, depth):
        nonlocal next_x

        node_children = children[node]

        if not node_children:
            x = next_x
            next_x += 1

        else:
            child_positions = []

            for child in node_children:
                child_x = position_node(
                    child,
                    depth + 1
                )

                child_positions.append(child_x)

            x = (
                child_positions[0]
                + child_positions[-1]
            ) / 2

        positions[node.position] = (
            x,
            -depth
        )

        return x

    position_node(
        algorithm.start_node,
        0
    )

    return positions

def show_search_tree(
    algorithm: SearchAlgorithm
):
    tree = nx.DiGraph()

    for node in algorithm.visited_order:
        tree.add_node(node.position)

    for node in algorithm.visited_order:
        parent = algorithm.parents[node]

        if parent is not None:
            tree.add_edge(
                parent.position,
                node.position
            )

    positions = calculate_tree_positions(
        algorithm
    )

    solution_path = algorithm.get_solution_path()

    solution_nodes = {
        node.position
        for node in solution_path
    }

    node_colors = [
        "green"
        if node in solution_nodes
        else "lightblue"
        for node in tree.nodes
    ]

    plt.figure(figsize=(12, 8))

    nx.draw(
        tree,
        pos=positions,
        with_labels=True,
        arrows=False,
        node_size=1200,
        font_size=8,
        node_color=node_colors
    )

    plt.title(
        f"Árbol de búsqueda - "
        f"{type(algorithm).__name__}"
    )

    plt.tight_layout()

    plt.show(block=False)