import os
import sys
import algorithms.MaximalFlow as MaximalFlow
from algorithms.MaximalFlow import Tee


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



def display_cost_matrix(cost_matrix):
    print("Matrice de coût:")
    for row in cost_matrix:
        print("  ", row)
    print()


def get_source_and_sink(cost_matrix):
    return MaximalFlow.get_source_and_sink(cost_matrix)


def bellman_ford(res_cost, res_cap, source, sink):
    """
    Bellman-Ford: affiche k=0..n-1 tables (dist, prev),
    ne relâche que sur arcs résiduels (res_cap>0).
    """
    n = len(res_cost)
    INF = float('inf')
    dist = [INF] * n
    prev = [None] * n
    dist[source] = 0

    # En-tête
    nodes = list(range(n))
    header = 'Iter |' + ''.join(f' {i:>6}' for i in nodes)
    sep = '-' * len(header)
    print('=== Bellman-Ford ===')
    print(header)
    print(sep)

    # k=0
    print(f"{0:>4} |" + ''.join(f" {'0' if j == source else '∞':>6}" for j in nodes))
    print('     |' + ''.join(f" {'-' if prev[j] is None else prev[j]:>6}" for j in nodes))

    # k=1..n-1
    for k in range(1, n):
        for u in range(n):
            for v in range(n):
                if res_cap[u][v] > 0:
                    w = res_cost[u][v]
                    if w != 0 and dist[u] != float('inf') and dist[u] + w < dist[v]:
                        dist[v] = dist[u] + w
                        prev[v] = u
        # Display the iteration results
        print(f"{k:>4} |" + ''.join(f" {(dist[j] if dist[j] != float('inf') else '∞'):>6}" for j in nodes))
        print('     |' + ''.join(f" {'-' if prev[j] is None else prev[j]:>6}" for j in nodes))
    # reconstruction
    if dist[sink] == INF:
        print('Pas de chemin s→t')
        return None, None
    path = []
    u = sink
    while u is not None:
        path.insert(0, u)
        u = prev[u]

    print(f"Chemin trouvé: {path} (coût = {dist[sink]})")
    return path, dist[sink]


def minimal_cost_flow(cap_mat, cost_mat, source, sink, required_flow):
    """
    Flot à coût minimal par chaînes améliorantes successives.
    Retourne (flow_value, total_cost, flow_matrix)
    """
    n = len(cap_mat)
    # initialiser résiduels
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
        print(f"\n--- Itération #{iteration}: flot={flow_value}, coût={total_cost} ---")
        # Bellman-Ford complet sur arcs résiduels
        path, path_cost = bellman_ford(res_cost, res_cap, source, sink)
        if path is None:
            print("Plus de chaîne possible.")
            break
        # goulot
        delta = required_flow - flow_value
        for u, v in zip(path, path[1:]):
            delta = min(delta, res_cap[u][v])
        print(f"Chaîne: {path}, delta={delta}, coût unitaire={path_cost}")
        # maj
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

            MaximalFlow.display_capacity_matrix(cap)
            display_cost_matrix(cost)

            s, t = get_source_and_sink(cost)
            print(f"Source={s}, Sink={t}\n")

            cap_copy = [row[:] for row in cap]
            fmax = MaximalFlow.ford_fulkerson(cap_copy, s, t)
            print(f"Flot max possible = {fmax}\n")

            while True:
                F = int(input(f"Entrez flot désiré (1..{fmax}): ").strip())
                if 1 <= F <= fmax:
                    break
                print(f"Erreur: 1 ≤ flot ≤ {fmax}.")
            print(f"\n--- Calcul pour flot = {F} ---")

            fv, tc, Fmat = minimal_cost_flow(cap, cost, s, t, F)
            if fv == F:
                print(f"\n=== Résultat final ===")
                print(f"Flot total obtenu = {fv}")
                print(f"Coût total minimal = {tc}\n")
                print("Flux arc (f/c; coût_unitaire):")
                n = len(cap)
                for u in range(n):
                    for v in range(n):
                        if cap[u][v] > 0:
                            print(f" {u}->{v}: ({Fmat[u][v]}/{cap[u][v]}; {cost[u][v]})")
            else:
                print("Objectif non atteint.")
        finally:
            sys.stdout = orig
    print(f"Trace saved to {trace_file}")