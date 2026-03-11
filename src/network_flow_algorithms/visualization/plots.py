import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Dictionnaires pour stocker les temps par itération pour chaque n
ff_data = {}
pr_data = {}
mc_data = {}

with open("worst_case_summary.txt", "r") as f:
    for line in f:
        try:
            if "FF worst-case:" in line:
                parts = line.strip().split('|')
                if len(parts) < 5:
                    continue

                n = int(parts[0].split('=')[1].strip())
                iteration = int(parts[1].split()[1])
                ff_time = float(parts[2].split(':')[1].strip()[:-1])
                mc_time = float(parts[3].split(':')[1].strip()[:-1])
                pr_time = float(parts[4].split(':')[1].strip()[:-1])

                ff_data.setdefault(n, []).append((iteration, ff_time))
                mc_data.setdefault(n, []).append((iteration, mc_time))
                pr_data.setdefault(n, []).append((iteration, pr_time))
        except (IndexError, ValueError):
            continue

# Listes pour stocker les valeurs maximales pour chaque n
n_values = []
max_ff = []
max_pr = []
max_mc = []

# Création d'un graphique par valeur de n avec 3 courbes
for n in sorted(ff_data.keys()):
    ff = sorted(ff_data[n])
    mc = sorted(mc_data[n])
    pr = sorted(pr_data[n])

    iterations_ff, times_ff = zip(*ff)
    iterations_mc, times_mc = zip(*mc)
    iterations_pr, times_pr = zip(*pr)

    # Enregistrement des valeurs maximales
    n_values.append(n)
    max_ff.append(max(times_ff))
    max_pr.append(max(times_pr))
    max_mc.append(max(times_mc))

    # Graphe individuel pour chaque n
    plt.figure(figsize=(10, 6))
    plt.plot(iterations_ff, times_ff, label="θFF(n)", color="blue", marker='o', linewidth=1)
    plt.plot(iterations_mc, times_mc, label="θMIN(n)", color="green", marker='s', linewidth=1)
    plt.plot(iterations_pr, times_pr, label="θPR(n)", color="red", marker='^', linewidth=1)

    plt.title(f"Évolution du temps d'exécution pour n = {n}")
    plt.xlabel("Itération")
    plt.ylabel("Temps d'exécution (s)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=4))
    plt.show()

# Graphe des valeurs maximales θFF et θPR selon n
plt.figure(figsize=(10, 6))
plt.plot(n_values, max_ff, label="Max θFF(n)", color="blue", marker='o')
plt.plot(n_values, max_pr, label="Max θPR(n)", color="red", marker='^')
plt.title("Comparaison des valeurs maximales de θFF(n) et θPR(n) selon n")
plt.xlabel("Taille du graphe n")
plt.ylabel("Temps d'exécution maximal (s)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=4))
plt.show()

# Graphe des enveloppes maximales θFF, θPR et θMIN selon n
plt.figure(figsize=(10, 6))
plt.plot(n_values, max_ff, label="Max θFF(n)", color="blue", marker='o')
plt.plot(n_values, max_pr, label="Max θPR(n)", color="red", marker='^')
plt.plot(n_values, max_mc, label="Max θMIN(n)", color="green", marker='s')
plt.title("Enveloppe maximale des temps d'exécution par algorithme")
plt.xlabel("Taille du graphe n")
plt.ylabel("Temps d'exécution maximal (s)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=4))
plt.show()
