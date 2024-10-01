# app/utils/validators/image/validate_file_size.py

from flask import current_app
import os

def validate_file_size(file, max_size=16 * 1024 * 1024):
    """
    Überprüft, ob die Datei die maximale Größe nicht überschreitet.
    
    :param file: Datei, die geprüft wird
    :param max_size: Maximale Dateigröße in Bytes
    :return: True, wenn die Dateigröße gültig ist, sonst False
    """
    try:
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Setzt den Dateizeiger wieder an den Anfang
        return file_size <= max_size
    except Exception as e:
        current_app.logger.error(f"Error validating file size: {str(e)}")
        return False
