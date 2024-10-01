# app/utils/validators/image/validate_image_format.py

from flask import current_app
from PIL import Image

def validate_image_format(image_file):
    """
    Überprüft, ob die Datei tatsächlich ein Bild ist.
    
    :param image_file: Bilddatei, die geprüft wird
    :return: True, wenn das Bildformat gültig ist, sonst False
    """
    try:
        with Image.open(image_file) as img:
            img.verify()  # Überprüft das Bildformat
        return True
    except Exception as e:
        current_app.logger.error(f"Error validating image format: {str(e)}")
        return False
