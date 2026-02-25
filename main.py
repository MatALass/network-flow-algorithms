import algorithms.MaximalFlow as MaximalFlow
import algorithms.MinimalCost as MinimalCost
import algorithms.pushRelabel as pushRelabel
import GUI

def main():
    while True:
        print("\nChoisissez une option:")
        print("ff - Calculer Ford-Fulkerson")
        print("cm - Calculer Coût Minimal (non implémenté)")
        print("pr - Calculer Pousser-Réétiqueter (non implémenté)")
        print("gui - Lancer l'interface graphique")
        print("0 - Quitter le programme")

        choice = input("Entrez votre choix (ff, cm, pr, gui, 0): ").strip().lower()

        if choice == "0":
            print("Programme terminé.")
            break
        elif choice == "gui":
            print("Lancement de l'interface graphique...")
            GUI.root.mainloop()
            break
        elif choice not in {"ff", "cm", "pr"}:
            print("Choix invalide. Veuillez réessayer.")
            continue

        try:
            number = int(input("Entrez un nombre entre 1 et 10: ").strip())
            if number < 1 or number > 10:
                print("Le nombre doit être entre 1 et 10. Veuillez réessayer.")
                continue
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre entier.")
            continue

        if choice == "ff":
            MaximalFlow.main_ford_fulkerson(number)
        elif choice == "cm":
            print("Coût Minimal n'est pas encore implémenté.")
        elif choice == "pr":
            pushRelabel.main_(number)

if __name__ == '__main__':
    main()