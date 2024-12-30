# Fichier : markov.py
# Nom : Opérations de Markov
# Auteurs : Hugo PANEL, Mohamed ZAMMIT CHATTI
# Description :
"""
Ce fichier regroupe les fonctions utilisées pour générer des tableaux et des mélodies de Markov.
"""

import random
import notes as note_lib

def generateMarkovTable(score):
    """Génère un tableau de Markov à partir d'une partition.
    La partition doit être un string.
    Paramètres :
        str: partition : Partition sous forme de chaîne de caractères
    Retourne :
        <str: Tableau de Markov> en cas de succès.
        <bool: False> en cas d'erreur (e.g. partition incorrecte)."""
    Markov = [[0] * 7 for i in range(7)]  # Génération d'un tableau vide
    score = score.split()

    note = note_lib.getNoteIndex(score[0][:-1])  # Première note
    if note is not False:
        # Boucle pour toutes les notes
        for _ in score[1:]:
            if _ != "p" and _[:-1] != "Z":  # On vérifie qu'il s'agisse bien d'une note
                new_note = note_lib.getNoteIndex(_[:-1])
                if new_note is not False:
                    Markov[note][new_note] += 1  # On ajoute 1 à la case correspondante dans le tableau
                    note = new_note
                else:
                    return False  # On quitte la boucle pour afficher le message d'erreur.
        Markov[note][note_lib.getNoteIndex(score[0][:-1])] += 1  # La dernière note est suivie par la première
        return Markov
    return False


# NOTE:
# La fonction generateMarkovMelody() ne vérifie pas les erreurs dans le tableau de Markov (s'il y a des lettres au lieu
# de chiffres par exemple) dans le but d'économiser quelques ressources puisque nous partons du principe que les erreurs
# potentielles auront été détectées par la fonction generateMarkovTable().
def generateMarkovMelody(markov_table, nb_notes, check_occurrences=False):
    """Génère une mélodie grâce à un tableau de Markov.
    Paramètres :
        str: markov_table : Tableau de Markov
        int: nb_notes : Nombre de notes à générer dans la partition.
        bool: check_occurrences=True : Le programme prend en compte le nombre d'occurrences de chaque note.
    Retourne :
        str: La partition générée."""
    score = []
    note = -1
    # Choix de la première note
    if check_occurrences:
        # [("DO", 4), ("RE", 5), ("MI", 1), ...]
        notes = []
        for _ in range(7):
            occurrences = 0
            for i in range(7):
                occurrences += markov_table[_][i]
            notes.append((_, occurrences))

        # On trie en fonction du nombre d'occurrences, par de l'index de la note.
        # La fonction sort accepte en entrée une liste différente de variables. Au lieu de lui passer *self* (notes),
        # on définit une fonction temporaire (lambda) appelée *occ* qui ne retourne que les nombres d'occurrences.
        notes.sort(key=lambda occ: occ[1])

        note = notes[-1][0]  # On récupère la note et pas le nombre d'occurrences
    else:
        while note == -1:
            note = random.randint(0, 6)
            if markov_table[note] == [0] * 7:  # On ne prend pas de note qui n'apparaît jamais.
                note = -1
    score.append(note_lib.getNoteFromIndex(note) + "n")

    # Choix des notes suivantes :
    if check_occurrences:
        for _ in range(nb_notes):
            choix = []
            for i in range(7):
                for j in range(markov_table[note][i]):
                    choix.append(i)
            note = random.choice(choix)
            score.append(note_lib.getNoteFromIndex(note) + "n")
    else:
        for _ in range(nb_notes):
            # On récupère les notes qui succèdent
            choix = []
            for i in range(7):
                if markov_table[note][i] > 0:
                    choix.append(i)
            note = random.choice(choix)
            score.append(note_lib.getNoteFromIndex(note) + "n")
    return ' '.join(score)

