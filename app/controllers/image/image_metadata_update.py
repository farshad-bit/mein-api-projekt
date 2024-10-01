# app/controllers/image/image_metadata_update.py

from flask import request, jsonify, current_app, Blueprint
from app import db
from app.models.image import Image
from app.utils.validators.image import validate_date_format
from app.utils.validators.image import validate_description_length
from app.utils.validators.image import validate_tags_length

image_metadata_update_bp = Blueprint('image_metadata_update_bp', __name__)

@image_metadata_update_bp.route('/images/<int:image_id>/metadata', methods=['PUT'])
def update_image_metadata(image_id):
    # Suche nach dem Bild in der Datenbank
    image = Image.query.get_or_404(image_id)
    
    # Hole die Metadaten, die aktualisiert werden sollen
    data = request.get_json()

    # Validierung: Sicherstellen, dass der JSON-Body nicht leer ist
    if not data:
        current_app.logger.error(f"Leere JSON-Daten für Bild {image_id}")
        return jsonify({"error": "Leere Daten. Es müssen Metadaten zur Aktualisierung übergeben werden."}), 400

    # Validierung: Überprüfen des Datumsformats
    if 'date_taken' in data:
        date_taken = validate_date_format(data['date_taken'])
        if not date_taken:
            return jsonify({"error": "Ungültiges Datumsformat. Erwartet wird YYYY-MM-DD HH:MM:SS."}), 400
        image.date_taken = date_taken

    # Validierung: Überprüfen der Beschreibung (maximale Länge 255 Zeichen)
    description = data.get('description', image.description)
    if not validate_description_length(description):
        return jsonify({"error": "Beschreibung darf maximal 255 Zeichen lang sein."}), 400
    image.description = description

    # Validierung: Überprüfen der Tags (maximale Länge 255 Zeichen)
    tags = data.get('tags', image.tags)
    if not validate_tags_length(tags):
        return jsonify({"error": "Tags dürfen maximal 255 Zeichen lang sein."}), 400
    image.tags = tags

    # Speichern der aktualisierten Daten in der Datenbank
    try:
        db.session.commit()
        current_app.logger.info(f"Bildmetadaten für Bild {image_id} erfolgreich aktualisiert.")
        return jsonify({"message": "Bildmetadaten erfolgreich aktualisiert"}), 200
    except Exception as e:
        current_app.logger.error(f"Fehler beim Speichern der Bildmetadaten für Bild {image_id}: {str(e)}")
        return jsonify({"error": "Fehler beim Speichern der Metadaten"}), 500
