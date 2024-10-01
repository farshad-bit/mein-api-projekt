# app/utils/validators/image/is_valid_filename.py

import re

def is_valid_filename(filename):
    """
    Überprüft, ob der Dateiname gültig ist.
    Ein gültiger Dateiname enthält nur Buchstaben, Ziffern, Bindestriche, Unterstriche und Punkte.
    """
    return bool(re.match(r'^[\w\-.]{1,255}$', filename))
