from flask import request, jsonify, current_app, Blueprint
from app import db
from app.models.patient import Patient
from datetime import datetime
from app.utils.validators.patient import validate_patient_data

patient_update_bp = Blueprint('patient_update_bp', __name__)

@patient_update_bp.route('/patients/<int:id>', methods=['PUT'])
def update_patient(id):
    # Suche nach dem Patienten
    patient = Patient.query.get_or_404(id)
    
    # JSON-Daten des Antrags erhalten
    data = request.get_json()

    # Validierung der Patientendaten
    is_valid, error_message = validate_patient_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    # Patientendaten aktualisieren
    patient.first_name = data.get('first_name', patient.first_name)
    patient.last_name = data.get('last_name', patient.last_name)
    patient.title = data.get('title', patient.title)
    patient.dob = datetime.strptime(data['dob'], '%Y-%m-%d').date() if 'dob' in data else patient.dob
    patient.gender = data.get('gender', patient.gender)
    patient.physician = data.get('physician', patient.physician)
    patient.ancestry = data.get('ancestry', patient.ancestry)
    patient.inconsistency = data.get('inconsistency', patient.inconsistency)
    patient.eyeid = data.get('eyeid', patient.eyeid)

    # Änderungen in der Datenbank speichern
    db.session.commit()

    return jsonify({"message": "Patient erfolgreich aktualisiert"}), 200
