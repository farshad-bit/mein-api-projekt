# app/controllers/file_controller.py

import os
from flask import Blueprint, send_from_directory, jsonify, abort

# Erstelle einen Blueprint für den File Controller
file_bp = Blueprint('file_bp', __name__)

# Absoluter Pfad zu deinem Upload-Verzeichnis
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

# Stelle sicher, dass das Upload-Verzeichnis existiert
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route zum Bereitstellen von hochgeladenen Bildern
@file_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    # Überprüfe, ob der Pfad sicher ist (verhindert, dass man außerhalb des Verzeichnisses zugreifen kann)
    if not os.path.isfile(os.path.join(UPLOAD_FOLDER, filename)):
        return jsonify({"error": "File not found"}), 404

    # Sende die Datei aus dem Upload-Verzeichnis
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except FileNotFoundError:
        abort(404)
