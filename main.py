from pprint import pprint
import tabulate
from function import *

restart = ""

while restart != "exit" :
    numero_fichier = None
    while numero_fichier is None:
        entree = input("Bonjour, veuillez donner le numero du fichier à executé : ")
        if entree.isdigit():  # Vérifie si l'entrée est constituée uniquement de chiffres
            if 0 < int(entree) <= 12:
                numero_fichier = entree
            else : print("entrez une valeur entre 1 et 12")
        else:
            print("Erreur : Veuillez entrer un entier valide.")

    fichier = "./fichier_test/tableau_"+numero_fichier+".txt"

    with open(fichier, 'r') as fichier:
        lignes = fichier.readlines()

    # Lire les dimensions de la matrice
    dimension = list(map(int, lignes[0].split()))

    # Lire les données de la matrice
    matrice = [list(map(int, ligne.split())) for ligne in lignes[1:]]

    # Séparer la matrice en proposition, provisions, commandes et matrice des coûts
    matrice_couts = [ligne[:-1] for ligne in matrice[:-1]]
    provisions = [ligne[-1] for ligne in matrice[:-1]]
    commandes = matrice[-1]


    print("Que voulez vous faire : \n \t1. Matrice des coûts \n \t2. proposition de transport")
    restart = input()
    proposition_transport = []
    match restart :
        # Matrice des couts
        case "1" :
            print("Voici la matrice des coûts : ")
            print(tabulate.tabulate(matrice_couts, tablefmt="rounded_grid"))

        # Proposition de transport
        case "2" :
            print("Veillez choisir un algorithme pour fixer la proposition de transport: \n \t1. Nord-Ouest \n \t2. Balas-Hammer")
            choix = input()
            match choix :
                case "1":
                    proposition_transport = nord_ouest(provisions,commandes)
                case "2":
                    proposition_transport = balas_hammer(provisions,commandes,matrice_couts)
            couts_total(proposition_transport,matrice_couts)

            degenere = verification_non_degenere(proposition_transport)
            matrice_arrete_ajoute = clone_matrice(proposition_transport)

            while degenere != 0:
                if degenere == 1:
                    cout_arrete, arrete_non_degenere = choix_point_cycle(matrice_arrete_ajoute, matrice_couts)
                    matrice_arrete_ajoute[arrete_non_degenere[0]][arrete_non_degenere[1]] = 1
                    print(f"L'arrete [{arrete_non_degenere[0]},{arrete_non_degenere[1]}] ne crée pas de cycle et est de poids minimum donc on l'ajoute à notre proposition.\n")
                else:
                    proposition_transport = maximisation_transport(proposition_transport)
                degenere = verification_non_degenere(matrice_arrete_ajoute)

            print("Voici une matrice qui represente les arretes faisant parti de notre nouvelle proposition non-degenere")
            print(tabulate.tabulate(matrice_arrete_ajoute, tablefmt="rounded_grid"))
            print()

            potentiels_lignes, potentiels_colonnes = calcul_des_potentiels(matrice_couts, matrice_arrete_ajoute)

            print(f"Ligne des coûts potentiels : {potentiels_lignes}")
            print(f"Colonne des coûts potentiels : {potentiels_colonnes}\n")

            matrice_potentiels = calcul_matrice_couts_potentiels(potentiels_lignes, potentiels_colonnes)
            print("--Matrice des couts potentiels :--")
            print(tabulate.tabulate(matrice_potentiels, tablefmt="rounded_grid"))

            matrice_marginaux = calcul_matrice_couts_marginaux(matrice_potentiels, matrice_couts)
            print("--Matrice des couts marginaux :--")
            print(tabulate.tabulate(matrice_marginaux, tablefmt="rounded_grid"))

            minimum, arrete = arrete_ameliorante(matrice_marginaux)
            if minimum >= 0:
                print(
                    "Il n'y a pas d'arrete améliorante car toutes les valeurs de la matrice des couts marginaux sont positives")
            else:
                print(f"l'arrete la plus améliorante est : {arrete} avec un valeur de {minimum}")

    print("\n")