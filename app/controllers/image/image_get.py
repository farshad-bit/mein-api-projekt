# app/controllers/image/image_get.py

from flask import request, jsonify, current_app, Blueprint
from app.models.image import Image
from app.models.patient import Patient
from app.utils.validators.image import validate_pagination_parameters

# Erstelle den Blueprint für diesen Controller
image_get_bp = Blueprint('image_get_bp', __name__)

@image_get_bp.route('/patients/<int:patient_id>/images', methods=['GET'])
def get_images(patient_id):
    # Überprüfe, ob der Patient existiert
    patient = Patient.query.get_or_404(patient_id)

    # Pagination-Parameter abrufen (Standardwerte: Seite 1, 10 Einträge pro Seite)
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
    except ValueError:
        current_app.logger.error("Ungültige Werte für page oder per_page")
        return jsonify({"error": "Ungültige Werte für page oder per_page"}), 400

    # Validierung der Paginierungsparameter
    valid, error_message = validate_pagination_parameters(page, per_page)
    if not valid:
        return jsonify({"error": error_message}), 400

    # Abrufen aller Bilder, die dem Patienten zugeordnet sind, mit Pagination
    images_query = Image.query.filter_by(patient_id=patient_id).paginate(page=page, per_page=per_page)

    # Überprüfen, ob Bilder vorhanden sind
    if not images_query.items:
        return jsonify({"message": f"Keine Bilder für den Patienten mit der ID {patient_id} gefunden"}), 404

    # JSON-Antwort vorbereiten
    response = {
        "page": images_query.page,
        "per_page": images_query.per_page,
        "total_pages": images_query.pages,
        "total_images": images_query.total,
        "images": [image.serialize() for image in images_query.items]
    }

    return jsonify(response), 200

