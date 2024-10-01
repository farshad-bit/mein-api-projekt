# app/controllers/image/image_delete.py

from flask import jsonify, current_app, Blueprint
from app import db
from app.models.image import Image
from app.utils.validators.image import validate_image_format, is_writable
import os
import logging

image_delete_bp = Blueprint('image_delete_bp', __name__)

@image_delete_bp.route('/images/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    current_app.logger.debug(f"Delete request received for image ID: {image_id}")

    # Suche nach dem Bild in der Datenbank
    image = db.session.get(Image, image_id)
    if not image:
        current_app.logger.debug(f"Image ID {image_id} not found")
        return jsonify({"error": "Image not found"}), 404

    # Pfad des Bildes und Thumbnails
    image_path = image.image_path
    thumbnail_path = os.path.join(os.path.dirname(image_path), 'thumbnails', os.path.basename(image_path))

    # Überprüfung, ob das Verzeichnis beschreibbar ist, bevor versucht wird, Dateien zu löschen
    if not is_writable(os.path.dirname(image_path)):
        current_app.logger.error(f"Verzeichnis nicht beschreibbar: {os.path.dirname(image_path)}")
        return jsonify({"error": "Directory not writable"}), 500

    # Versuch, das Thumbnail zu löschen
    try:
        if os.path.exists(thumbnail_path):
            if validate_image_format(thumbnail_path):
                os.remove(thumbnail_path)
                current_app.logger.info(f"Thumbnail {thumbnail_path} gelöscht.")
            else:
                current_app.logger.warning(f"Ungültiges Format für Thumbnail {thumbnail_path}.")
        else:
            current_app.logger.warning(f"Thumbnail {thumbnail_path} nicht gefunden.")
    except Exception as e:
        current_app.logger.error(f"Fehler beim Löschen des Thumbnails {thumbnail_path}: {str(e)}")
        return jsonify({"error": f"Failed to delete thumbnail: {str(e)}"}), 500

    # Versuch, das Bild zu löschen
    try:
        if os.path.exists(image_path):
            if validate_image_format(image_path):
                os.remove(image_path)
                current_app.logger.info(f"Bild {image_path} gelöscht.")
            else:
                current_app.logger.warning(f"Ungültiges Format für Bild {image_path}.")
                return jsonify({"error": "Invalid file format"}), 400
        else:
            current_app.logger.warning(f"Bild {image_path} nicht gefunden.")
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        current_app.logger.error(f"Fehler beim Löschen des Bildes {image_path}: {str(e)}")
        return jsonify({"error": f"Failed to delete file: {str(e)}"}), 500

    # Löschen des Eintrags in der Datenbank
    try:
        db.session.delete(image)
        db.session.commit()
        current_app.logger.info(f"Bild mit ID {image_id} erfolgreich aus der Datenbank gelöscht.")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Fehler beim Löschen des Datenbank-Eintrags für Bild mit ID {image_id}: {str(e)}")
        return jsonify({"error": f"Failed to delete database entry: {str(e)}"}), 500

    return jsonify({"message": "Bild und Thumbnail erfolgreich gelöscht"}), 200
