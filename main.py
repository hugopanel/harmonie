from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import files
from sound import playMelody
import settings
import markov
from time import sleep
import random
import operations
import notes as notes_lib


root = Tk()
root.title("Menu Principal - L'harmonie est numérique.")
root.geometry("420x420")
root.resizable(False, False)


class MainMenuWindow:
    """Fenêtre du menu principal."""
    def __init__(self, master):
        """Constructeur de la classe. Affiche la fenêtre et ses éléments."""

        # Lecture et génération de partitions.
        frameScores = LabelFrame(master, text="Partitions", padx=60, pady=10)
        Label(frameScores,
              text="Jouez une partition ou générez une nouvelle\n mélodie en s'inspirant d'autres partitions.") \
            .grid(row=0, column=0)
        bPlayScore = Button(frameScores, text="Jouer une partition", command=PlayWindow).grid(row=1, column=0)
        bGenerateScore = Button(frameScores, text="Générer une partition", command=GenerateWindow).grid(row=2, column=0)
        frameScores.pack()

        # Opérations sur les partitions
        frameOperations = LabelFrame(master, text="Opérations", padx=60, pady=10)
        Label(frameOperations, text="Effectuez des opérations mathématiques \nsur les partitions.") \
            .grid(row=0, column=0)
        bTranspose = Button(frameOperations, text="Transposition", command=TranspositionWindow).grid(row=1, column=0)
        bInvert = Button(frameOperations, text="Inversion", command=InversionWindow).grid(row=2, column=0)
        frameOperations.pack()

        # Base de données
        frameDatabase = LabelFrame(master, text="Base de données", padx=60, pady=10)
        Label(frameDatabase,
              text="Consultez la base de données pour \nconsulter, ajouter, ou supprimer des partitions.") \
            .grid(row=0, column=0)
        bShowDatabase = Button(frameDatabase, text="Accéder à la base de données", command=DatabaseWindow) \
            .grid(row=1, column=0)
        frameDatabase.pack()

        # Paramètres et "Quitter"
        frameBottomButtons = Frame(master, pady=10)
        bOpenSettings = Button(frameBottomButtons, text="Paramètres", command=SettingsWindow).grid(row=0, column=0)
        bQuit = Button(frameBottomButtons, text="Quitter", command=root.destroy).grid(row=0, column=1)
        frameBottomButtons.pack()


class SettingsWindow:
    """Fenêtre des paramètres."""
    def __init__(self):
        """Constructeur de la classe. Affiche la fenêtre et ses éléments."""
        wSettings = Toplevel()
        wSettings.geometry("230x200")
        wSettings.title("Paramètres")
        wSettings.resizable(False, False)  # On ne peut plus la redimensionner.
        wSettings.grab_set()  # Pour empêcher les interactions sur la première fenêtre.

        frameAudioSettings = LabelFrame(wSettings, text="Paramètres Audio", pady=18)

        self.sample_rate = IntVar()
        self.sample_rate.set(settings.Settings["audio"]["sample_rate"])
        sample_rates = [44100, 48000, 96000, 192000]
        Label(frameAudioSettings, text="Fréquence d'échantillonnage : ").pack()
        cbSample_Rate = OptionMenu(frameAudioSettings, self.sample_rate, *sample_rates)
        cbSample_Rate.pack()

        Label(frameAudioSettings, text="Vitesse (Battements par minute) : ").pack()
        self.iBPM = Entry(frameAudioSettings)
        self.iBPM.insert(0, settings.Settings["audio"]["bpm"])
        self.iBPM.pack()

        frameAudioSettings.pack()

        frameAudioSettings = Frame(wSettings)

        bSaveSettings = Button(frameAudioSettings, text="Sauvegarder", command=self.save)
        bSaveSettings.grid(row=0, column=0)
        Button(frameAudioSettings, text="Fermer", command=wSettings.destroy).grid(row=0, column=1)

        frameAudioSettings.pack(pady=10)

    def save(self):
        """Sauvegarde les paramètres dans le fichier de configuration."""
        settings.Settings["audio"]["sample_rate"] = int(self.sample_rate.get())
        settings.Settings["audio"]["bpm"] = int(self.iBPM.get())
        if settings.saveSettings() is False:
            messagebox.showerror("Erreur !", "Impossible de sauvegarder les paramètres pour le moment.\n" +
                                 "Veuillez réessayer dans quelques instants et vérifier que le fichier de configuration"
                                 "n'est ouvert nulle part.")
        else:
            messagebox.showinfo("Succès !", "Les paramètres ont bien été sauvegardés.")


class DatabaseWindow:
    """Fenêtre Base de données."""
    def __init__(self):
        """Constructeur de la classe. Affiche la fenêtre et ses éléments."""
        self.wDatabase = Toplevel()
        self.wDatabase.geometry("850x220")
        self.wDatabase.title("Base de données")
        self.wDatabase.resizable(False, False)
        self.wDatabase.grab_set()  # Pour empêcher les interactions sur la première fenêtre.

        Label(self.wDatabase, text="Consultez la base de données de partitions :").grid(row=0, column=0)
        self.dbWidget = DbWidget(self.wDatabase)
        self.dbWidget.grid(row=1, column=0)

        actionButtonsFrame = Frame(self.wDatabase)
        self.addButton = Button(actionButtonsFrame, text="Ajouter une partition", command=self.showAddScore).pack()
        self.removeButton = Button(actionButtonsFrame, text="Supprimer la partition", command=self.deleteScore).pack()
        self.editButton = Button(actionButtonsFrame, text="Modifier la partition", command=self.showEditWindow).pack()
        actionButtonsFrame.grid(row=1, column=1)

        self.dbWidget.update()

    def deleteScore(self):
        """Supprime la partition sélectionnée de la base de données."""
        score_number = self.dbWidget.getSelection()
        if len(score_number) > 0:
            score_number = self.dbWidget.getSelection()[0]
            file = files.readFile(settings.scores_path)
            if file is not False:
                scores = []
                pos = 0
                for i in range(len(file)):
                    if file[i][0] == '#':
                        pos += 1
                        if pos != score_number:
                            scores.append(file[i])
                            if i + 1 < len(file):
                                if file[i + 1][0] != '#':
                                    scores.append(file[i + 1])
                files.replaceFile(settings.scores_path, ''.join(scores))
                self.dbWidget.update()
                messagebox.showinfo("Succès !", "La partition a bien été supprimée.")
            else:
                messagebox.showerror("Erreur !",
                                     "Impossible de supprimer la partition car l'ouverture du fichier a échouée.")

    def showEditWindow(self):
        """Affiche la fenêtre de modification de partition."""
        self.editSelection = self.dbWidget.getSelection()
        if len(self.editSelection) > 0:  # Si une partition est sélectionnée.
            self.wEditScore = Toplevel()
            self.wEditScore.geometry("400x170")
            self.wEditScore.title("Modifier une partition.")
            self.wEditScore.resizable(True, False)
            self.wEditScore.grab_set()

            editScoreFrame = Frame(self.wEditScore)
            Label(editScoreFrame, text="Nom de la partition : ").pack()
            self.iNewScoreName = Entry(editScoreFrame)
            self.iNewScoreName.pack(fill=X, padx=10, pady=10)
            Label(editScoreFrame, text="Partition : ").pack()
            self.iNewScore = Entry(editScoreFrame)
            hScrollbar = Scrollbar(editScoreFrame, orient=HORIZONTAL)
            hScrollbar.pack(side=BOTTOM, fill=X)
            hScrollbar.config(command=self.iNewScore.xview)
            self.iNewScore.configure(xscrollcommand=hScrollbar.set)
            self.iNewScore.pack(fill=X)
            editScoreFrame.pack(fill=X, padx=10, pady=10)
            partition = files.getPartition(self.dbWidget.getSelection()[0])

            # Récupération du nom de la partition
            score_name = files.getPartitionName(self.dbWidget.getSelection()[0])
            if score_name[0]:
                self.iNewScoreName.insert(0, score_name[1])

                # Récupération de la partition
                if partition[0] and len(partition[1]) > 0:
                    self.iNewScore.insert(0, partition[1][:-1] if partition[1][-1] == '\n' else partition[1])

            if score_name[0] is False or partition[0] is False:
                messagebox.showerror("Erreur !", "La partition souhaitée n'a pas été trouvée.")
                self.dbWidget.update()
                return

            actionButtonsLabel = Label(self.wEditScore)
            self.bApplyEditScore = Button(actionButtonsLabel, text="Sauvegarder et quitter",
                                          command=self.applyEditScore)
            self.bApplyEditScore.grid(row=0, column=0)
            bCancel = Button(actionButtonsLabel, text="Annuler", command=self.wEditScore.destroy)
            bCancel.grid(row=0, column=1)
            actionButtonsLabel.pack()

    def applyEditScore(self):
        """Sauvegarde les modifications apportées à une partition."""
        newScoreName = self.iNewScoreName.get()  # Nouveau nom pour la partition
        newScore = self.iNewScore.get()  # La partition modifiée
        score_index = self.editSelection[0]  # La position de la partition modifiée
        try:
            with open(settings.scores_path, "r", encoding='utf8') as file:
                lines = file.readlines()
                score_number = 0
                res = []
                for line in range(len(lines)):
                    if lines[line][0] == '#':
                        score_number += 1
                        if score_number == score_index:
                            res.append('#' + str(score_index) + ' ' + newScoreName + '\n')
                            res.append(newScore + '\n')
                        else:
                            res.append(lines[line])
                            if line + 1 < len(lines) - 1:
                                if lines[line + 1][0] != '#':
                                    res.append(lines[line + 1])
                files.replaceFile(settings.scores_path, ''.join(res))
        except IOError:
            messagebox.showerror("Erreur !", "Impossible d'ouvrir le fichier de partitions.\n" +
                                 "Les modifications n'ont pas pu être sauvegardées.")
            # On ne ferme pas la fenêtre s'il y a eu une erreur, pour pouvoir réessayer.
        finally:
            self.dbWidget.update()
            self.wEditScore.destroy()

    def showAddScore(self):
        """Affiche la fenêtre d'ajout de partition."""
        self.wAddScore = Toplevel()
        self.wAddScore.geometry("400x170")
        self.wAddScore.title("Ajouter une nouvelle partition")
        self.wAddScore.resizable(True, False)
        self.wAddScore.grab_set()

        addScoreFrame = Frame(self.wAddScore)
        Label(addScoreFrame, text="Nom de la partition : ").pack()
        self.iNewScoreName = Entry(addScoreFrame)
        self.iNewScoreName.pack(fill=X, padx=10, pady=10)
        Label(addScoreFrame, text="Partition : ").pack()
        self.iNewScore = Entry(addScoreFrame)
        hScrollbar = Scrollbar(addScoreFrame, orient=HORIZONTAL)
        hScrollbar.pack(side=BOTTOM, fill=X)
        hScrollbar.config(command=self.iNewScore.xview)
        self.iNewScore.configure(xscrollcommand=hScrollbar.set)
        self.iNewScore.pack(fill=X)
        addScoreFrame.pack(fill=X, padx=10, pady=10)

        actionButtonsLabel = Label(self.wAddScore)
        self.bCreateNewScore = Button(actionButtonsLabel, text="Sauvegarder et quitter", command=self.addNewScore)
        self.bCreateNewScore.grid(row=0, column=0)
        bCancel = Button(actionButtonsLabel, text="Annuler", command=self.wAddScore.destroy)
        bCancel.grid(row=0, column=1)
        actionButtonsLabel.pack()

    def addNewScore(self):
        """Sauvegarde la nouvelle partition."""
        newScoreName = self.iNewScoreName.get()
        newScore = self.iNewScore.get()
        if files.addLine(settings.scores_path,
                         '\n#' + str(self.dbWidget.getWidget().size()) + ' ' + newScoreName + '\n' +
                         newScore):
            messagebox.showinfo("Succès !", "La partition a bien été ajoutée.")
            self.dbWidget.update()
            self.wAddScore.destroy()
        else:
            messagebox.showerror("Erreur !", "Une erreur s'est produite et la partition n'a pas pu être ajoutée.")


class PlayWindow:
    """Fenêtre de lecture de partitions."""
    def __init__(self):
        """Constructeur de la classe. Affiche la fenêtre et ses éléments."""
        self.wPlay = Toplevel()
        self.wPlay.geometry("820x350")
        self.wPlay.title("Jouer une partition")
        self.wPlay.resizable(False, False)
        self.wPlay.grab_set()

        Label(self.wPlay, text="Jouez la partition désirée.").grid(row=0, column=0)
        self.dbWidget = DbWidget(self.wPlay)
        self.dbWidget.grid(row=1, column=0)

        actionButtonsFrame = Frame(self.wPlay)
        self.playButton = Button(actionButtonsFrame, text="Jouer la mélodie", command=self.playMusic)
        self.playButton.pack()
        self.bReadFromFile = Button(actionButtonsFrame, text="Lire un fichier", command=self.readFromFile)
        self.bReadFromFile.pack()
        actionButtonsFrame.grid(row=1, column=1)

        # Affichage du piano
        self.pianoFrame = LabelFrame(self.wPlay, text="Piano : ")

        self.notes_variations = {"DO": "Var1", "RE": "Var3", "MI": "Var2", "FA": "Var1", "SOL": "Var3", "LA": "Var3",
                                 "SI": "Var2"}

        self.DOImage_Released = ImageTk.PhotoImage(Image.open("img/" + self.notes_variations["DO"] + "_Released.png"))
        self.DOImage_Pressed = ImageTk.PhotoImage(Image.open("img/" + self.notes_variations["DO"] + "_Pressed.png"))
        self.DOLabel = Label(self.pianoFrame, image=self.DOImage_Released, borderwidth=0)
        self.DOLabel.grid(row=0, column=0)

        self.REImage_Released = ImageTk.PhotoImage(Image.open("img/" + self.notes_variations["RE"] + "_Released.png"))
        self.REImage_Pressed = ImageTk.PhotoImage(Image.open("img/" + self.notes_variations["RE"] + "_Pressed.png"))
        self.RELabel = Label(self.pianoFrame, image=self.REImage_Released, borderwidth=0)
        self.RELabel.grid(row=0, column=1)

        self.MIImage_Released = ImageTk.PhotoImage(Image.open("img/" + self.notes_variations["MI"] + "_Released.png"))
        self.MIImage_Pressed = ImageTk.PhotoImage(Image.open("img/" + self.notes_variations["MI"] + "_Pressed.png"))
        self.MILabel = Label(self.pianoFrame, image=self.MIImage_Released, borderwidth=0)
        self.MILabel.grid(row=0, column=2)

        self.FAImage_Released = ImageTk.PhotoImage(Image.open("img/" + self.notes_variations["FA"] + "_Released.png"))
        self.FAImage_Pressed = ImageTk.PhotoImage(Image.open("img/" + self.notes_variations["FA"] + "_Pressed.png"))
        self.FALabel = Label(self.pianoFrame, image=self.FAImage_Released, borderwidth=0)
        self.FALabel.grid(row=0, column=3)

        self.SOLImage_Released = ImageTk.PhotoImage(Image.open("img/" + self.notes_variations["SOL"] + "_Released.png"))
        self.SOLImage_Pressed = ImageTk.PhotoImage(Image.open("img/" + self.notes_variations["SOL"] + "_Pressed.png"))
        self.SOLLabel = Label(self.pianoFrame, image=self.SOLImage_Released, borderwidth=0)
        self.SOLLabel.grid(row=0, column=4)

        self.LAImage_Released = ImageTk.PhotoImage(Image.open("img/" + self.notes_variations["LA"] + "_Released.png"))
        self.LAImage_Pressed = ImageTk.PhotoImage(Image.open("img/" + self.notes_variations["LA"] + "_Pressed.png"))
        self.LALabel = Label(self.pianoFrame, image=self.LAImage_Released, borderwidth=0)
        self.LALabel.grid(row=0, column=5)

        self.SIImage_Released = ImageTk.PhotoImage(Image.open("img/" + self.notes_variations["SI"] + "_Released.png"))
        self.SIImage_Pressed = ImageTk.PhotoImage(Image.open("img/" + self.notes_variations["SI"] + "_Pressed.png"))
        self.SILabel = Label(self.pianoFrame, image=self.SIImage_Released, borderwidth=0)
        self.SILabel.grid(row=0, column=6)

        self.pianoFrame.grid(row=2, column=0)

        self.notes_images = {"DO": (self.DOImage_Released, self.DOImage_Pressed),
                             "RE": (self.REImage_Released, self.REImage_Pressed),
                             "MI": (self.MIImage_Released, self.MIImage_Pressed),
                             "FA": (self.FAImage_Released, self.FAImage_Pressed),
                             "SOL": (self.SOLImage_Released, self.SOLImage_Pressed),
                             "LA": (self.LAImage_Released, self.LAImage_Pressed),
                             "SI": (self.SIImage_Released, self.SIImage_Pressed)}
        self.notes_labels = {"DO": self.DOLabel,
                             "RE": self.RELabel,
                             "MI": self.MILabel,
                             "FA": self.FALabel,
                             "SOL": self.SOLLabel,
                             "LA": self.LALabel,
                             "SI": self.SILabel}

        self.dbWidget.update()  # Remplit la liste de partitions.

    def playMusic(self):
        """Joue la partition sélectionnée."""
        if len(self.dbWidget.getSelection()) > 0:  # Si une partition est sélectionnée.
            Selection = self.dbWidget.getSelection()[0]
            partition = files.getPartition(Selection)
            # partition = Tuple: (True/False, "partition"/"message d'erreur")
            if partition[0]:  # Si partition[0] est True, donc si la partition a été trouvée :
                self.playButton.configure(state=DISABLED)  # On désactive le bouton "Jouer" puisqu'on joue déjà.
                self.bReadFromFile.configure(state=DISABLED)
                playMelody(self, partition[1])
            else:
                print("Erreur : " + partition[1])
                messagebox.showwarning("Erreur !", partition[1])
            self.playButton.configure(state=NORMAL)  # On réactive le bouton "Jouer"
            self.bReadFromFile.configure(state=NORMAL)

    def readFromFile(self):
        """Demande à l'utilisateur d'ouvrir un fichier pour le lire."""
        file_path = files.openFileDialog()
        if file_path != "":
            score_name = ""
            score = ""
            try:
                with open(file_path, 'r', encoding="utf8") as file:
                    line = file.readline()
                    while line != "":
                        if line[0] == '#' and score_name == "":
                            line = line.split()
                            score_name = ' '.join(line[1:])
                        else:
                            score = line
                            break
                        line = file.readline()
            except IOError:
                messagebox.showerror("Erreur !", "Impossible d'ouvrir le fichier spécifié.")
            finally:
                self.playButton.configure(state=DISABLED)
                self.bReadFromFile.configure(state=DISABLED)
                if playMelody(self, score) is False:
                    messagebox.showwarning("Erreur !", "Une erreur est survenue. Il se peut que la partition soit " +
                                                       "incorrecte et elle ne sera pas ajoutée à la base de données.")
                else:
                    self.playButton.configure(state=NORMAL)
                    self.bReadFromFile.configure(state=NORMAL)
                    # Ajout de la partition à la base de données :
                    score_number = self.dbWidget.getWidget().size() + 2
                    if files.addLine(settings.scores_path, '\n#' + str(score_number) + ' ' + score_name + '\n' + score):
                        messagebox.showinfo("Succès !", "Cette partition vient d'être ajoutée à la base de données.")
                        return
                    messagebox.showerror("Erreur !", "Cette partition n'a pas pu être ajoutée à la base de données.")

    def pressNote(self, note):
        """Change l'image du piano pour 'appuyer' sur la touche correspondante."""
        self.notes_labels[note].configure(image=self.notes_images[note][1])
        self.wPlay.update()

    def releaseNote(self, note):
        """Change l'image du piano pour 'relâcher' la touche correspondante."""
        self.notes_labels[note].configure(image=self.notes_images[note][0])
        self.wPlay.update()
        sleep(0.05)


class GenerateWindow:
    """Fenêtre de génération de partition"""
    def __init__(self):
        """Constructeur de la classe. Affiche la fenêtre et ses éléments."""
        self.wGenerate = Toplevel()
        self.wGenerate.geometry("850x220")
        self.wGenerate.title("Génération de partitions")
        self.wGenerate.resizable(False, False)
        self.wGenerate.grab_set()

        Label(self.wGenerate, text="Générez de nouvelles partitions !").grid(row=0, column=0)

        self.dbWidget = DbWidget(self.wGenerate, MULTIPLE)
        self.dbWidget.grid(row=1, column=0)
        self.dbWidget.update()

        actionButtonsFrame = Frame(self.wGenerate, padx=20)

        self.bSelectAll = Button(actionButtonsFrame, text="Tout sélectionner", command=self.selectAll)
        self.bSelectAll.pack()

        self.bDeselectAll = Button(actionButtonsFrame, text="Tout désélectionner", command=self.deselectAll)
        self.bDeselectAll.pack()

        self.bGenerate = Button(actionButtonsFrame, text="Générer", command=self.generateMelody)
        self.bGenerate.pack()

        actionButtonsFrame.grid(row=1, column=1)

        settingsFrame = LabelFrame(self.wGenerate, text="Configuration")

        self.checkOccurrences = BooleanVar()
        self.cCheckOccurrences = Checkbutton(settingsFrame, text='Vérifier le nombre d\'occurrences',
                                             variable=self.checkOccurrences, onvalue=True, offvalue=False)
        self.cCheckOccurrences.pack()
        Label(settingsFrame, text="Nombre de notes : ").pack()

        self.iNbNotes = Entry(settingsFrame)
        self.iNbNotes.insert(0, "20")
        self.iNbNotes.pack()

        settingsFrame.grid(row=1, column=2)

    def selectAll(self):
        """Sélectionne tous les éléments de la liste."""
        self.dbWidget.getWidget().select_set(0, END)

    def deselectAll(self):
        """Annule la sélection de l'utilisateur dans la liste."""
        self.dbWidget.getWidget().selection_clear(0, END)

    def generateMelody(self):
        """Génère une mélodie d'après la/les partition(s) sélectionnée(s)."""
        if len(self.dbWidget.getSelection()) > 0:
            partitions = self.dbWidget.getSelection()
            partition = ""
            for _ in partitions:
                _ = files.getPartition(_)
                if _[0]:
                    partition += '   ' + _[1][:-1] if _[1][-1] == '\n' else _[1]
                else:
                    print(_[1])
                    messagebox.showerror("Erreur !", "L'une des partitions n'a pas été trouvée.")
                    self.dbWidget.update()
                    return
            print(partition)
            _markovTable = markov.generateMarkovTable(partition)
            if _markovTable is False:
                messagebox.showerror("Erreur !", "L'une des partitions fournies est incorrecte.\n" +
                                     "Le tableau de Markov n'a pas pu être généré.")
                return
            melody = markov.generateMarkovMelody(_markovTable, int(self.iNbNotes.get()), self.checkOccurrences)
            score_number = self.dbWidget.getWidget().size() + 1
            name = []
            for _ in self.dbWidget.getSelection():
                partition_name = files.getPartitionName(_)
                if partition_name[0]:
                    name.append(partition_name[1])
            name = ' + '.join(name) + ' ' + str(random.randint(1000, 9999))
            try:
                files.addLine(settings.scores_path, "\n#" + str(score_number) + " " + name + '\n')
                files.addLine(settings.scores_path, melody)
                messagebox.showinfo("Succès !", "La partition '" + name + "' a bien été ajoutée.")
                self.dbWidget.update()
            except:
                messagebox.showerror("Erreur !",
                                     "Une erreur s'est produite et il se peut que la partition n'ait pas pu être ajoutée à la base de données.")


class TranspositionWindow:
    """Fenêtre de transposition de partition."""
    def __init__(self):
        """Constructeur de la classe. Affiche la fenêtre et ses éléments."""
        self.wTransposition = Toplevel()
        self.wTransposition.title("Transposition")
        self.wTransposition.geometry("400x320")
        self.wTransposition.grab_set()

        Label(self.wTransposition, text="Transposez des partitions.").pack()
        self.dbWidget = DbWidget(self.wTransposition)
        self.dbWidget.pack()
        self.dbWidget.update()

        configurationFrame = LabelFrame(self.wTransposition, text="Configuration : ")
        Label(configurationFrame, text="k=").grid(row=0, column=0)
        self.iK = Entry(configurationFrame)
        self.iK.insert(0, "5")
        self.iK.grid(row=0, column=1)
        Label(configurationFrame, text="Intervalle : ").grid(row=1, column=0)
        self.iInterval = Entry(configurationFrame)
        self.iInterval.insert(0, "(0;6)")
        self.iInterval.grid(row=1, column=1)
        configurationFrame.pack()

        actionButtonsFrame = Frame(self.wTransposition)
        Button(actionButtonsFrame, text="Transposer la partition", command=self.Transpose).grid(row=0, column=0)
        Button(actionButtonsFrame, text="Quitter", command=self.wTransposition.destroy).grid(row=0, column=1)
        actionButtonsFrame.pack()

    def Transpose(self):
        """Transpose une partition."""
        partition_index = self.dbWidget.getSelection()
        print(partition_index)
        if len(partition_index) > 0:
            partition_index = partition_index[0]
            score = files.getPartition(partition_index)
            if score[0]:
                k = int(self.iK.get())

                # Intervalle :
                interval = self.iInterval.get()
                # '  (0;6)  ' --> [0, 6]
                interval = interval.strip()  # '(0;6)'
                interval = interval[1:-1]  # '0;6'
                interval = interval.split(';')  # ['0', '6']
                interval = [int(_) for _ in interval]  # [0, 6]
                print(interval)

                # Partition :
                score = score[1][:-1] if score[1][-1] == '\n' else score[1]
                score = score.split()  # ['DOn', 'REc', 'p', 'Zc', ...]
                newScore = []
                for i in score:  # ['DOn', 'REc', ...]
                    if i != 'p' and i[0] != 'Z':
                        newScore.append(i)
                score = newScore
                score = [_[:-1] for _ in score]  # ['DO', 'RE', ...]
                score = [notes_lib.getNoteIndex(_) if _ != '' else '' for _ in score]  # [0, 1, ...]
                for i in range(len(score)):
                    if score[i] is False:
                        messagebox.showerror("Erreur !", "La partition est invalide et ne peut pas être transposée.")
                        return

                transposition = operations.transposition(score, k, interval)
                suffix = ""
                res = []
                i = 0
                while i < len(transposition):
                    note = notes_lib.getNoteFromIndex(transposition[i])
                    if note is False:
                        messagebox.showwarning("Erreur !", "Une erreur s'est produite et la transposition ne peut pas" +
                                               " être convertie en partition.\nSi l'intervalle est différent de (0;6)," +
                                               " la transposition ne pourra pas être convertie en partition.\n" +
                                               "La transposition va être sauvegardé tout de même mais ne sera pas " +
                                               "lisible.")
                        suffix = " (Illisible)"
                        break
                    res.append(note)
                    i += 1

                if i == len(transposition):
                    transposition = res
                else:
                    transposition = [str(_) for _ in transposition]

                # Enregistrement de la nouvelle partition :
                score_number = self.dbWidget.getWidget().size()
                score_name = files.getPartitionName(partition_index)
                if score_name[0] is False:
                    messagebox.showerror("Erreur !",
                                         "Une erreur est survenue et la partition demandée n'a pas été trouvée.")
                    return
                interval = [str(_) for _ in interval]
                if files.addLine(settings.scores_path,
                                 line='\n#' + str(score_number + 1) + ' ' + score_name[1] + ' k=' +
                                      str(k) + ' Interval=(' + ';'.join(interval) + ') ' +
                                      str(random.randint(1000, 9999)) + suffix + '\n') is not False:
                    transposition = ' '.join(transposition)
                    if files.addLine(settings.scores_path, transposition) is not False:
                        messagebox.showinfo("Succès !", "La partition a bien été sauvegardée.")
                        return
                messagebox.showerror("Erreur !", "Une erreur est survenue lors de l'enregistrement de la partition.")
            else:
                messagebox.showerror("Erreur !", "La partition n'a pas été trouvée.")


class InversionWindow:
    """Fenêtre d'inversion de partition."""
    def __init__(self):
        """Constructeur de la classe. Affiche la fenêtre et ses éléments."""
        self.wInverse = Toplevel()
        self.wInverse.title("Inversion")
        self.wInverse.geometry("400x300")
        self.wInverse.grab_set()

        Label(self.wInverse, text="Inversez des partitions.").pack()
        self.dbWidget = DbWidget(self.wInverse)
        self.dbWidget.pack()
        self.dbWidget.update()

        configurationFrame = LabelFrame(self.wInverse, text="Configuration : ")
        Label(configurationFrame, text="Intervalle : ").grid(row=0, column=0)
        self.iInterval = Entry(configurationFrame)
        self.iInterval.insert(0, "(0;6)")
        self.iInterval.grid(row=0, column=1)
        configurationFrame.pack()

        actionButtonsFrame = Frame(self.wInverse)
        Button(actionButtonsFrame, text="Inverser la partition", command=self.Invert).grid(row=0, column=0)
        Button(actionButtonsFrame, text="Quitter", command=self.wInverse.destroy).grid(row=0, column=1)
        actionButtonsFrame.pack()

    def Invert(self):
        """Inverse la partition sélectionnée."""
        score_index = self.dbWidget.getSelection()
        if len(score_index) > 0:
            score_index = score_index[0]
            score = files.getPartition(score_index)
            if score[0]:
                # Intervalle :
                interval = self.iInterval.get()
                # '  (0;6)  ' --> [0, 6]
                interval = interval.strip()  # '(0;6)'
                interval = interval[1:-1]  # '0;6'
                interval = interval.split(';')  # ['0', '6']
                interval = [int(_) for _ in interval]  # [0, 6]
                print(interval)

                # Partition :
                score = score[1][:-1] if score[1][-1] == '\n' else score[1]
                score = score.split()  # ['DOn', 'REc', 'p', 'Zc', ...]
                newScore = []
                for i in score:  # ['DOn', 'REc', ...]
                    if i != 'p' and i[0] != 'Z':
                        newScore.append(i)
                score = newScore
                score = [_[:-1] for _ in score]  # ['DO', 'RE', ...]
                score = [notes_lib.getNoteIndex(_) if _ != '' else '' for _ in score]  # [0, 1, ...]
                for i in range(len(score)):
                    if score[i] is False:
                        messagebox.showerror("Erreur !", "La partition est invalide et ne peut pas être inversée.")
                        return

                inversion = operations.inversion(score, interval)
                suffix = ""
                res = []
                i = 0
                while i < len(inversion):
                    note = notes_lib.getNoteFromIndex(inversion[i])
                    if note is False:
                        messagebox.showwarning("Erreur !", "Une erreur s'est produite et l'inversion ne peut pas" +
                                               " être convertie en partition.\nSi l'intervalle est différent de (0;6)," +
                                               " l'inversion ne pourra pas être convertie en partition.\n" +
                                               "L'inversion va être sauvegardé tout de même mais ne sera pas " +
                                               "lisible.")
                        suffix = " (Illisible)"
                        break
                    res.append(note)
                    i += 1
                if i == len(inversion):
                    inversion = res
                else:
                    inversion = [str(_) for _ in inversion]

                # Enregistrement de la nouvelle partition :
                score_number = self.dbWidget.getWidget().size()
                score_name = files.getPartitionName(score_index)
                if score_name[0] is False:
                    messagebox.showerror("Erreur !",
                                         "Une erreur est survenue et la partition demandée n'a pas été trouvée.")
                    return
                interval = [str(_) for _ in interval]
                if files.addLine(settings.scores_path, line='\n#' + str(score_number + 1) + ' ' + score_name[1] +
                                                            ' Interval=(' + ';'.join(interval) + ') ' +
                                                            str(random.randint(1000,
                                                                               9999)) + suffix + '\n') is not False:
                    inversion = ' '.join(inversion)
                    if files.addLine(settings.scores_path, inversion) is not False:
                        messagebox.showinfo("Succès !", "La partition a bien été sauvegardée.")
                        return
                messagebox.showerror("Erreur !", "Une erreur est survenue lors de l'enregistrement de la partition.")
            else:
                messagebox.showerror("Erreur !", "La partition n'a pas été trouvée.")


class DbWidget:
    """Widget Liste de partitions de la base de données."""
    def __init__(self, master, selectmode=BROWSE):
        """Constructeur de la classe. Affiche le composant."""
        self._dbFrame = Frame(master, padx=10)
        vScrollbar = Scrollbar(self._dbFrame)
        vScrollbar.pack(side=RIGHT, fill=Y)
        hScrollbar = Scrollbar(self._dbFrame, orient=HORIZONTAL)
        hScrollbar.pack(side=BOTTOM, fill=X)
        self._dbWidget = Listbox(self._dbFrame, width=70, height=10, yscrollcommand=vScrollbar.set,
                                 xscrollcommand=hScrollbar.set, selectmode=selectmode)
        vScrollbar.config(command=self._dbWidget.yview)
        hScrollbar.config(command=self._dbWidget.xview)
        self._dbWidget.pack()

    def pack(self):
        """Permet d'ajouter le composant à la fenêtre avec pack()."""
        self._dbFrame.pack()

    def grid(self, row, column):
        """Permet d'ajouter le composant à la fenêtre avevc grid()"""
        self._dbFrame.grid(row=row, column=column)

    def getWidget(self):
        """Retourne l'objet widget pour accéder à ses propriétés."""
        return self._dbWidget

    def getSelection(self):
        """Retourne la ou les partition(s) sélectionnée(s)."""
        if type(self._dbWidget.curselection()) is tuple:
            return [_ + 1 for _ in self._dbWidget.curselection()]
        else:
            return self._dbWidget.curselection() + 1

    def update(self):
        """Efface la liste et la remplit avec les partitions de la base de données."""
        self._dbWidget.delete(0, END)
        partitions = files.getPartitions()
        if partitions[0]:
            for partition in partitions[1]:
                self._dbWidget.insert(partition[0], partition[1])


mainmenu = MainMenuWindow(root)  # Ouverture du menu principal
root.mainloop()  # Boucle TkInter.
