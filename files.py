# Fichier : files.py
# Nom : Fichiers
# Auteurs : Hugo PANEL, Mohamed ZAMMIT CHATTI
# Description :
"""
Ce fichier regroupe les fonctions permettant de lire le contenu d'un fichier.
"""

import settings
from tkinter import filedialog


def readFile(file_path):
    """Lit l'entièreté d'un fichier.
    Paramètres :
        str: file_path : Chemin vers le fichier.
    Retourne :
        liste contenant toutes les lignes."""
    try:
        with open(file_path, "r", encoding='utf8') as file:
            res = file.readlines()
    except IOError:
        return False
    return res


def addLine(file_path, line):
    """Ajoute une ligne à un fichier.
    Paramètres :
        str: file_path : Chemin vers le fichier.
        str: line : Contenu de la ligne à ajouter.
    Retourne :
        False s'il y a eu une erreur d'ouverture du fichier."""
    try:
        with open(file_path, "a+", encoding='utf8') as file:
            file.write(line)
    except IOError:
        return False
    return True


def replaceFile(file_path, content):
    """Remplace le contenu d'un fichier par *content*
    Paramètres :
        str: file_path : Chemin vers le fichier.
        str: content : Nouveau contenu du fichier.
    Retourne :
        False s'il y a eu une erreur d'ouverture du fichier."""
    try:
        with open(file_path, "w", encoding='utf8') as file:
            file.write(content)
    except IOError:
        return False
    return True


def openFileDialog():
    """Demande à l'utilisateur de sélectionner un fichier sur son ordinateur.
    Retourne :
        str: Le chemin vers le fichier sélectionné."""
    file_path = filedialog.askopenfilename()
    return file_path


def getPartition(score_index):
    """Récupère une partition.
    Paramètres :
        partition_index : numéro de la partition dans la base de données.
    Retourne : Tuple:
        (True, <str: Partition>) en cas de succès.
        (False, <str: Message d'erreur>) en cas d'erreur."""
    try:
        with open(settings.scores_path, "r", encoding='utf8') as file:
            line = file.readline()
            score_number = 0
            while line != "":
                if line[0] == '#':
                    # C'est un numéro
                    score_number += 1
                    if score_number == score_index:
                        score = file.readline()
                        while len(score.strip()) == 0 and score != "":
                            score = file.readline()
                        if score != "":
                            return True, "" if score.strip()[0] in ["#", ""] else score
                        else:
                            pass
                line = file.readline()
    except IOError:
        return False, "Le fichier n'a pas été trouvé."
    return False, "La partition n'a pas été trouvée."


def getPartitionName(score_index):
    """Récupère le nom de la partition dans la base de données.
    Paramètres :
        partition_index : Numéro de la partition dans la base de données
    Retourne : Tuple:
        (True, <str: Nom de la partition>) en cas de succès.
        (False, <str: Message d'erreur>) en cas d'erreur."""
    try:
        with open(settings.scores_path, "r", encoding='utf8') as file:
            line = file.readline()
            score_number = 0
            while line != "":
                if line[0] == "#":
                    score_number += 1
                    if score_number == score_index:
                        return True, ' '.join(line.split()[1:])
                line = file.readline()
    except IOError:
        return False, "Le fichier n'a pas été trouvé."
    return False, "La partition n'a pas été trouvée."


def getPartitions():
    """Retourne une liste de tuples contenant toutes les partitions de la base de données avec le numéro.
    Retourne : tuple:
        (True, [(<int: Numéro de la partition dans la base de données>, <str: Partition>), ...]) en cas de succès.
        (False, <str: Message d'erreur>) en cas d'erreur."""
    scores_file_path = settings.scores_path
    try:
        with open(scores_file_path, "r", encoding='utf8') as file:
            scores = []
            lines = file.readlines()
            score_number = 0
            for i in range(len(lines)):
                if lines[i][0] == '#':
                    score_number += 1
                    line = lines[i]
                    line = line.split()
                    scores.append((score_number, ' '.join(line[1:]),
                                       "" if (i == len(lines)-1 or lines[i+1][0] == "#") else
                                       lines[i+1][:-1] if lines[i+1][-1] == '\n' else lines[i+1]))
            return True, scores
    except IOError:
        return False, "Le fichier n'a pas été trouvé."
