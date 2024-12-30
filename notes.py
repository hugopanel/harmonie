# Fichier : notes.py
# Nom : Notes
# Auteurs : Hugo PANEL, Mohamed ZAMMIT CHATTI
# Description :
"""
Ce fichier regroupe les fonctions en rapport avec les notes et les partitions.
Ces fonctions permettent d'obtenir les fréquences, les durées, ou les indices des notes.
"""

import settings


def getFrequency(note):
    """Retourne la fréquence d'une note.
    Note: Les silences sont pris en compte et retournent 0Hz.
    Paramètres :
        str: note : La note sous forme de chaîne de caractères (ex: \"DO\")
    Retourne :
        int: Fréquence correspondant à la note, en cas de succès.
        bool: False : en cas d'erreur (e.g. note incorrecte)."""
    notes = {"DO": 264, "RE": 297, "MI": 330, "FA": 352, "SOL": 396, "LA": 440, "SI": 495, "Z": 0}
    if note in notes.keys():  # On vérifie si la note existe
        return notes[note]  # Retourne la fréquence de la note
    else:
        return False  # La note n'existe pas donc on retourne Faux.


def getNoteIndex(note):
    """Retourne le numéro de la note
    ex: DO -> 0
        RE -> 1
        ...
    Les silences (Z) ne sont pas pris en compte.
    Paramètres :
        str: note : La note sous forme de chaîne de caractères (ex: \"DO\").
    Retourne :
        int: Le numéro de la note.
        bool: False : en cas d'erreur (e.g. note incorrecte)."""
    notes = {"DO": 0, "RE": 1, "MI": 2, "FA": 3, "SOL": 4, "LA": 5, "SI": 6}
    if note in notes.keys():
        return notes[note]
    else:
        return False


def getNoteFromIndex(index):
    """Retourne la note correspondante à l'index (entre 0 et 6 compris).
    ex: 0 -> DO
        1 -> RE
        ...
    Paramètres :
        int: index : Le numéro (index) de la note.
    Retourne :
        str: Note correspondante sous forme de chaîne de caractères.
        bool: False : en cas d'erreur (e.g. numéro de note incorrecte)."""
    notes = {0: "DO", 1: "RE", 2: "MI", 3: "FA", 4: "SOL", 5: "LA", 6: "SI"}
    if index in notes.keys():
        return notes[index]
    else:
        return False


def getDuration(duree):
    """Retourne la durée correspondante en secondes.
    Paramètres :
        str: duree : La durée de la note sous forme de caractère. (ex: \"c\")
    Retourne :
        int : Durée de la note en secondes.
        bool: False : En cas d'erreur (e.g. caractère de durée incorrecte)."""
    bpm = int(settings.Settings["audio"]["bpm"])
    durees = {"c": 0.5*60/bpm, "n": 1*60/bpm, "b": 2*60/bpm, "r": 4*60/bpm}
    if duree in durees.keys():
        return durees[duree]
    else:
        return False
