import matplotlib.pyplot as plt
import networkx as nx

from Model.search_algorithm import SearchAlgorithm


def calculate_tree_positions(algorithm: SearchAlgorithm):
    # Crea una lista de hijos para cada nodo visitado
    children = {
        node: []
        for node in algorithm.visited_order
    }

    # Construye la relación padre -> hijos usando el árbol de búsqueda
    for node in algorithm.visited_order:
        parent = algorithm.parents[node]

        if parent is not None:
            children[parent].append(node)

    positions = {}
    next_x = 0

    def position_node(node, depth):
        nonlocal next_x

        node_children = children[node]

        # Las hojas se colocan de izquierda a derecha
        if not node_children:
            x = next_x
            next_x += 1

        # Los padres se centran respecto a sus hijos
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

        # La profundidad determina la posición vertical
        positions[node.position] = (
            x,
            -depth
        )

        return x

    # Empieza a calcular posiciones desde el nodo inicial
    position_node(
        algorithm.start_node,
        0
    )

    return positions


def show_search_tree(
    algorithm: SearchAlgorithm
):
    tree = nx.DiGraph()

    # Agrega al árbol todos los nodos que fueron visitados
    for node in algorithm.visited_order:
        tree.add_node(node.position)

    # Agrega las conexiones padre -> hijo
    for node in algorithm.visited_order:
        parent = algorithm.parents[node]

        if parent is not None:
            tree.add_edge(
                parent.position,
                node.position
            )

    # Calcula una distribución jerárquica para los nodos
    positions = calculate_tree_positions(
        algorithm
    )

    solution_path = algorithm.get_solution_path()

    # Guarda las posiciones que forman parte de la solución
    solution_nodes = {
        node.position
        for node in solution_path
    }

    # Resalta en verde los nodos que pertenecen al camino solución
    node_colors = [
        "green"
        if node in solution_nodes
        else "lightblue"
        for node in tree.nodes
    ]

    # Crea y dibuja la ventana del árbol
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

    # Muestra la ventana sin bloquear la aplicación principal
    plt.show(block=False)