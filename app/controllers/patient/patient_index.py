# controllers/patient/patient_index.py

from flask import Blueprint

# Erstelle einen Blueprint für die Startseite
index_bp = Blueprint('index_bp', __name__)

# Route für die Startseite (GET /)
@index_bp.route('/')
def index():
    # Eine einfache Begrüßung auf der Startseite der API
    return "Willkommen zur Patient API! Verwende /patients, um Patientendaten abzurufen."
