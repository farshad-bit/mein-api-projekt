# Datei: tests/conftest.py

import pytest
from app import create_app  # Korrekt
from app.db import db as _db 
from app.models.patient import Patient
from app.models.image import Image
import uuid
from datetime import date

@pytest.fixture(scope='session')
def app():
    """Erstellt die Flask-App im Testmodus."""
    app = create_app('testing')
    return app

@pytest.fixture(scope='function')
def db(app):
    """Erstellt eine frische Datenbank für jeden Test."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()
        _db.engine.dispose() 

@pytest.fixture(scope='function')
def client(app, db):
    """Erstellt einen Test-Client für die App."""
    return app.test_client()

@pytest.fixture(scope='function')
def app_context(app):
    """Aktiviert den Anwendungskontext für einen Test."""
    with app.app_context():
        yield

@pytest.fixture(scope='function')
def new_patient(db):
    """Erstellt einen neuen Patienten für Tests."""
    patient = Patient(
        first_name='John',
        last_name='Doe',
        dob=date(1990, 1, 1),
        gender='male',
        title='Mr.',
        physician='Dr. Smith',
        ancestry='European',
        inconsistency=None,
        eyeid=str(uuid.uuid4())
    )
    db.session.add(patient)
    db.session.commit()
    return patient

@pytest.fixture(scope='function')
def new_image(db, new_patient):
    """Erstellt ein neues Bild, das einem Patienten zugeordnet ist."""
    image = Image(
        image_path='uploads/test_image.jpg',
        patient_id=new_patient.id,
        description='A sample image',
        tags='sample, test'
    )
    db.session.add(image)
    db.session.commit()
    return image


