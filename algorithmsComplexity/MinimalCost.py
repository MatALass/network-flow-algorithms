import os
import sys
import algorithms.MaximalFlow as MaximalFlow
from algorithms.MaximalFlow import Tee
import time


def create_cost_matrix(file_name):
    base_dir = os.path.dirname(__file__)  # chemin du fichier MinimalCost.py
    root_dir = os.path.abspath(os.path.join(base_dir, ".."))  # dossier ProjetRechercheOp
    full_path = os.path.join(root_dir, file_name)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"File not found : {full_path}")

    with open(full_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    n = int(lines[0])
    expected_lines = 1 + 2 * n
    if len(lines) < expected_lines:
        raise ValueError(f"Le fichier {file_name} est incomplet : {len(lines)} lignes trouvées, {expected_lines} attendues.")

    cost_lines = lines[1 + n : 1 + 2 * n]
    cost_matrix = []

    for i, line in enumerate(cost_lines):
        row = list(map(int, line.split()))
        if len(row) != n:
            raise ValueError(f"Ligne {i + 1 + n} du fichier {file_name} : {len(row)} valeurs trouvées, {n} attendues.")
        cost_matrix.append(row)

    return cost_matrix

def get_source_and_sink(cost_matrix):
    return MaximalFlow.get_source_and_sink(cost_matrix)


def bellman_ford(res_cost, res_cap, source, sink):
    n = len(res_cost)
    INF = float('inf')
    dist = [INF] * n
    prev = [None] * n
    dist[source] = 0
    nodes = list(range(n))
    header = 'Iter |' + ''.join(f' {i:>6}' for i in nodes)
    sep = '-' * len(header)

    for k in range(1, n):
        for u in range(n):
            for v in range(n):
                if res_cap[u][v] > 0:
                    w = res_cost[u][v]
                    if w != 0 and dist[u] != float('inf') and dist[u] + w < dist[v]:
                        dist[v] = dist[u] + w
                        prev[v] = u
    if dist[sink] == INF:
        return None, None
    path = []
    u = sink
    while u is not None:
        path.insert(0, u)
        u = prev[u]
    return path, dist[sink]


def minimal_cost_flow(cap_mat, cost_mat, source, sink, required_flow):
    n = len(cap_mat)
    res_cap = [row[:] for row in cap_mat]
    res_cost = [[0]*n for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if cap_mat[u][v] > 0:
                res_cost[u][v] = cost_mat[u][v]
                res_cost[v][u] = -cost_mat[u][v]

    flow_value = 0
    total_cost = 0
    flow_mat = [[0]*n for _ in range(n)]
    iteration = 0

    while flow_value < required_flow:
        iteration += 1
        path, path_cost = bellman_ford(res_cost, res_cap, source, sink)
        if path is None:
            break
        delta = required_flow - flow_value
        for u, v in zip(path, path[1:]):
            delta = min(delta, res_cap[u][v])
        for u, v in zip(path, path[1:]):
            res_cap[u][v] -= delta
            res_cap[v][u] += delta
            if cap_mat[u][v] > 0:
                flow_mat[u][v] += delta
            else:
                flow_mat[v][u] -= delta
        flow_value += delta
        total_cost += delta * path_cost

    return flow_value, total_cost, flow_mat


def main_minimal_cost(numbertest):
    project_dir = os.path.dirname(os.path.abspath(__file__))
    trace_file = os.path.join(project_dir, 'tracefiles', f'K5-trace{numbertest}-MC')
    os.makedirs(os.path.dirname(trace_file), exist_ok=True)

    with open(trace_file, 'w', encoding='utf-8') as f:
        orig = sys.stdout
        sys.stdout = Tee(f, orig)
        try:
            cap = MaximalFlow.create_capacity_matrix(f'/testfiles/test{numbertest}')
            cost = create_cost_matrix(f'/testfiles/test{numbertest}')
            s, t = get_source_and_sink(cost)

            cap_copy = [row[:] for row in cap]
            fmax = MaximalFlow.ford_fulkerson(cap_copy, s, t)

            while True:
                F = int(input(f"Entrez flot désiré (1..{fmax}): ").strip())
                if 1 <= F <= fmax:
                    break

            start_time = time.time()  # Début du suivi du temps
            fv, tc, Fmat = minimal_cost_flow(cap, cost, s, t, F)
            end_time = time.time()  # Fin du suivi du temps

            elapsed_time = end_time - start_time
            if fv == F:
                print(f"\n=== Résultat final ===")
                print(f"Temps d'exécution: {elapsed_time:.4f} secondes")  # Affiche seulement le temps

        finally:
            sys.stdout = orig