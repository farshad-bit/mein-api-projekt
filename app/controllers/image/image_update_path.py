# app/controllers/image/image_update_path.py
from flask import request, jsonify, current_app, Blueprint
from app import db
from app.models.image import Image
from werkzeug.utils import secure_filename
from app.utils.validators.image import validate_image_path  # Importiere die Validierung
import os
import logging


image_update_path_bp = Blueprint('image_update_path_bp', __name__)

@image_update_path_bp.route('/images/<int:image_id>/update_path', methods=['PUT'])
def update_image_path(image_id):
    # Suche nach dem Bild in der Datenbank
    image = Image.query.get_or_404(image_id)

    # Hole den neuen Pfad aus der Anfrage
    data = request.get_json()
    new_path = data.get('image_path', None)

    if not new_path:
        current_app.logger.warning(f"No image path provided for image {image_id}")
        return jsonify({"error": "Image path is required"}), 400

    # Validierungslogik für den neuen Bildpfad
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    max_size = current_app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)  # 16 MB
    is_valid, error_message = validate_image_path(new_path, allowed_extensions, max_size)

    if not is_valid:
        return jsonify({"error": error_message}), 400

    # Verschieben der Datei, falls der alte Pfad existiert
    old_path = image.image_path
    if not os.path.exists(old_path):
        current_app.logger.warning(f"Old file not found at {old_path} for image {image_id}")
        return jsonify({"error": "File does not exist"}), 404

    try:
        os.rename(old_path, new_path)
        current_app.logger.info(f"File successfully moved from {old_path} to {new_path} for image {image_id}")
    except Exception as e:
        current_app.logger.error(f"Failed to move file for image {image_id}: {str(e)}")
        return jsonify({"error": f"Failed to move file: {str(e)}"}), 500

    # Aktualisiere den Bildpfad in der Datenbank
    image.image_path = new_path
    db.session.commit()

    current_app.logger.info(f"Image path successfully updated in database for image {image_id}")

    return jsonify({"message": "Bildpfad erfolgreich aktualisiert"}), 200
