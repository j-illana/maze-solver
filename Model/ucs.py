import heapq
from typing import Dict, List, Tuple
from Model.direction import DIRECTIONS
from Model.node import Node
from Model.search_algorithm import SearchAlgorithm
from Model.search_status import SearchStatus

COSTOS_TERRENO: Dict[str, int] = {
    '.': 1,
    ',': 5,
    '~': 10,
    'S': 0,
    'G': 1
}

class UCS(SearchAlgorithm):
    def __init__(self, maze: list[str], start: tuple[int, int], goals: list[tuple[int, int]]):
        super().__init__(maze, start, goals)

        self.visited_nodes: set[Node] = set()
        self.closed_positions: set[tuple[int, int]] = set()
        
        # Guardamos el mejor costo g(n) conocido para cada posición
        self.costos_g: dict[tuple[int, int], int] = {}
        
        # Diccionario para reconstruir el camino: nodo -> nodo_padre
        self.padres: dict[Node, Node] = {}

        # Contador secuencial para desempate en min-heap
        self.counter = 0

        start_node = self.graph.add_node(*self.start)
        self.costos_g[self.start] = 0
        
        # Priority Queue (Min-Heap): (costo_g, contador, node)
        self.pq: list[tuple[int, int, Node]] = []
        heapq.heappush(self.pq, (0, self.counter, start_node))

        # Estadísticas
        self.max_frontera = 1
        self.nodos_explorados = 0
        self.total_inserciones = 1
        self.pasos = 0
        self.costo_total = 0

        # Formato inicial del log
        self.logs: list[str] = [
            "Traza del algoritmo UCS",
            "--------------------------------------------------",
            "Paso 0:",
            f"  Frontera : {{{self._formatear_nodo(start_node, 0)}}}",
            f"  Extrae   : {self._formatear_pos(self.start)} (g = 0)",
            "--------------------------------------------------"
        ]

        self.status = (
            SearchStatus.FOUND if self.start in self.goals
            else SearchStatus.SEARCHING
        )

    def _formatear_pos(self, pos: tuple[int, int]) -> str:
        r, c = pos
        simb = self.maze[r][c]
        if simb == 'S':
            return f"S({r},{c})"
        elif simb == 'G':
            return f"G({r},{c})"
        return f"({r},{c})"

    def _formatear_nodo(self, node: Node, g: int) -> str:
        return f"({self._formatear_pos(node.position)}, {g})"

    def _obtener_frontera_str(self, limite: int = 5) -> str:
        # Ordenamos los elementos actuales de la cola por costo
        elementos_ordenados = sorted(self.pq, key=lambda x: x[0])
        items = [f"({self._formatear_pos(node.position)}, {g})" for g, _, node in elementos_ordenados[:limite]]
        if len(elementos_ordenados) > limite:
            items.append(f"... (+{len(elementos_ordenados) - limite} más)")
        return "{" + ", ".join(items) + "}"

    def step(self):
        if self.status != SearchStatus.SEARCHING:
            return

        if not self.pq:
            self.status = SearchStatus.NOT_FOUND
            self.logs.extend([
                "\n[Sin Solución]",
                "  La frontera se vació sin encontrar ninguna meta."
            ])
            return

        # Snapshot de la frontera antes de extraer
        frontera_antes_str = self._obtener_frontera_str()

        costo_act, _, current_node = heapq.heappop(self.pq)
        pos_act = current_node.position

        # Descarte diferido si ya cerramos esta posición
        if pos_act in self.closed_positions:
            return

        self.pasos += 1
        self.max_frontera = max(self.max_frontera, len(self.pq) + 1)

        self.closed_positions.add(pos_act)
        self.visited_nodes.add(current_node)
        self.nodos_explorados = len(self.visited_nodes)

        # Actualizar stack con la ruta actual para renderizado en UI
        self.stack = self._reconstruir_ruta_nodos(current_node)

        # Registro del paso actual
        paso_log = [
            f"\nPaso {self.pasos}:",
            f"  Frontera : {frontera_antes_str}",
            f"  Extrae   : {self._formatear_pos(pos_act)} (g = {costo_act})"
        ]

        # Comprobar meta al extraer de la cola de prioridad
        if pos_act in self.goals:
            self.status = SearchStatus.FOUND
            self.costo_total = costo_act
            ruta_str = " -> ".join(self._formatear_pos(node.position) for node, _ in self.stack)
            
            paso_log.append("  -> ¡Es estado objetivo! Termina la búsqueda.")
            paso_log.extend([
                "\n==================================================",
                "Solución Final",
                "==================================================",
                f"  Meta alcanzada : {self._formatear_pos(pos_act)}",
                f"  Ruta óptima    : {ruta_str}",
                f"  Costo total g  : {costo_act}",
                f"  Longitud ruta  : {len(self.stack)} pasos",
                f"  Nodos cerrados : {self.nodos_explorados}",
                f"  Máx. frontera  : {self.max_frontera}",
                "=================================================="
            ])
            self.logs.extend(paso_log)
            return

        # Generar vecinos
        generados = []
        for direction in DIRECTIONS:
            neighbor = self.discover_neighbor(current_node, direction)
            if neighbor is None:
                continue

            pos_vec = neighbor.position
            if pos_vec in self.closed_positions:
                continue

            simb_vec = self.maze[neighbor.row][neighbor.column]
            costo_paso = COSTOS_TERRENO.get(simb_vec, 1)
            nuevo_costo = costo_act + costo_paso

            # Si encontramos un mejor camino a este vecino (o primera vez visto)
            if pos_vec not in self.costos_g or nuevo_costo < self.costos_g[pos_vec]:
                es_actualizacion = pos_vec in self.costos_g
                self.costos_g[pos_vec] = nuevo_costo
                self.padres[neighbor] = current_node
                self.counter += 1
                heapq.heappush(self.pq, (nuevo_costo, self.counter, neighbor))
                self.total_inserciones += 1
                
                info_gen = f"{self._formatear_pos(pos_vec)} con costo {costo_act} + {costo_paso} = {nuevo_costo}"
                if es_actualizacion:
                    info_gen += " (actualiza ruta)"
                generados.append(info_gen)

        if generados:
            paso_log.append("  Genera   : " + ", ".join(generados))
        else:
            paso_log.append("  Genera   : (sin vecinos nuevos)")

        self.logs.extend(paso_log)

    def _reconstruir_ruta_nodos(self, node: Node) -> list[tuple[Node, int]]:
        ruta = []
        curr: Node | None = node
        while curr is not None:
            ruta.append((curr, 0))
            curr = self.padres.get(curr)
        ruta.reverse()
        return ruta
