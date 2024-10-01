from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models.image import Image
from app.models.patient import Patient
from werkzeug.utils import secure_filename
from app.services.image_service import create_thumbnail
from app.utils.validators.image import (
    is_valid_filename,
    allowed_file_extension,
    validate_image_size,
    validate_image_format,
    validate_file_size,
    is_writable
)
import os
import logging

# Erstelle einen Blueprint für den Image Controller
image_add_bp = Blueprint('image_add_bp', __name__)

@image_add_bp.route('/patients/<int:patient_id>/images', methods=['POST'])
def add_image(patient_id):
    # Setze die maximale Dateigröße in der Konfiguration innerhalb des Application Contexts
    current_app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

    # Überprüfe, ob der Patient existiert
    patient = Patient.query.get_or_404(patient_id)

    # Prüfen, ob eine Bilddatei hochgeladen wurde
    if 'image_path' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image_path']
    filename = image_file.filename

    # Validierung: Dateiname
    if not is_valid_filename(filename):
        current_app.logger.error(f"Invalid filename: {filename}")
        return jsonify({"error": "Invalid filename"}), 400

    # Validierung: Dateiendung
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if not allowed_file_extension(filename, allowed_extensions):
        current_app.logger.error(f"Invalid file extension: {filename}")
        return jsonify({"error": "Invalid file extension"}), 400

    # Validierung: Bildformat
    if not validate_image_format(image_file):
        current_app.logger.error(f"Invalid image format for file: {filename}")
        return jsonify({"error": "Invalid image format"}), 400

    # Validierung: Bildgröße (Breite/Höhe)
    if not validate_image_size(image_file, max_width=3840, max_height=2160):
        current_app.logger.error(f"Image size exceeds limits for file: {filename}")
        return jsonify({"error": "Image size exceeds the maximum allowed width or height"}), 400

    # Validierung: Dateigröße
    max_size = current_app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)  # Standard: 16 MB
    if not validate_file_size(image_file, max_size=max_size):
        current_app.logger.error(f"File size exceeds limit for patient {patient_id}")
        return jsonify({"error": f"File size exceeds the limit of {max_size / (1024 * 1024)} MB"}), 413

    # Sicherer Dateiname
    filename = secure_filename(filename)

    # Speicherpfad für den Patienten (z.B. 'uploads/<patient_id>')
    upload_dir = os.path.join('uploads', str(patient_id))
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Überprüfe, ob das Verzeichnis beschreibbar ist
    if not is_writable(upload_dir):
        current_app.logger.error(f"Upload directory is not writable for patient {patient_id}")
        return jsonify({"error": "Upload directory is not writable"}), 500

    image_path = os.path.join(upload_dir, filename)

    # Datei speichern
    try:
        image_file.save(image_path)
        current_app.logger.info(f"Image saved successfully for patient {patient_id} at {image_path}")
    except Exception as e:
        current_app.logger.error(f"Failed to save image for patient {patient_id}: {str(e)}")
        return jsonify({"error": f"Failed to save image: {str(e)}"}), 500

    # Thumbnail erstellen
    try:
        thumbnail_path = create_thumbnail(image_path)
        current_app.logger.info(f"Thumbnail created successfully for {image_path}")
    except Exception as e:
        current_app.logger.error(f"Thumbnail creation failed for {image_path}: {str(e)}")
        return jsonify({"error": f"Failed to create thumbnail: {str(e)}"}), 500

    # Neues Bild in der Datenbank speichern
    new_image = Image(image_path=image_path, patient_id=patient.id)
    db.session.add(new_image)
    db.session.commit()

    current_app.logger.info(f"Image entry added to the database for patient {patient_id}")

    return jsonify({"message": "Bild erfolgreich hinzugefügt", "thumbnail_path": thumbnail_path}), 201
