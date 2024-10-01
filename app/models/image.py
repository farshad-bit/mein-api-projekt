# app/models/image.py
from app.db import db
from datetime import datetime

class Image(db.Model):
    __tablename__ = 'images'

    # Primärschlüssel
    id = db.Column(db.Integer, primary_key=True)
    
    # Pfad zum Bild
    image_path = db.Column(db.String(255), nullable=False)
    
    # Datum der Aufnahme, standardmäßig auf das aktuelle Datum gesetzt
    date_taken = db.Column(db.DateTime, default=datetime.utcnow)

    # Bildbeschreibung mit einer maximalen Länge von 255 Zeichen
    description = db.Column(db.String(255), nullable=True)

    # Tags für das Bild, ebenfalls auf 255 Zeichen beschränkt
    tags = db.Column(db.String(255), nullable=True)

    # Fremdschlüssel zur Patienten-Tabelle (patients), Index hinzufügen für schnellere Abfragen
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False, index=True)

    # Index hinzufügen: Sorgt für schnellere Abfragen basierend auf den Tags
    # Wenn du viele Abfragen auf Tags machst, könnte dies die Abfragegeschwindigkeit verbessern
    __table_args__ = (
        db.Index('idx_tags', tags),
    )

    def serialize(self):
        return {
            'id': self.id,
            'image_path': self.image_path,
            'date_taken': self.date_taken,
            'patient_id': self.patient_id,
            'description': self.description,
            'tags': self.tags
        }
