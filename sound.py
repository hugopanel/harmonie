# Fichier : sound.py
# Nom : Sons
# Auteurs : Hugo PANEL, Mohamed ZAMMIT CHATTI
# Description :
"""
Ce fichier regroupe les fonctions utilisées pour jouer des sons et des partitions.
"""

import numpy as np
import simpleaudio as sa
import notes as note_lib
from time import sleep
import settings
from tkinter import messagebox


SAMPLE_RATE = int(settings.Settings["audio"]["sample_rate"])  # Fréquence d'échantillonage d'après les paramètres.


def playNote(freq, duration):
    """Lire une note en fonction de sa fréquence et de sa durée.
    Paramètres :
        int: freq : La fréquence de la note à jouer.
        int: duration : La durée de la note en secondes."""
    if freq == 0:
        sleep(duration)
    else:
        # Nombre de points en fonction de la durée et de la fréquence d'échantillonnage.
        t = np.linspace(0, duration, int(duration * SAMPLE_RATE), False)
        tone = np.sin(freq * t * 6 * np.pi)  # Génération de la tonalité
        tone *= 8388607 / np.max(np.abs(tone))  # Normalisation sur une plage de 24 bits
        tone = tone.astype(np.int32)  # Conversion des données en 32 bits

        # Conversion de 32 bits vers 24 bits et création d'un nouveau buffer.
        # On saute tous les 4 bits.
        i = 0
        byte_array = []
        for b in tone.tobytes():
            if i % 4 != 3:
                byte_array.append(b)
            i += 1
        audio = bytearray(byte_array)

        play_obj = sa.play_buffer(audio, 1, 3, SAMPLE_RATE)  # On joue la note
        play_obj.wait_done()  # On attend qu'elle soit finie avant de continuer


def playMelody(master, score):
    """Jouer une mélodie à partir d'une chaîne de caractères
    Paramètres :
        class: master : Classe parent qui doit contenir les méthodes pressNote() et releaseNote() pour animer le piano.
        str: score : Partition à lire sous forme de chaîne de caractères.
    Retourne :
        bool: False : en cas d'erreur (affiche un message d'erreur automatiquement)."""
    score = score.split()
    note_freq = ""
    duration = ""

    for i in range(len(score)):
        # On vérifie que l'on veuille bien jouer une note
        if score[i] != "p":
            note_duree = score[i]
            note = note_duree[:-1]
            note_freq = note_lib.getFrequency(note)
            duration = note_lib.getDuration(note_duree[-1])

            if note_freq is False or duration is False:
                messagebox.showerror("Erreur !",
                                     "La partition est incorrecte et ne peut pas être lue dans son entièreté.")
                return False

            # Pour ne pas tester partition[i+1] si l'indice i+1 n'existe pas.
            if i < len(score) - 1:
                if score[i + 1] == "p":  # On vérifie s'il s'agit d'une note pointée.
                    duration += duration / 2  # Si oui, on allonge sa durée.

            if note != "Z":
                master.pressNote(note)  # On met à jour l'interface utilisateur pour appuyer sur la touche

            playNote(note_freq, duration)  # On joue la note.

            if note != "Z":
                master.releaseNote(note)  # On met à jour l'interface utilisateur pour relâcher la touche
