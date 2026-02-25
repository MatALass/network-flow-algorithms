import io
import tkinter as tk
from tkinter import ttk, messagebox
import algorithms.MaximalFlow as MaximalFlow
import algorithms.MinimalCost as MinimalCost
import algorithms.pushRelabel as pushRelabel
import os
import sys


def create_gui():
    root = tk.Tk()
    root.title("Calculateur d'Algorithmes")
    root.state("zoomed")  # Full-screen mode

    # Paned window for compartments
    paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashwidth=5, bg="#d9d9d9")
    paned_window.pack(fill="both", expand=True)

    # Left frame for inputs and controls
    left_frame = tk.Frame(paned_window, bg="#f0f0f0", padx=20, pady=20)
    paned_window.add(left_frame, minsize=300)

    # Right frame for results
    right_frame = tk.Frame(paned_window, bg="#ffffff", padx=20, pady=20)
    paned_window.add(right_frame)

    # Title
    title_label = tk.Label(left_frame, text="Calculateur d'Algorithmes", font=("Arial", 20, "bold"), bg="#f0f0f0")
    title_label.pack(pady=10)

    # Algorithm selection
    algorithm_label = tk.Label(left_frame, text="Choisissez un algorithme:", font=("Arial", 14), bg="#f0f0f0")
    algorithm_label.pack(anchor="w", pady=5)

    algorithm_var = tk.StringVar()
    algorithm_dropdown = ttk.Combobox(left_frame, textvariable=algorithm_var, state="readonly", font=("Arial", 12))
    algorithm_dropdown['values'] = ("Ford-Fulkerson", "Coût Minimal", "Pousser-Réétiqueter")
    algorithm_dropdown.pack(fill="x", pady=5)

    # Number input
    number_label = tk.Label(left_frame, text="Entrez un nombre:", font=("Arial", 14), bg="#f0f0f0")
    number_label.pack(anchor="w", pady=5)

    number_var = tk.StringVar()
    number_entry = tk.Entry(left_frame, textvariable=number_var, font=("Arial", 12))
    number_entry.pack(fill="x", pady=5)

    # Desired flow input (for "Coût Minimal")
    flow_label = tk.Label(left_frame, text="Entrez le flot désiré:", font=("Arial", 14), bg="#f0f0f0")
    flow_label.pack(anchor="w", pady=5)
    flow_label.pack_forget()

    flow_var = tk.StringVar()
    flow_entry = tk.Entry(left_frame, textvariable=flow_var, font=("Arial", 12), state="disabled")
    flow_entry.pack(fill="x", pady=5)
    flow_entry.pack_forget()

    # Button for minimal cost calculation
    calculate_button = tk.Button(left_frame, text="Calculer Coût Minimal", font=("Arial", 12), bg="#2196F3", fg="white", padx=10, pady=5)
    calculate_button.pack(fill="x", pady=10)
    calculate_button.pack_forget()

    # Results section
    results_label = tk.Label(right_frame, text="Résultats:", font=("Arial", 16, "bold"), bg="#ffffff")
    results_label.pack(anchor="w", pady=10)

    results_text = tk.Text(right_frame, font=("Courier New", 12), wrap="word", padx=10, pady=10, bg="#f9f9f9", relief="solid", borderwidth=1)
    results_text.pack(fill="both", expand=True)

    # Store the original stdout
    original_stdout = sys.stdout

    def redirect_output_to_results():
        """Redirect stdout to the results_text widget."""
        class TextRedirector:
            def __init__(self, widget):
                self.widget = widget

            def write(self, string):
                if self.widget.winfo_exists():  # Ensure the widget still exists
                    self.widget.insert(tk.END, string)
                    self.widget.see(tk.END)  # Auto-scroll to the end

            def flush(self):
                pass

        sys.stdout = TextRedirector(results_text)

    def quit_program():
        """Quit the program and restore stdout."""
        sys.stdout = original_stdout  # Restore the original stdout
        root.destroy()  # Close the GUI

    def execute_algorithm():
        """Execute the selected algorithm."""
        algorithm = algorithm_var.get()
        number = number_var.get()

        if algorithm not in {"Ford-Fulkerson", "Coût Minimal", "Pousser-Réétiqueter"}:
            messagebox.showerror("Erreur", "Veuillez sélectionner un algorithme valide.")
            return

        try:
            number = int(number)
            if algorithm in {"Ford-Fulkerson", "Pousser-Réétiqueter"} and not (1 <= number <= 10):
                raise ValueError("Le nombre doit être entre 1 et 10.")
            if algorithm == "Coût Minimal" and not (6 <= number <= 10):
                raise ValueError("Le nombre doit être entre 6 et 10.")
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            return

        results_text.delete(1.0, tk.END)
        redirect_output_to_results()

        if algorithm == "Ford-Fulkerson":
            MaximalFlow.main_ford_fulkerson(number)
        elif algorithm == "Pousser-Réétiqueter":
            pushRelabel.main_push_relabel(number)
        elif algorithm == "Coût Minimal":
            try:
                cap = MaximalFlow.create_capacity_matrix(f'/testfiles/test{number}')
                cost = MinimalCost.create_cost_matrix(f'/testfiles/test{number}')
                source, sink = MinimalCost.get_source_and_sink(cost)

                # Display matrices and source/sink
                MaximalFlow.display_capacity_matrix(cap)
                MinimalCost.display_cost_matrix(cost)
                print(f"Source={source}, Sink={sink}\n")

                # Calculate max flow
                max_flow = MaximalFlow.ford_fulkerson([row[:] for row in cap], source, sink)
                print(f"Flot max possible = {max_flow}\n")

                # Enable flow input and show the calculate button
                flow_label.config(text=f"Entrez le flot désiré (1..{max_flow}):")
                flow_label.pack()
                flow_entry.config(state="normal")
                flow_entry.pack()
                flow_entry.max_flow = max_flow
                flow_entry.cap = cap
                flow_entry.cost = cost
                flow_entry.source = source
                flow_entry.sink = sink
                calculate_button.config(command=calculate_minimal_cost)
                calculate_button.pack()

            except FileNotFoundError:
                messagebox.showerror("Erreur", "Fichier de test introuvable.")

    def calculate_minimal_cost():
        """Calculate the minimal cost for the desired flow."""
        try:
            desired_flow = int(flow_var.get())
            max_flow = flow_entry.max_flow

            if desired_flow < 1 or desired_flow > max_flow:
                raise ValueError(f"Le flot doit être entre 1 et {max_flow}.")

            # Perform the minimal cost calculation
            cap = flow_entry.cap
            cost = flow_entry.cost
            source = flow_entry.source
            sink = flow_entry.sink

            fv, tc, Fmat = MinimalCost.minimal_cost_flow(cap, cost, source, sink, desired_flow)

            print(f"\n=== Résultat final ===")
            print(f"Flot total obtenu = {fv}")
            print(f"Coût total minimal = {tc}\n")
            print("Flux arc (f/c; coût_unitaire):")
            n = len(cap)
            for u in range(n):
                for v in range(n):
                    if cap[u][v] > 0:
                        print(f" {u}->{v}: ({Fmat[u][v]}/{cap[u][v]}; {cost[u][v]})")

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    execute_button = tk.Button(left_frame, text="Exécuter", command=execute_algorithm, font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
    execute_button.pack(fill="x", pady=10)

    quit_button = tk.Button(left_frame, text="Quitter", command=quit_program, font=("Arial", 12), bg="#f44336", fg="white", padx=10, pady=5)
    quit_button.pack(fill="x", pady=5)

    return root