# Fichier : operations.py
# Nom : Opérations Mathématiques
# Auteurs : Hugo PANEL, Mohamed ZAMMIT CHATTI
# Description :
"""
Ce fichier regroupe les fonctions utilisées pour effectuer les opérations mathématiques de la transposition et de
l'inversion sur des partitions.
"""


def transposition(score, k, interval=(0, 6)):
    """Applique la transposition sur une partition (sous forme d'index).
    Paramètres :
        list[int]: score : La partition à transposer. La partition doit être une liste.
        int: k : La valeur à ajouter à chaque note
        tuple(int, int): interval=(0, 6) : L'intervalle dans lequel les notes finales sont comprises.
    Retourne :
        list[int]: res : La partition transposée (sous forme d'entiers)."""
    res = []  # Liste dans laquelle on va stocker la partition transposée.
    sup = interval[1] - interval[0]

    # Pour chaque note dans la partition :
    for note in score:
        note = (note + k) % (sup + 1)  # On applique la transposition
        res.append(note + interval[0])
    return res  # On retourne la partition transposée


def inversion(score, interval=(0, 6)):
    """Applique l'inversion sur une partition (sous forme d'index).
    Paramètres :
        list[int]: score : La partition à inverser. La partition doit être une liste.
        tuple(int, int): interval=(0, 6) : L'intervalle dans lequel les notes finales sont comprises.
    Retourne :
        list[int]: res : La partition inversée sous forme de liste d'index."""
    res = []
    sup = interval[1] - interval[0]

    for note in score:
        note = (sup + 1 - note) % (sup + 1)
        res.append(note + interval[0])
    return res
