# app/utils/validators/image/validate_tags_length.py

from flask import current_app

def validate_tags_length(tags, max_length=255):
    """
    Überprüft, ob die Tags die maximale Länge nicht überschreiten.
    
    :param tags: Die zu überprüfenden Tags
    :param max_length: Maximale Länge der Tags (Standard: 255 Zeichen)
    :return: True, wenn die Länge gültig ist, sonst False
    """
    if tags and len(tags) > max_length:
        current_app.logger.error(f"Tags zu lang: {len(tags)} Zeichen")
        return False
    return True
