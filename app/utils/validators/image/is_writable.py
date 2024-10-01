# app/utils/validators/image/is_writable.py

from flask import current_app
import os

def is_writable(path):
    """
    Überprüft, ob das Verzeichnis am angegebenen Pfad beschreibbar ist.
    
    :param path: Pfad zum Verzeichnis
    :return: True, wenn das Verzeichnis beschreibbar ist, sonst False
    """
    try:
        testfile = os.path.join(path, "testfile")
        with open(testfile, 'w') as f:
            pass
        os.remove(testfile)
        return True
    except Exception as e:
        current_app.logger.error(f"Error checking if directory is writable: {str(e)}")
        return False
