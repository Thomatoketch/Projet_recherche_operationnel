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
    m = int(dimension[0])
    n = int(dimension[1])

    # Initialiser la proposition de transport avec des zéros
    proposition = [[0] * m for _ in range(n)]

    # Variables pour suivre les index des lignes et colonnes
    i = 0
    j = 0

    while True:
        # Trouver la cellule la moins chère et la remplir autant que possible
        min_cout = float('inf')
        min_i = None
        min_j = None
        for i in range(n):
            for j in range(m):
                if provisions[i] > 0 and commandes[j] > 0:
                    cout = couts[i][j]
                    if cout < min_cout:
                        min_cout = cout
                        min_i = i
                        min_j = j
        if min_cout == float('inf'):
            break

        quantite = min(provisions[min_i], commandes[min_j])
        proposition[min_i][min_j] = quantite
        provisions[min_i] -= quantite
        commandes[min_j] -= quantite

    return proposition
