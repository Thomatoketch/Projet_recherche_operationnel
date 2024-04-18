from pprint import pprint
import tabulate
from function import *



numero_fichier = input("Bonjour, veuillez donner le numero du fichier à executé : ")

fichier = "./fichier_test/tableau_"+numero_fichier+".txt"

with open(fichier, 'r') as f:
    lines = f.readlines()
    dimensions = lines[0].split(" ")
    # Diviser la chaîne en lignes
    lignes = lines[1:]

matrice = []
for ligne in lignes:
    elements = ligne.split()
    ligne_matrice = [int(element) for element in elements]
    matrice.append(ligne_matrice)


liste_provisions= []
for ligne in matrice[:-1]:
    liste_provisions.append(ligne[-1])
liste_commandes = [int(element) for element in lines[-1].split()]



print("Que voulez vous faire : \n \t1. Matrice des coûts \n \t2. proposition de transport\n \t3. table des couts potentiels\n \t4. table des couts margianux")
match input() :
    # Matrice des couts
    case "1" :
        print("Voici la matrice des coûts : ")
        print(tabulate.tabulate(matrice, tablefmt="rounded_grid"))

    # Proposition de transport
    case "2" :
        print(tabulate.tabulate(balas_hammer(dimensions, liste_provisions, liste_commandes, matrice), tablefmt="rounded_grid"))

    # Table des coûts potentiels
    case "3" :
        "dza"

    # Table des coûts marginaux
    case "4" :
        "dzad"







