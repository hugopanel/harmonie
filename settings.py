# Fichier : settings.py
# Nom : Propriétés
# Auteurs : Hugo PANEL, Mohamed ZAMMIT CHATTI
# Description :
"""
Ce fichier regroupe les fonctions et variables du fichier de configuration *user/settings.json*.
"""

import json
import files


Settings = ""
try:
    with open("user/settings.json", "r") as _settings:
        _settings = _settings.readlines()
        if len(_settings) > 1:
            # On convertit en string en enlevant les retours à la ligne ('\n') :
            _settings = ''.join(i[:-1] if i[-1] == '\n' else i for i in _settings)
        else:
            _settings = _settings[0]  # Conversion en string
        try:
            Settings = json.loads(_settings)
        except:
            print("Format JSON incorrect.")
            exit(0)
except IOError:
    print("Le fichier de configuration est introuvable.")
    exit(0)

scores_path = "user/" + Settings["user"]["scores_file"]


def saveSettings():
    """Sauvegarde les paramètres dans le fichier de configuration.
    Retourne :
        bool: False : en cas d'erreur."""
    content = json.dumps(Settings, ensure_ascii=False)
    # Si files.replaceFile retourne False, on retourne False aussi :
    return files.replaceFile("user/settings.json", content)
