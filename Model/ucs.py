import heapq
from typing import List, Tuple, Optional, Dict

# Costo de desplazamiento por tipo de celda (g(n))
COSTOS_TERRENO: Dict[str, int] = {
    '.': 1,   # Camino libre
    ',': 5,   # Terreno accidentado
    '~': 10,  # Agua / Pantano
    'S': 0,   # Casilla origen
    'G': 1    # Meta
}

MOVIMIENTOS: List[Tuple[int, int]] = [
    (-1, 0),  # Arriba
    (1, 0),   # Abajo
    (0, -1),  # Izquierda
    (0, 1)    # Derecha
]


def encontrar_posicion(laberinto: List[str], simbolo: str) -> Optional[Tuple[int, int]]:
    """Encuentra las coordenadas (fila, columna) del símbolo buscado."""
    for f, fila in enumerate(laberinto):
        for c, celda in enumerate(fila):
            if celda == simbolo:
                return (f, c)
    return None


def costo_uniforme(laberinto: List[str], recopilar_trazas: bool = False) -> Tuple:
    """
    Algoritmo de Búsqueda de Costo Uniforme (UCS).
    Explora caminos utilizando una cola de prioridad (min-heap) ordenada por costo acumulado g(n).
    
    Returns:
        Si recopilar_trazas=False: (ruta_optima, costo_total)
        Si recopilar_trazas=True:  (ruta_optima, costo_total, stats_dict, logs_list)
    """
    stats = {
        "costo_total": float('inf'),
        "longitud_ruta": 0,
        "nodos_explorados": 0,
        "max_frontera": 0,
        "total_inserciones": 0,
        "pasos_totales": 0
    }
    logs: List[str] = []

    if not laberinto or not laberinto[0]:
        if recopilar_trazas:
            logs.append("[ERROR] Laberinto vacío o inválido.")
            return None, float('inf'), stats, logs
        return None, float('inf')

    filas, columnas = len(laberinto), len(laberinto[0])
    inicio = encontrar_posicion(laberinto, 'S')
    meta = encontrar_posicion(laberinto, 'G')

    if not inicio or not meta:
        if recopilar_trazas:
            logs.append("[ERROR] Puntos de inicio 'S' o meta 'G' no encontrados.")
            return None, float('inf'), stats, logs
        return None, float('inf')

    if recopilar_trazas:
        logs.extend([
            "=" * 50,
            "         INICIO DE BÚSQUEDA UCS (UNIFORM COST)",
            "=" * 50,
            f"Dimensiones: {filas} filas x {columnas} columnas",
            f"Punto de Salida 'S': {inicio} | Meta 'G': {meta}",
            "-" * 50,
            f"[COLA INIT] Insertado origen S{inicio} con g(n)=0"
        ])

    # Frontera (Min-Heap): (costo_acumulado_g, (fila, col), ruta_actual)
    frontera = [(0, inicio, [inicio])]
    stats["total_inserciones"] = 1
    stats["max_frontera"] = 1

    visitados = set()
    paso = 0

    while frontera:
        stats["max_frontera"] = max(stats["max_frontera"], len(frontera))
        costo_act, (f_act, c_act), ruta_act = heapq.heappop(frontera)
        paso += 1
        stats["pasos_totales"] = paso

        if recopilar_trazas:
            simb = laberinto[f_act][c_act]
            logs.append(f"\n[PASO {paso}] Pop -> Casilla ({f_act}, {c_act}) ['{simb}'] | g(n) = {costo_act}")

        # Descarte diferido: ignorar si ya fue explorada con menor costo
        if (f_act, c_act) in visitados:
            if recopilar_trazas:
                logs.append(f"  -> [DESCARTE DIFERIDO] ({f_act}, {c_act}) ya visitada. Omitiendo.")
            continue

        visitados.add((f_act, c_act))
        stats["nodos_explorados"] = len(visitados)

        # Prueba de Meta al extraer del montículo
        if (f_act, c_act) == meta:
            stats["costo_total"] = costo_act
            stats["longitud_ruta"] = len(ruta_act)
            if recopilar_trazas:
                logs.extend([
                    "\n" + "=" * 50,
                    "            ¡META 'G' ALCANZADA!",
                    "=" * 50,
                    f"  * Costo Óptimo Total g(Meta): {costo_act}",
                    f"  * Longitud del Camino: {len(ruta_act)} celdas",
                    f"  * Nodos Cerrados (Visitados): {len(visitados)}",
                    f"  * Tamaño Máx. Frontera: {stats['max_frontera']}",
                    f"  * Inserciones Totales en Cola: {stats['total_inserciones']}",
                    "=" * 50
                ])
                return ruta_act, costo_act, stats, logs
            return ruta_act, costo_act

        # Expansión de vecinos
        for df, dc in MOVIMIENTOS:
            f_vec, c_vec = f_act + df, c_act + dc

            if 0 <= f_vec < filas and 0 <= c_vec < columnas:
                simb_vec = laberinto[f_vec][c_vec]
                if simb_vec != '#' and (f_vec, c_vec) not in visitados:
                    paso_costo = COSTOS_TERRENO.get(simb_vec, 1)
                    nuevo_costo = costo_act + paso_costo
                    nueva_ruta = ruta_act + [(f_vec, c_vec)]

                    heapq.heappush(frontera, (nuevo_costo, (f_vec, c_vec), nueva_ruta))
                    stats["total_inserciones"] += 1

                    if recopilar_trazas:
                        logs.append(f"  -> [+] Push Vecino ({f_vec}, {c_vec}) ['{simb_vec}'] (+{paso_costo}) -> g(n) = {nuevo_costo}")

        if recopilar_trazas:
            top_cola = [(item[0], item[1]) for item in sorted(frontera, key=lambda x: x[0])[:5]]
            logs.append(f"  -> [ESTADO COLA] {len(frontera)} elems. Top: {top_cola}")

    if recopilar_trazas:
        logs.append("\n[FIN] Frontera vacía: la meta es inalcanzable.")
        return None, float('inf'), stats, logs
    return None, float('inf')



