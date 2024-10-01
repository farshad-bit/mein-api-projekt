# Adresse: create_tables.py

from app import db, app
from app.models.patient import Patient
from app.models.image import Image

# Tabellen in der Datenbank erstellen
with app.app_context():
    db.create_all()
    print("Tabellen wurden erstellt.")
