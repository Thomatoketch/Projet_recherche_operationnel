import numpy as np
import random


def generer_probleme_transport(n):
    # Générer les coûts de transport aléatoires entre 1 et 100 inclus
    couts_transport = np.random.randint(1, 101, size=(n, n))

    provisions = np.random.randint(1, 101, size=n)
    commandes = np.random.randint(1, 101, size=n)

    demande_totale = np.sum(commandes)
    fourniture_totale = np.sum(provisions)

    while demande_totale != fourniture_totale:
        # Si la somme des demandes est plus grande, on réduit une demande aléatoire
        if demande_totale > fourniture_totale:
            index = np.random.randint(0, n)
            if commandes[index] > 1:
                commandes[index] -= 1
                demande_totale -= 1
        # Si la somme des fournitures est plus grande, on réduit une provision aléatoire
        else:
            index = np.random.randint(0, n)
            if provisions[index] > 1:
                provisions[index] -= 1
                fourniture_totale -= 1

    return couts_transport, provisions, commandes