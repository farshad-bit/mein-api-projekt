# app/utils/validators/image/validate_date_format.py

from datetime import datetime
from flask import current_app

def validate_date_format(date_str):
    """
    Überprüft, ob das Datum im Format YYYY-MM-DD HH:MM:SS vorliegt.
    
    :param date_str: Das zu überprüfende Datum als String
    :return: Das konvertierte Datum, wenn gültig, sonst False
    """
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        current_app.logger.error(f"Ungültiges Datumsformat: {date_str}")
        return False
