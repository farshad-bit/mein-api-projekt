import os
from werkzeug.utils import secure_filename
from flask import current_app
from .is_valid_filename import is_valid_filename
from .allowed_file_extension import allowed_file_extension
from .validate_file_size import validate_file_size

# Überprüfe und validiere den neuen Bildpfad
def validate_image_path(new_path, allowed_extensions, max_size):
    """
    Überprüft und validiert den neuen Bildpfad (Dateiname, Endung, Dateigröße).
    
    :param new_path: Der vom Benutzer angegebene neue Pfad
    :param allowed_extensions: Liste der erlaubten Dateiendungen
    :param max_size: Maximale Dateigröße in Bytes
    :return: True, wenn die Validierung erfolgreich ist, sonst False mit einer Fehlermeldung
    """
    # Sichere den neuen Dateinamen
    new_filename = secure_filename(os.path.basename(new_path))

    # Validierung des Dateinamens
    if not is_valid_filename(new_filename):
        current_app.logger.warning(f"Invalid filename: {new_filename}")
        return False, "Invalid filename"

    # Überprüfe die Dateiendung
    if not allowed_file_extension(new_filename, allowed_extensions):
        current_app.logger.warning(f"Invalid file extension: {new_filename}")
        return False, "Invalid file extension. Allowed types are: " + ", ".join(allowed_extensions)

    # Überprüfe die Dateigröße
    if not os.path.exists(new_path):
        return False, "File does not exist"

    if not validate_file_size(open(new_path, 'rb'), max_size):
        current_app.logger.warning(f"File size exceeds limit for: {new_filename}")
        return False, f"File size exceeds the limit of {max_size / (1024 * 1024)} MB"

    return True, None
