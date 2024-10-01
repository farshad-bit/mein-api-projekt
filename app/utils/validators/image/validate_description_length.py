# app/utils/validators/image/validate_description_length.py

from flask import current_app

def validate_description_length(description, max_length=255):
    """
    Überprüft, ob die Beschreibung die maximale Länge nicht überschreitet.
    
    :param description: Die zu überprüfende Beschreibung
    :param max_length: Maximale Länge der Beschreibung (Standard: 255 Zeichen)
    :return: True, wenn die Länge gültig ist, sonst False
    """
    if description and len(description) > max_length:
        current_app.logger.error(f"Beschreibung zu lang: {len(description)} Zeichen")
        return False
    return True
