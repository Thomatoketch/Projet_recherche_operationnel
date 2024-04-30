import tabulate
import sys
from collections import deque

def nord_ouest(dimension, provisions, commandes):
    m = int(dimension[0])
    n = int(dimension[1])

    # Initialiser la proposition de transport avec des zéros
    proposition = [[0] * m for _ in range(n)]

    # Variables pour suivre les index des lignes et colonnes
    i = 0
    j = 0

    # Remplir la proposition de transport selon l'algorithme Nord-Ouest
    while i < n and j < m:
        quantite = min(provisions[i], commandes[j])
        proposition[i][j] = quantite
        provisions[i] -= quantite
        commandes[j] -= quantite
        if provisions[i] == 0:
            i += 1
        if commandes[j] == 0:
            j += 1

    return proposition



def balas_hammer(dimension, provisions, commandes, couts):
    m = int(dimension[1])
    n = int(dimension[0])
    temp =[]
    
    # Initialiser la proposition de transport avec des zéros
    proposition = [[0] * m for _ in range(n)]
    matrice_rempli = [[0] * m for _ in range(n)]

    # Variables pour suivre les index des lignes et colonnes
    i = 0
    j = 0

    while True:
        choix_penalité = {}
        penalites_lignes, penalites_colonnes, penalite_max, penalites_multiples = calculer_penalites_balas_hammer(couts, provisions, commandes, matrice_rempli)
        print("Pénalités par ligne :", penalites_lignes)
        print("Pénalités par colonne :", penalites_colonnes)
        print("Pénalité maximale :", penalite_max)
        print("Indices des pénalités maximales multiples :", penalites_multiples)
        
        if len(penalites_multiples) > 1:
            for ligne in penalites_multiples :
                temp = []
                if ligne < n :
                    for i in range(m):
                        if matrice_rempli[ligne][i] == 0 :
                            temp.append(couts[ligne][i])
                        else :
                            temp.append(sys.maxsize)
                    min_cout = min(temp)
                    min_i = ligne
                    min_j = temp.index(min_cout)
                else :
                    for j in range(n):
                        if matrice_rempli[j][ligne-n] == 0 :
                            temp.append(couts[j][ligne-n])
                        else :
                            temp.append(sys.maxsize)
                    min_cout = min(temp)
                    min_i = temp.index(min_cout)
                    min_j = ligne-n

                quantite = min(provisions[min_i], commandes[min_j])
                choix_penalité[ligne] = [min_i,min_j,quantite]
            min_i = choix_penalité[max(choix_penalité, key=lambda k: choix_penalité[k][2])][0]
            min_j = choix_penalité[max(choix_penalité, key=lambda k: choix_penalité[k][2])][1] 
        
        else :    
            if penalites_multiples[0] < n :
                n= penalites_multiples[0]
                for i in range(m):
                    if matrice_rempli[n][i] == 0 :
                        temp.append(couts[n][i])
                    else :
                        temp.append(sys.maxsize)
                min_cout = min(temp)
                min_i = n
                min_j = temp.index(min_cout)
            else :
                m= penalites_multiples[0]-n
                for j in range(n):
                    if matrice_rempli[j][m] == 0 :
                        temp.append(couts[j][m])
                    else :
                        temp.append(sys.maxsize)
                min_cout = min(temp)
                min_i = temp.index(min_cout)
                min_j = m

        m = int(dimension[1])
        n = int(dimension[0])
        temp = []
        matrice_rempli[min_i][min_j] = 1
        quantite = min(provisions[min_i], commandes[min_j])
        proposition[min_i][min_j] = quantite
        provisions[min_i] -= quantite
        commandes[min_j] -= quantite
        
        if provisions[min_i] == 0 :
            matrice_rempli[min_i] = [1]*m
        if commandes[min_j] == 0 :
            for i in range(n) :
                matrice_rempli[i][min_j] = 1
        
        for i in range(n):
            if len([i for i, penalite in enumerate(matrice_rempli[i]) if penalite == 1]) == m-1:
                j = matrice_rempli[i].index(0)
                quantite = min(provisions[i], commandes[j])
                proposition[i][j] = quantite
                provisions[i] -= quantite
                commandes[j] -= quantite
                matrice_rempli[i][j] = 1
                
        for j in range(m):
            ligne = 0
            nombre_occurrences = 0
            for ligne in matrice_rempli:
                if j < len(ligne):  # Vérifier si la colonne existe dans la ligne
                    if ligne[j] == 1:
                            nombre_occurrences += 1
            if nombre_occurrences == n-1 :
                quantite = min(provisions[i], commandes[j])
                proposition[i][j] = quantite
                provisions[i] -= quantite
                commandes[j] -= quantite
                matrice_rempli[i][j] = 1
        
                
        #print(tabulate.tabulate(matrice_rempli, tablefmt="rounded_grid"))
        print(tabulate.tabulate(proposition, tablefmt="rounded_grid"))
        print("\n\n\n")
        
        if (matrice_rempli == [[1] * m for _ in range(n)] or (provisions == [[0] for _ in range(n)] and commandes == [[0] for _ in range(m)])):
            return proposition


    
def calculer_penalites_balas_hammer(proposition, provisions, commandes, matrice_rempli):
    m = len(commandes)
    n = len(provisions)
    couts = [ligne[:] for ligne in proposition]
    penalites_lignes = []
    penalites_colonnes = []

    # Calcul des pénalités par ligne et par colonne
    for i in range(n):
        penalites_temp = []
        for j in range(m):
            if matrice_rempli[i][j] == 0 :
                penalites_temp.append(couts[i][j])
        if len(penalites_temp) <= 1 : 
            penalites_lignes.append(0)
            continue
        penalites_ligne = min(penalites_temp)
        penalites_temp.remove(penalites_ligne)
        penalites_ligne = min(penalites_temp)- penalites_ligne
        penalites_lignes.append(penalites_ligne)
    
    
    couts = [ligne[:] for ligne in proposition]
    for i in range(m):
        penalites_temp = []
        for j in range(n):
            if matrice_rempli[j][i] == 0 :
                penalites_temp.append(couts[j][i])
        if len(penalites_temp) <= 1 : 
            penalites_colonnes.append(0)
            continue
        penalites_colonne = min(penalites_temp)
        penalites_temp.remove(penalites_colonne)
        penalites_colonne = min(penalites_temp)- penalites_colonne
        penalites_colonnes.append(penalites_colonne)

    # Trouver la plus grande pénalité
    penalite_max = max(penalites_lignes + penalites_colonnes)

    # Vérifier si la plus grande pénalité est présente plusieurs fois
    penalites_multiples = [i for i, penalite in enumerate(penalites_lignes) if penalite == penalite_max] + \
                          [j + n for j, penalite in enumerate(penalites_colonnes) if penalite == penalite_max]

    return penalites_lignes, penalites_colonnes, penalite_max, penalites_multiples



def verification_arretes_sommets(proposition):
    m = len(proposition[0])  # Nombre de colonnes
    n = len(proposition)     # Nombre de lignes
    compteur = 0
    lien = {}
    for ligne in proposition:
        for case in ligne:
            if (case != 0):
                compteur += 1
    if compteur == n + m - 1 :
        return True
    return False


def parcours_largeur(graphe, sommet):
    if not(sommet in graphe.keys()):
        return None
    F = [sommet]
    liste_sommets = []
    while len(F) != 0:
        S = F[0]
        for voisin in graphe[S]:
            if not(voisin in liste_sommets) and not(voisin in F):
                F.append(voisin)
        liste_sommets.append(F.pop(0))
    return liste_sommets

def matrice_vers_dictionnaire_graphe(matrice):
    graphe = {}
    n = len(matrice)

    # Ajout des successeurs des lignes
    for i in range(n):
        cle_ligne = "S" + str(i + 1)
        voisins_ligne = []
        for j in range(n):
            if matrice[i][j] > 0:
                voisins_ligne.append("C" + str(j + 1))
        graphe[cle_ligne] = tuple(voisins_ligne)

    # Ajout des successeurs des colonnes
    for j in range(n):
        cle_colonne = "C" + str(j + 1)
        voisins_colonne = []
        for i in range(n):
            if matrice[i][j] > 0:
                voisins_colonne.append("S" + str(i + 1))
        graphe[cle_colonne] = tuple(voisins_colonne)

    return graphe

def detecter_cycle(graphe, sommet):
    if sommet not in graphe.keys():
        return None

    F = [(sommet, None)]  # Chaque élément de la file F est un tuple (sommet, parent)
    liste_sommets = set()  # Utiliser un ensemble pour une recherche plus rapide
    parents = {sommet: None}  # Initialiser avec le sommet de départ comme clé

    # Initialiser le dictionnaire des parents avec toutes les clés possibles du graphe
    for sommet in graphe.keys():
        if sommet not in parents:
            parents[sommet] = None

    while F:
        S, parent = F.pop(0)
        liste_sommets.add(S)

        for voisin in graphe[S]:
            if voisin in parents and voisin != parent:  # Cycle détecté
                cycle = [voisin]
                parent_cycle = S
                while parent_cycle != voisin:
                    cycle.append(parent_cycle)
                    parent_cycle = parents[parent_cycle]
                cycle.append(voisin)
                return cycle
            if voisin not in liste_sommets:
                F.append((voisin, S))
                parents[voisin] = S

    return None


def verification_cycle(graphe):
    #appel de la fonction de parcours en largeur
    cycle = parcours_largeur(graphe, "S1")
    if cycle:
        print("Il existe un cycle dans la proposition:",cycle)
        return False  # La proposition n'est pas acyclique
    print("La proposition est acyclique.")
    return True  # La proposition est acyclique




def verification_non_degenere(proposition) :
    if verification_arretes_sommets(proposition) and verification_cycle(proposition) == 0 : 
        print("La proposition est non-degenere")
        return True
    else :
        if verification_arretes_sommets(proposition) == 0 :
            print("La proposition est degenere car le nombre d'arrete est different du nombre de sommet-1")
        if verification_cycle(proposition):
            print("La proposition est degene car il y a un cycle")
        return False



def choix_point_cycle(proposition, cout):
    m = len(proposition[0])  # Nombre de colonnes
    n = len(proposition)     # Nombre de lignes
    dico = {}
    matrice_cycle = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m) :
            matrice_cycle
            if proposition[i][j] == 0:
                dico[i,j] = cout[i][j]
            else :
                matrice_cycle[i][j] = 1
    print(dico)
    for i in range(len(dico)):
        minimum = min(dico, key=lambda k: dico[k])
        matrice_cycle[minimum[0]][minimum[-1]] = 1
        print(tabulate.tabulate(matrice_cycle, tablefmt="rounded_grid"))
        if verification_cycle(matrice_cycle) :
            print("creer un cycle")
            dico.pop(minimum)
        else :
            print("ne creer pas de cycle")
            return minimum, matrice_cycle
        
def calcul_potentiel(matrice_cycle, cout):
    m = len(cout[0])  # Nombre de colonnes
    n = len(cout)     # Nombre de lignes
    ligne_cout_potentiel = [0] * n
    colonne_cout_potentiel = [0] * m
    for i in range(n):
        temp = ligne_cout_potentiel[i]
        for j in range(m):
            if matrice_cycle[i][j] == 1:
                colonne_cout_potentiel