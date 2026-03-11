import time
import os
from algorithms.MaximalFlow import create_capacity_matrix, get_source_and_sink, ford_fulkerson
from algorithms.MinimalCost import create_cost_matrix, minimal_cost_flow
from algorithms.pushRelabel import push_relabel  


def test_ford_fulkerson(capacity_matrix, source, sink, test_number):
    print(f"--- Test Ford-Fulkerson sur test{test_number} ---")
    start_time = time.time()
    max_flow = ford_fulkerson(capacity_matrix, source, sink)
    end_time = time.time()

    print(f"Flot maximal: {max_flow}")
    print(f"Temps d'exécution : {end_time - start_time:.6f} secondes\n")
    return end_time - start_time

def test_minimal_cost_flow(capacity_matrix, source, sink, test_number, required_flow=None):
    print(f"--- Test Flot à Coût Minimal sur test{test_number} ---")
    cost_matrix = create_cost_matrix(f"testfiles/test{test_number}")

    if required_flow is None:
        required_flow = ford_fulkerson(capacity_matrix, source, sink)

    start_time = time.time()
    flow_value, total_cost, flow_matrix = minimal_cost_flow(capacity_matrix, cost_matrix, source, sink, required_flow)
    end_time = time.time()

    print(f"Flot obtenu: {flow_value}, Coût total: {total_cost}")
    print(f"Temps d'exécution : {end_time - start_time:.6f} secondes\n")
    return end_time - start_time

def test_push_relabel(capacity_matrix, source, sink, test_number):
    print(f"--- Test Push-Relabel sur test{test_number} ---")

    start_time = time.time()
    max_flow = push_relabel(capacity_matrix, source, sink)
    end_time = time.time()

    print(f"Flot maximal (Push-Relabel): {max_flow}")
    print(f"Temps d'exécution : {end_time - start_time:.6f} secondes\n")
    return end_time - start_time

def analyser_complexite(nb_tests=10):
    print("=== Analyse de Complexité ===\n")
    for i in range(6, nb_tests + 1):
        capacity_matrix = create_capacity_matrix(f"testfiles/test{i}")
        source, sink = get_source_and_sink(capacity_matrix)
        ff_time = test_ford_fulkerson(capacity_matrix, source, sink, i)
        pr_time = test_push_relabel(capacity_matrix, source, sink, i)
        mcf_time = test_minimal_cost_flow(capacity_matrix, source, sink, i)
        print(f"Résumé Test {i}: Ford-Fulkerson = {ff_time:.6f}s, Push-Relabel = {pr_time:.6f}s, FlotCoûtMin = {mcf_time:.6f}s")
        print("-" * 50)


if __name__ == "__main__":
    analyser_complexite()
