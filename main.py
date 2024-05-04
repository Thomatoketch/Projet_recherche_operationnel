from pprint import pprint
import tabulate
from function import *

numero_fichier = "1"
restart = ""

while restart != "exit" :
    numero_fichier = input("Bonjour, veuillez donner le numero du fichier à executé : ")

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


    print("Que voulez vous faire : \n \t1. Matrice des coûts \n \t2. proposition de transport\n \t3. table des couts potentiels\n \t4. table des couts marginaux")
    restart = input()
    match restart :
        # Matrice des couts
        case "1" :
            print("Voici la matrice des coûts : ")
            print(tabulate.tabulate(matrice_couts, tablefmt="rounded_grid"))

        # Proposition de transport
        case "2" :
            proposition_transport = balas_hammer(dimension, provisions, commandes, matrice_couts)
            if verification_non_degenere(proposition_transport) == False:
                print(choix_point_cycle(proposition_transport, matrice_couts))
                

        # Table des coûts potentiels
        case "3" :
            "dzad"
            # Exemple d'utilisation
            proposition_transport = balas_hammer(dimension, provisions, commandes, matrice_couts)
            degenere = verification_non_degenere(proposition_transport)
            matrice_arrete_ajoute = clone_matrice(proposition_transport)


            while degenere != 0 :
                if degenere == 1:
                    cout_arrete, arrete_non_degenere = choix_point_cycle(matrice_arrete_ajoute, matrice_couts)
                    matrice_arrete_ajoute[arrete_non_degenere[0]][arrete_non_degenere[1]] = 1
                else :
                    proposition_transport = maximisation_transport(proposition_transport)
                degenere = verification_non_degenere(matrice_arrete_ajoute)


            potentiels_lignes, potentiels_colonnes = calcul_des_potentiels(matrice_couts, matrice_arrete_ajoute)

            print("Ligne des coûts potentiels : ", potentiels_lignes)
            print("Colonne des coûts potentiels : ", potentiels_colonnes)

            matrice_potentiels = calcul_matrice_couts_potentiels(potentiels_lignes, potentiels_colonnes)
            print(tabulate.tabulate(matrice_potentiels, tablefmt="rounded_grid"))

            matrice_marginaux = calcul_matrice_couts_marginaux(matrice_potentiels, matrice_couts)
            print(tabulate.tabulate(matrice_marginaux, tablefmt="rounded_grid"))

            minimum, arrete = arrete_ameliorante(matrice_marginaux)
            if minimum >= 0:
                print(
                    "Il n'y a pas d'arrete améliorante car toutes les valeurs de la matrice des couts marginaux sont positives")
            else:
                print(f"l'arrete la plus améliorante est : {arrete} avec un valeur de {minimum}")

            

        # Table des coûts marginaux
        case "4" :
            "dzad"
            proposition_transport = [
                [30, 10, 20, 0],  # Ligne 1
                [0, 20, 30, 0],  # Ligne 2
                [10, 0, 0, 20]  # Ligne 3
            ]
            matrice_couts = [
                [10, 20, 30, 40],  # Ligne 1
                [50, 60, 70, 80],  # Ligne 2
                [90, 100, 110, 120]  # Ligne 3
            ]
            potentiels_lignes, potentiels_colonnes = calcul_des_potentiels(proposition_transport, matrice_couts)

            print("Ligne des coûts potentiels : ", potentiels_lignes)
            print("Colonne des coûts potentiels : ", potentiels_colonnes)

            matrice_potentiels = calcul_matrice_couts_potentiels(potentiels_lignes,potentiels_colonnes)
            print(tabulate.tabulate(matrice_potentiels, tablefmt="rounded_grid"))

            matrice_marginaux = calcul_matrice_couts_marginaux(matrice_potentiels, matrice_couts)
            print(tabulate.tabulate(matrice_marginaux, tablefmt="rounded_grid"))

            minimum, arrete = arrete_ameliorante(matrice_marginaux)
            if minimum >= 0: print("Il n'y a pas d'arrete améliorante car toutes les valeurs de la matrice des couts marginaux sont positives")
            else : print(f"l'arrete la plus améliorante est : {arrete} avec un valeur de {minimum}")
    break