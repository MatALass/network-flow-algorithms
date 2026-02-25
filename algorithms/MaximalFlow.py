import os
from collections import deque
import sys
import io
def create_capacity_matrix(file_path):
    base_dir = os.path.dirname(__file__)  # ProjetRechercheOp/algorithms
    root_dir = os.path.abspath(os.path.join(base_dir, ".."))  # ProjetRechercheOp/
    full_path = os.path.join(root_dir, file_path)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"File not found: {full_path}")
    
    with open(full_path, 'r') as file:
        lines = file.readlines()

    n = int(lines[0].strip())  # Read the size of the matrix
    matrix_lines = lines[1:1 + n]  # Extract only the next `n` lines

    capacity_graph = []
    for line in matrix_lines:
        row = list(map(int, line.strip().split()))
        if len(row) != n:
            raise ValueError(f"Invalid row length in adjacency matrix: {line.strip()}")
        capacity_graph.append(row)

    return capacity_graph
def display_capacity_matrix(capacity_matrix):
    print("Matrice de Capacité:")
    for row in capacity_matrix:
        print(row)
    print(f"\n")
def get_source_and_sink(capacity_matrix):
    n = len(capacity_matrix)
    source = 0
    sink = n - 1
    return source, sink

def bfs(residual_graph, source, sink):
    n = len(residual_graph)
    parent = [-1] * n
    visited = [False] * n
    queue = deque([source])
    visited[source] = True

    letters = ['s'] + [chr(ord('a') + i) for i in range(n - 2)] + ['t']

    print("Le parcours en largeur :")
    print(letters[source])  # Première ligne : juste "s"

    while queue:
        u = queue.popleft()

        newly_discovered = []

        for v in range(n):
            if not visited[v] and residual_graph[u][v] > 0:
                parent[v] = u
                visited[v] = True
                queue.append(v)
                newly_discovered.append(v)

                if v == sink:
                    # Affichage final quand on découvre t
                    line = ''.join(letters[x] for x in queue)
                    preds = [f"Π({letters[v]}) = {letters[u]}"]
                    print(f"{line} ; {'; '.join(preds)}")
                    return parent

        if newly_discovered:
            line = ''.join(letters[x] for x in queue)
            preds = [f"Π({letters[v]}) = {letters[parent[v]]}" for v in newly_discovered]
            print(f"{line} ; {'; '.join(preds)}")

    return None

def find_bottleneck_capacity(residual_graph, parent, source, sink):
    path_flow = float('Inf')
    v = sink
    while v != source:
        u = parent[v]
        path_flow = min(path_flow, residual_graph[u][v])
        v = u
    return path_flow

def update_residual_graph(residual_graph, parent, source, sink, path_flow):
    v = sink
    while v != source:
        u = parent[v]
        residual_graph[u][v] -= path_flow
        residual_graph[v][u] += path_flow
        v = u

def print_ford_fulkerson_info(iteration, path, path_flow, residual_graph, max_flow):
    print(f"\n")
    print(f"Iteration {iteration}:")
    print(f"Chaine ameliorante: {path} de flot {path_flow}")
    print(f"Modifications sur le graphe residuel:")

    letters = ['s'] + [chr(ord('a') + i) for i in range(len(residual_graph) - 2)] + ['t']
    print("   " + "  ".join(letters))

    for i in range(len(residual_graph)):
        letter = letters[i]
        print(f"{letter} {residual_graph[i]}")
    print(f"\n")




def ford_fulkerson(capacity_matrix, source, sink):
    n = len(capacity_matrix)
    residual_graph = [row[:] for row in capacity_matrix]
    max_flow = 0
    iteration = 1

    letters = ['s'] + [chr(ord('a') + i) for i in range(n - 2)] + ['t']

    while True:
        parent = bfs(residual_graph, source, sink)
        if not parent:
            break

        path_flow = find_bottleneck_capacity(residual_graph, parent, source, sink)

        # Construction du chemin (indices)
        path = []
        v = sink
        while v != source:
            path.append(v)
            v = parent[v]
        path.append(source)
        path.reverse()

        # Conversion en chaîne de lettres
        path_str = ''.join(letters[node] for node in path)

        update_residual_graph(residual_graph, parent, source, sink, path_flow)

        print_ford_fulkerson_info(iteration, path_str, path_flow, residual_graph, max_flow + path_flow)

        max_flow += path_flow
        iteration += 1

    return max_flow

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

def main_ford_fulkerson(numbertest):
    # Construct the correct path for the output file
    project_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current script's directory
    output_file = os.path.join(project_dir, 'tracefiles', 'K5-trace' + str(numbertest) + '-FF')  # Use os.path.join for portability

    # Ensure the 'tracefiles' directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:  # Open the file for writing
        original_stdout = sys.stdout  # Save the original stdout
        sys.stdout = Tee(file, original_stdout)  # Redirect stdout to both file and console

        try:
            # Execute your main logic
            capacity_matrix = create_capacity_matrix('/testfiles/test' + str(numbertest))
            display_capacity_matrix(capacity_matrix)
            source, sink = get_source_and_sink(capacity_matrix)
            max_flow = ford_fulkerson(capacity_matrix, source, sink)
            print(f"Flot maximal: {max_flow}")
        finally:
            # Restore the original stdout
            sys.stdout = original_stdout

    print(f"Les résultats ont été enregistrés dans le fichier '{output_file}'.")
