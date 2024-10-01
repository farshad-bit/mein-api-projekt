# app/models/patient.py

from app.db import db

class Patient(db.Model):
    __tablename__ = 'patients'

    # Primärschlüssel
    id = db.Column(db.Integer, primary_key=True)
    
    # Vorname des Patienten
    first_name = db.Column(db.String(50), nullable=False)
    
    # Nachname des Patienten
    last_name = db.Column(db.String(50), nullable=False, index=True)  # Index auf last_name hinzugefügt
    
    # Geburtsdatum
    dob = db.Column(db.Date, nullable=False)
    
    # Geschlecht des Patienten
    gender = db.Column(db.String(10), nullable=False)
    
    # Titel des Patienten (z.B. Dr., Prof.)
    title = db.Column(db.String(10), nullable=True)
    
    # Zu behandelnder Arzt
    physician = db.Column(db.String(100), nullable=True)
    
    # Abstammung des Patienten
    ancestry = db.Column(db.String(100), nullable=True)
    
    # Eventuelle Inkonsistenzen in den Daten
    inconsistency = db.Column(db.String(255), nullable=True)
    
    # Eindeutige ID für das Auge (EyeID)
    eyeid = db.Column(db.String(100), unique=True, index=True)  # Eindeutigkeit und Index auf eyeid
    
    # Die serialize-Methode wandelt die Patientendaten in ein JSON-Format um
    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'dob': self.dob.strftime('%Y-%m-%d'),  # Konvertiert das Datum in ein lesbares Format
            'gender': self.gender,
            'title': self.title,
            'physician': self.physician,
            'ancestry': self.ancestry,
            'inconsistency': self.inconsistency,
            'eyeid': self.eyeid 
        }
