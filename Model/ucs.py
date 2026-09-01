import heapq
from typing import List, Tuple, Optional, Dict

# ==============================================================================
# 1. TABLA DE COSTOS POR TIPO DE TERRENO
# ==============================================================================
# Mapeo de caracteres a sus respectivos costos de desplazamiento (g(n)).
# - '#' no está en el diccionario porque es intransitable.
# - 'S' tiene costo 0 (posición de origen).
# - 'G' y '.' comparten el costo base de 1.
COSTOS_TERRENO: Dict[str, int] = {
    '.': 1,   # Camino libre
    ',': 5,   # Terreno difícil / accidentado
    '~': 10,  # Agua / Pantano
    'S': 0,   # Casilla de salida (origen)
    'G': 1    # Meta / Objetivo
}

# Direcciones de movimiento permitidas (Arriba, Abajo, Izquierda, Derecha)
# Formato: (delta_fila, delta_columna)
MOVIMIENTOS: List[Tuple[int, int]] = [
    (-1, 0),  # Arriba
    (1, 0),   # Abajo
    (0, -1),  # Izquierda
    (0, 1)    # Derecha
]


# ==============================================================================
# 2. FUNCIONES AUXILIARES
# ==============================================================================
def encontrar_posicion(laberinto: List[str], simbolo: str) -> Optional[Tuple[int, int]]:
    """
    Busca las coordenadas de un símbolo específico en la matriz del laberinto.
    
    Args:
        laberinto (List[str]): Matriz de caracteres que representa el laberinto.
        simbolo (str): Carácter a buscar ('S' o 'G').
        
    Returns:
        Optional[Tuple[int, int]]: Coordenadas (fila, columna) o None si no se encuentra.
    """
    for f, fila in enumerate(laberinto):
        for c, celda in enumerate(fila):
            if celda == simbolo:
                return (f, c)
    return None


# ==============================================================================
# 3. ALGORITMO DE BÚSQUEDA DE COSTO UNIFORME (UCS)
# ==============================================================================
def costo_uniforme(laberinto: List[str]) -> Tuple[Optional[List[Tuple[int, int]]], float]:
    """
    Estructuras de Datos Utilizadas:
    1. `frontera` (Cola de Prioridad con `heapq`):
       - Almacena tuplas: `(costo_acumulado, (fila, col), ruta_recorrida)`.
       - `heapq` mantiene el montículo binario (min-heap) para extraer el nodo con 
         menor costo en O(log N).
    2. `visitados` (Conjunto Cerrado con `set`):
       - Almacena tuplas `(fila, col)`. Proporciona búsquedas en O(1).
       - Registra los nodos ya expandidos. En UCS, una vez que un nodo se extrae de la 
         frontera, tenemos la certeza matemática de haber llegado a él por su ruta más barata.
    3. `Descarte Diferido (Lazy Deletion)`:
       - Si al extraer un nodo de la frontera sus coordenadas ya están en `visitados`,
         se descarta inmediatamente sin procesar sus vecinos.

    Args:
        laberinto (List[str]): Representación del laberinto como lista de cadenas/filas.

    Returns:
        Tuple[Optional[List[Tuple[int, int]]], float]: 
            - Lista de coordenadas [(f1, c1), (f2, c2), ...] que componen el camino óptimo.
            - Costo total acumulado de la ruta.
            - Devuelve (None, inf) si no existe un camino accesible hacia la meta.
    """
    # Validaciones iniciales de dimensiones y puntos clave
    if not laberinto or not laberinto[0]:
        return None, float('inf')

    filas = len(laberinto)
    columnas = len(laberinto[0])

    inicio = encontrar_posicion(laberinto, 'S')
    meta = encontrar_posicion(laberinto, 'G')

    if not inicio or not meta:
        return None, float('inf')

    # Inicialización de la Frontera (Min-Heap)
    # Tupla: (costo_acumulado_g, (fila, col), camino_hasta_aqui)
    frontera = []
    heapq.heappush(frontera, (0, inicio, [inicio]))

    # Conjunto de nodos cerrados/visitados
    visitados = set()

    while frontera:
        # Extraer el nodo con menor costo acumulado g(n) de toda la frontera
        costo_actual, (f_act, c_act), ruta_actual = heapq.heappop(frontera)

        # ----------------------------------------------------------------------
        # Descarte diferido (Lazy evaluation):
        # Si ya expandimos esta casilla previamente con un costo menor, la ignoramos.
        # ----------------------------------------------------------------------
        if (f_act, c_act) in visitados:
            continue

        # Marcar la celda actual como cerrada/visitada
        visitados.add((f_act, c_act))

        # ----------------------------------------------------------------------
        # Prueba de Meta (Goal Test):
        # IMPORTANTE: En UCS, la meta se valida ÚNICAMENTE al EXTRAER del heap,
        # NUNCA al generar los vecinos. Esto garantiza que la ruta sea estrictamente óptima.
        # ----------------------------------------------------------------------
        if (f_act, c_act) == meta:
            return ruta_actual, costo_actual

        # ----------------------------------------------------------------------
        # Expansión de Vecinos (Arriba, Abajo, Izquierda, Derecha)
        # ----------------------------------------------------------------------
        for df, dc in MOVIMIENTOS:
            f_vec, c_vec = f_act + df, c_act + dc

            # 1. Validar que no salga de los límites de la matriz
            if 0 <= f_vec < filas and 0 <= c_vec < columnas:
                simbolo_vecino = laberinto[f_vec][c_vec]

                # 2. Validar que no sea pared ('#') y que no haya sido cerrado previamente
                if simbolo_vecino != '#' and (f_vec, c_vec) not in visitados:
                    costo_paso = COSTOS_TERRENO.get(simbolo_vecino, 1)
                    nuevo_costo = costo_actual + costo_paso
                    nueva_ruta = ruta_actual + [(f_vec, c_vec)]

                    # Insertar en la cola de prioridad
                    heapq.heappush(frontera, (nuevo_costo, (f_vec, c_vec), nueva_ruta))

    # Si la frontera se vacía sin alcanzar la meta, el destino es inalcanzable
    return None, float('inf')



