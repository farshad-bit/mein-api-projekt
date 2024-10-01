# controllers/patient/patient_create.py

from flask import request, jsonify, Blueprint
from app.db import db
from app.models.patient import Patient
from app.utils.validators.patient import validate_patient_data  # Importiere die Validierung
from datetime import datetime

patient_create_bp = Blueprint('patient_create_bp', __name__)

@patient_create_bp.route('/patients', methods=['POST'])
def create_patient():
    # Die vom Client gesendeten JSON-Daten werden abgerufen
    data = request.get_json()

    # Nutze die Validierungsfunktion
    is_valid, error_message = validate_patient_data(data)
    
    if not is_valid:
        return jsonify({"error": error_message}), 400

    try:
        # Das Geburtsdatum wird in ein Datum konvertiert; Fehler bei ungültigem Format wird behandelt
        dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Ein neues Patientenobjekt wird erstellt und mit den übergebenen Daten befüllt
    new_patient = Patient(
        first_name=data['first_name'],
        last_name=data['last_name'],
        title=data['title'],
        dob=dob,
        gender=data['gender'],
        physician=data['physician'],
        ancestry=data['ancestry'],
        inconsistency=data['inconsistency'],
        eyeid=data['eyeid']
    )

    # Der neue Patient wird zur Datenbank hinzugefügt und die Änderungen werden gespeichert
    try:
        db.session.add(new_patient)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error: " + str(e)}), 500

    # Erfolgsmeldung wird zurückgegeben
    return jsonify({"message": "Patient erfolgreich erstellt"}), 201

