# Datei: tests/test_patient_model.py

import pytest
from app.models.patient import Patient
from app import db
from datetime import date

def test_patient_creation(app_context, db):
    """Testet die Erstellung und Speicherung eines neuen Patienten in der Datenbank."""
    patient = Patient(
        first_name='Max',
        last_name='Mustermann',
        dob=date(1985, 5, 15),
        gender='male',
        title='Dr.',
        physician='Dr. Müller',
        ancestry='European',
        inconsistency=None,
        eyeid='unique_eyeid_12345'
    )
    db.session.add(patient)
    db.session.commit()

    # Überprüfe, ob der Patient in der Datenbank gespeichert wurde
    saved_patient = Patient.query.filter_by(eyeid='unique_eyeid_12345').first()
    assert saved_patient is not None
    assert saved_patient.first_name == 'Max'
    assert saved_patient.last_name == 'Mustermann'
    assert saved_patient.dob.strftime('%Y-%m-%d') == '1985-05-15'
    assert saved_patient.gender == 'male'
    assert saved_patient.title == 'Dr.'
    assert saved_patient.physician == 'Dr. Müller'
    assert saved_patient.ancestry == 'European'
    assert saved_patient.inconsistency is None
    assert saved_patient.eyeid == 'unique_eyeid_12345'

def test_patient_serialization(new_patient):
    """Testet die Serialisierung eines Patientenobjekts."""
    serialized_data = new_patient.serialize()
    assert isinstance(serialized_data, dict)
    assert serialized_data['first_name'] == 'John'
    assert serialized_data['last_name'] == 'Doe'
    assert serialized_data['dob'] == '1990-01-01'
    assert serialized_data['gender'] == 'male'
    assert serialized_data['title'] == 'Mr.'
    assert serialized_data['physician'] == 'Dr. Smith'
    assert serialized_data['ancestry'] == 'European'
    assert serialized_data['inconsistency'] is None
    assert 'eyeid' in serialized_data
    assert 'id' in serialized_data
