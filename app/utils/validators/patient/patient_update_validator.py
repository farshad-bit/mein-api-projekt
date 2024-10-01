import re
from datetime import datetime
from flask import jsonify
from app.models.patient import Patient

def validate_patient_data(data):
    """
    Überprüft die Eingabedaten für das Erstellen eines Patienten.
    
    :param data: Die JSON-Daten für den Patienten
    :return: Ein Tuple (True, None) wenn alles OK ist, sonst (False, Fehlernachricht)
    """
    required_fields = ['first_name', 'last_name', 'dob', 'gender', 'title', 'physician', 'ancestry', 'inconsistency', 'eyeid']
    
    # Überprüfe, ob alle erforderlichen Felder vorhanden sind
    for field in required_fields:
        if field not in data:
            return False, f"Missing data for {field}"

    # Validierung von Namen (keine Sonderzeichen, max. Länge 100)
    name_pattern = r'^[A-Za-z\s\-]{1,100}$'
    if not re.match(name_pattern, data['first_name']):
        return False, "Invalid first name. Only letters, spaces, and hyphens are allowed, max 100 characters."
    if not re.match(name_pattern, data['last_name']):
        return False, "Invalid last name. Only letters, spaces, and hyphens are allowed, max 100 characters."

    # Validierung des Geburtsdatums (Erwartetes Format: YYYY-MM-DD)
    try:
        datetime.strptime(data['dob'], '%Y-%m-%d').date()
    except ValueError:
        return False, "Invalid date format. Expected YYYY-MM-DD."

    # Validierung von gender (nur bestimmte Werte erlaubt)
    if data['gender'] not in ['male', 'female', 'other']:
        return False, "Invalid gender. Expected 'male', 'female', or 'other'."

    # Überprüfen, ob die eyeid bereits existiert
    if Patient.query.filter_by(eyeid=data['eyeid']).first():
        return False, "eyeid already exists. It must be unique."

    # Validierung der Titel- und Physiciandaten (Länge max. 255 Zeichen)
    if len(data['title']) > 255 or len(data['physician']) > 255:
        return False, "Title and physician should be less than 255 characters."

    # Wenn alles gültig ist
    return True, None
