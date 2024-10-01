from flask import jsonify, current_app, Blueprint
from app import db
from app.models.patient import Patient
from app.utils.validators.patient import can_delete_patient

patient_delete_bp = Blueprint('patient_delete_bp', __name__)

@patient_delete_bp.route('/patients/<int:id>', methods=['DELETE'])
def delete_patient(id):
    # Sucht den Patienten mit der angegebenen ID in der Datenbank
    patient = Patient.query.get_or_404(id)

    # Überprüfen, ob der Patient gelöscht werden kann (z.B. keine zugehörigen Bilder)
    can_delete, error_message = can_delete_patient(id)
    if not can_delete:
        return jsonify({"error": error_message}), 400

    # Löscht den gefundenen Patienten aus der Datenbank
    try:
        db.session.delete(patient)
        db.session.commit()
        current_app.logger.info(f"Patient mit ID {id} erfolgreich gelöscht.")
        return jsonify({"message": f"Patient mit ID {id} erfolgreich gelöscht"}), 200
    except Exception as e:
        current_app.logger.error(f"Fehler beim Löschen des Patienten mit ID {id}: {str(e)}")
        return jsonify({"error": f"Fehler beim Löschen des Patienten: {str(e)}"}), 500
