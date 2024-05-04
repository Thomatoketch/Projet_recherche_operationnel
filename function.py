import tabulate
import sys
MAX = 500000000000000

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
        


def verification_cycle(proposition):
    m = len(proposition[0])  # Nombre de colonnes
    n = len(proposition)     # Nombre de lignes

    def dfs(i, j, visited, parent):
        visited[i][j] = True
        neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
        for ni, nj in neighbors:
            if 0 <= ni < n and 0 <= nj < m and not visited[ni][nj] and proposition[ni][nj] > 0:
                if dfs(ni, nj, visited, (i, j)):
                    return True
            elif 0 <= ni < n and 0 <= nj < m and visited[ni][nj] and (ni, nj) != parent:
                return True
        return False

    visited = [[False] * m for _ in range(n)]

    # Commencez la recherche en profondeur à partir de chaque cellule non affectée
    for i in range(n):
        for j in range(m):
            if proposition[i][j] > 0 and not visited[i][j]:
                if dfs(i, j, visited, (-1, -1)):
                    return True

    return False



def verification_non_degenere(proposition) :
    if verification_arretes_sommets(proposition) and verification_cycle(proposition) == 0 : 
        print("La proposition est non-degenere")
        return 0
    else :
        if verification_arretes_sommets(proposition) == 0 :
            print("La proposition est degenere car le nombre d'arrete est different du nombre de sommet-1")
            return 1
        if verification_cycle(proposition):
            print("La proposition est degene car il y a un cycle")
            return 2



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
    for i in range(len(dico)):
        minimum = min(dico, key=lambda k: dico[k])
        matrice_cycle[minimum[0]][minimum[-1]] = 1
        if verification_cycle(matrice_cycle) :
            print("creer un cycle")
            dico.pop(minimum)
        else :
            print("ne creer pas de cycle")
            for i in range(n):
                for j in range(m):
                    if matrice_cycle[i][j] == 1 and proposition[i][j] == 0 :
                        return minimum, (i,j)



def calcul_des_potentiels(couts, matrice_arrete):
    m = len(matrice_arrete[0])  # Nombre de colonnes
    n = len(matrice_arrete)     # Nombre de lignes
    
    # Définition des listes ligne et colonne avec maxsize pour la vérification de colonne non modifiée
    potentiels_lignes = [-MAX] * n
    potentiels_colonnes = [-MAX] * m
    k=0


    # Définition de S1 à 0
    potentiels_lignes[0] = 0
    # Calcul des coûts
    while -MAX in potentiels_lignes or -MAX in potentiels_colonnes :
        print(potentiels_lignes)
        print(potentiels_colonnes)
        for i in range(n):
            for j in range(m):
                if matrice_arrete[i][j] != 0:

                    if potentiels_lignes[i] == -MAX and potentiels_colonnes[j] != -MAX:
                        potentiels_lignes[i] = couts[i][j] + potentiels_colonnes[j]
                    elif potentiels_colonnes[j] == -MAX and potentiels_lignes[i] != -MAX:
                        potentiels_colonnes[j] = potentiels_lignes[i] - couts[i][j]
    return potentiels_lignes, potentiels_colonnes



def maximisation_transport(proposition, couts):
    while verification_cycle(proposition):
        print("Cycle détecté, maximisation en cours...")

        # Afficher les conditions pour chaque case
        # Parcourir la proposition de transport
        for i in range(len(proposition)):
            for j in range(len(proposition[0])):
                # Si la case est remplie
                if proposition[i][j] > 0:
                    print(f"Case [{i}, {j}] - {proposition[i][j]} unités")
                    # Vous pouvez ajouter des informations supplémentaires ici, comme les coûts, etc.

        # Afficher les arêtes supprimées à l'issue de la maximisation
        arêtes_supprimées = []
        while verification_cycle(proposition):
            point_cycle, matrice_cycle = choix_point_cycle(proposition, couts)
            arêtes_supprimées.append(point_cycle)
            proposition[point_cycle[0]][point_cycle[1]] = 0
            print(f"Arête supprimée : {point_cycle}")

        print("Maximisation terminée.\n")

    print("Pas de cycle détecté, la proposition est optimale.")
    return proposition



def trouver_cycle(proposition, start_i, start_j):
    m = len(proposition[0])  # Nombre de colonnes
    n = len(proposition)  # Nombre de lignes

    visited = [[False] * m for _ in range(n)]
    cycle = []

    def dfs(i, j, parent_i, parent_j):
        if visited[i][j]:
            return True
        visited[i][j] = True

        neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
        for ni, nj in neighbors:
            if 0 <= ni < n and 0 <= nj < m and (ni != parent_i or nj != parent_j) and proposition[ni][nj] > 0:
                if dfs(ni, nj, i, j):
                    cycle.append((ni, nj))
                    return True
        return False

    if dfs(start_i, start_j, -1, -1):
        cycle.append((start_i, start_j))
        return cycle
    else:
        return []



def calcul_matrice_couts_potentiels(ligne_potentiel, colonne_potentiels):
    matrice_potentiels = []
    for ligne in ligne_potentiel:
        temp = []
        for colonne in colonne_potentiels :
            temp.append(int(ligne) - int(colonne))
        matrice_potentiels.append(temp)
    return matrice_potentiels



def calcul_matrice_couts_marginaux(matrice_potentiels, matrice_couts):
    n = len(matrice_couts)
    m = len(matrice_couts[0])
    matrice_marginaux = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            matrice_marginaux[i][j] = matrice_couts[i][j] - matrice_potentiels[i][j]
    return matrice_marginaux



def arrete_ameliorante(matrice_marginaux):
    n = len(matrice_marginaux)
    m = len(matrice_marginaux[0])
    index = 0
    minimum = sys.maxsize
    for i in range(n) :
        for j in range(m):
            if matrice_marginaux[i][j] < minimum :
                minimum = matrice_marginaux[i][j]
                index = (i,j)
    return minimum, index



def clone_matrice(matrice):
    clone = []
    for ligne in matrice:
        nouvelle_ligne = []
        for valeur in ligne:
            if valeur != 0:
                nouvelle_ligne.append(1)
            else:
                nouvelle_ligne.append(0)
        clone.append(nouvelle_ligne)
    return clone