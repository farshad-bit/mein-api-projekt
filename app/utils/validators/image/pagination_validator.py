
from flask import jsonify, current_app

def validate_pagination_parameters(page, per_page, max_per_page=100):
    """
    Validiert die Paginierungsparameter.

    :param page: Aktuelle Seite (Integer)
    :param per_page: Anzahl der Elemente pro Seite (Integer)
    :param max_per_page: Maximale Anzahl der Elemente pro Seite (Standard: 100)
    :return: Tuple (valid, error_message) -> True/False und None bei Erfolg, False und Fehlermeldung bei Fehler.
    """
    if page < 1 or per_page < 1 or per_page > max_per_page:
        current_app.logger.error(f"Ungültige Paginierungsparameter: page={page}, per_page={per_page}")
        return False, "Ungültige Paginierungsparameter. Seite und Einträge pro Seite müssen positiv sein, und pro Seite dürfen nicht mehr als 100 Einträge abgefragt werden."
    
    return True, None
