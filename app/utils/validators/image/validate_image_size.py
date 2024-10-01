# app/utils/validators/image/validate_image_size.py

from flask import current_app
from PIL import Image

def validate_image_size(image_file, max_width=3840, max_height=2160):
    """
    Überprüft, ob die Bildgröße (Breite/Höhe) die maximale Breite und Höhe nicht überschreitet.
    
    :param image_file: Geöffnete Bilddatei
    :param max_width: Maximale Breite des Bildes
    :param max_height: Maximale Höhe des Bildes
    :return: True, wenn die Bildgröße gültig ist, sonst False
    """
    try:
        with Image.open(image_file) as img:
            width, height = img.size
            return width <= max_width and height <= max_height
    except Exception as e:
        current_app.logger.error(f"Error validating image size: {str(e)}")
        return False
