# controllers/patient/patient_get.py

from flask import jsonify, current_app, Blueprint
from app import db
from app.models.patient import Patient
from app.utils.validators.patient import validate_patient_id

patient_get_bp = Blueprint('patient_get_bp', __name__)

@patient_get_bp.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    # Überprüfe, ob die Patient-ID gültig ist
    is_valid, error_message = validate_patient_id(patient_id)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    # Sucht den Patienten mit der angegebenen ID in der Datenbank
    # Wenn der Patient nicht existiert, wird automatisch eine 404-Fehlermeldung zurückgegeben
    patient = Patient.query.get_or_404(patient_id)  # Hier den Parameter ändern

    # Rückgabe der Patientendaten als JSON-Antwort
    # serialize() ist eine Methode, die das Patient-Objekt in ein JSON-Format umwandelt
    return jsonify(patient.serialize()), 200

