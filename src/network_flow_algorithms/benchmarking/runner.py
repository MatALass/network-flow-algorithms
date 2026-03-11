import time
import random
from algorithmsComplexity.MaximalFlow import ford_fulkerson
from algorithmsComplexity.MinimalCost import minimal_cost_flow
from algorithmsComplexity.pushRelabel import push_relabel

def generate_random_graph(n, density=0.3, capacity_range=(1, 20), cost_range=(1, 10)):
    capacity_matrix = [[0]*n for _ in range(n)]
    cost_matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and random.random() < density:
                cap = random.randint(*capacity_range)
                cost = random.randint(*cost_range)
                capacity_matrix[i][j] = cap
                cost_matrix[i][j] = cost
    return capacity_matrix, cost_matrix

def benchmark(n, runs=100):
    ff_times = []
    mc_times = []
    pr_times = []

    for i in range(runs):
        cap, cost = generate_random_graph(n)
        source, sink = 0, n - 1

        # Ford-Fulkerson
        cap_ff = [row[:] for row in cap]
        start = time.process_time()
        ford_fulkerson(cap_ff, source, sink)
        end = time.process_time()
        ff_times.append(end - start)
        print(f"Ford-Fulkerson time for run {i+1}: {ff_times[-1]:.6f}s")
        # Pousse-réétiqueter
        cap_pr = [row[:] for row in cap]
        start = time.process_time()
        push_relabel(cap_pr, source, sink)
        end = time.process_time()
        pr_times.append(end - start)
        print(f"Push-Relabel time for run {i+1}: {pr_times[-1]:.6f}s")
        # Flot à coût minimal
        cap_mc = [row[:] for row in cap]
        try:
            max_flow = ford_fulkerson([row[:] for row in cap], source, sink)
            start = time.process_time()
            minimal_cost_flow(cap_mc, cost, source, sink, required_flow=max_flow)
            end = time.process_time()
            mc_times.append(end - start)
        except:
            continue
        print(f"Minimal Cost time for run {i+1}: {mc_times[-1]:.6f}s")  
    return ff_times, pr_times, mc_times

def save_results(n, i, ff_times, pr_times, mc_times):
    with open("benchmarks/worst_case_summary.txt", "a") as f:
        f.write(f"n={n} | iteration {i}| FF worst-case: {max(ff_times):.6f}s | MC worst-case: {max(mc_times):.6f}s | PR worst-case: {max(pr_times):.6f}s\n")

def main():
    sizes = [10, 20, 40, 100, 400, 1000, 4000, 10000]
    for n in sizes:
        for i in range(100):
            print(f"Running benchmark for n = {n}")
            ff_times, pr_times, mc_times = benchmark(n)
            save_results(n, i, ff_times, pr_times, mc_times)

            print(f"  Ford-Fulkerson worst-case time: {max(ff_times):.6f}s")
            print(f"  Minimal Cost worst-case time:   {max(mc_times):.6f}s")
            print(f"  Push-Relabel worst-case time:   {max(pr_times):.6f}s")


if __name__ == "__main__":
    main()
