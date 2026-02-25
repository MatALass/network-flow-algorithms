import os

def create_capacity_matrix(file_name):
    project_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = project_dir + file_name
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r') as f:
        lines = f.readlines()

    n = int(lines[0].strip())
    matrix_lines = lines[1:1 + n]

    capacity_graph = []
    for line in matrix_lines:
        row = list(map(int, line.strip().split()))
        if len(row) != n:
            raise ValueError(f"Invalid row length in matrix: {line.strip()}")
        capacity_graph.append(row)

    return capacity_graph

def get_source_and_sink(capacity_matrix):
    n = len(capacity_matrix)
    return 0, n - 1

def push_relabel(capacity, source, sink):
    n = len(capacity)
    height = [0] * n
    excess = [0] * n
    flow = [[0] * n for _ in range(n)]

    letters = ['s'] + [chr(ord('a') + i) for i in range(n - 2)] + ['t']

    def push(u, v):
        delta = min(excess[u], capacity[u][v] - flow[u][v])
        if delta > 0 and height[u] == height[v] + 1:
            flow[u][v] += delta
            flow[v][u] -= delta
            excess[u] -= delta
            excess[v] += delta
            return True
        return False

    def relabel(u):
        min_height = float('inf')
        for v in range(n):
            if capacity[u][v] - flow[u][v] > 0:
                min_height = min(min_height, height[v])
        if min_height < float('inf'):
            height[u] = min_height + 1

    # Initialisation
    height[source] = n
    for v in range(n):
        if capacity[source][v] > 0:
            flow[source][v] = capacity[source][v]
            flow[v][source] = -flow[source][v]
            excess[v] = flow[source][v]
            excess[source] -= flow[source][v]

    active = [i for i in range(n) if i != source and i != sink and excess[i] > 0]

    while active:
        active.sort(key=lambda i: (-height[i], letters[i]))
        u = active.pop(0)

        while excess[u] > 0:
            pushed = False
            neighbors = [sink] + sorted(
                [v for v in range(n) if v != sink and capacity[u][v] - flow[u][v] > 0],
                key=lambda x: letters[x]
            )
            for v in neighbors:
                if push(u, v):
                    if v != source and v != sink and v not in active and excess[v] > 0:
                        active.append(v)
                    pushed = True
                    break
            if not pushed:
                relabel(u)

        if excess[u] > 0 and u not in active:
            active.append(u)

    return sum(flow[source][i] for i in range(n))

import os
import sys

class Tee:
    def __init__(self, file, console):
        self.file = file
        self.console = console

    def write(self, data):
        self.file.write(data)
        self.console.write(data)

    def flush(self):
        self.file.flush()
        self.console.flush()

def main_push_relabel(numbertest):
    # Construct the output file path
    project_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(project_dir, 'tracefiles', f'K5-trace{numbertest}-PR')

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        original_stdout = sys.stdout
        sys.stdout = Tee(file, original_stdout)

        try:
            capacity_matrix = create_capacity_matrix(f'/testfiles/test{numbertest}')
            source, sink = get_source_and_sink(capacity_matrix)
            max_flow = push_relabel(capacity_matrix, source, sink)
        finally:
            sys.stdout = original_stdout

    print(f"Les résultats ont été enregistrés dans le fichier '{output_file}'.")
