# tests/patient/test_patient_create.py

import pytest
from flask import url_for

def test_create_patient_success(client):
    """
    Testet den erfolgreichen Fall, in dem ein Patient erfolgreich erstellt wird.
    """
    # Beispiel-Daten für einen neuen Patienten
    new_patient_data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "title": "Ms.",
        "dob": "1985-05-15",
        "gender": "female",
        "physician": "Dr. Alice",
        "ancestry": "Asian",
        "inconsistency": None,
        "eyeid": "12345678-1234-5678-1234-567812345678"
    }

    # Sende eine POST-Anfrage, um den neuen Patienten zu erstellen
    response = client.post(
        url_for('patient_create_bp.create_patient'),
        json=new_patient_data
    )

    # Überprüfen, ob der Statuscode 201 ist (Erfolg)
    assert response.status_code == 201
    assert response.is_json
    assert response.json['message'] == "Patient erfolgreich erstellt"


def test_create_patient_invalid_data(client):
    """
    Testet den Fall, in dem ungültige Patientendaten gesendet werden.
    """
    # Beispiel-Daten mit fehlendem Vor- und Nachnamen
    invalid_patient_data = {
        "first_name": "",
        "last_name": "",
        "title": "Mr.",
        "dob": "1990-01-01",
        "gender": "male",
        "physician": "Dr. Bob",
        "ancestry": "European",
        "inconsistency": None,
        "eyeid": "87654321-1234-5678-1234-567812345678"
    }

    # Sende die POST-Anfrage mit ungültigen Daten
    response = client.post(
        url_for('patient_create_bp.create_patient'),
        json=invalid_patient_data
    )

    # Überprüfen, ob der Statuscode 400 ist (Bad Request)
    assert response.status_code == 400
    assert response.is_json
    assert 'error' in response.json

def test_create_patient_invalid_date_format(client):
    """
    Testet den Fall, in dem das Geburtsdatum in einem ungültigen Format gesendet wird.
    """
    # Beispiel-Daten mit einem ungültigen Geburtsdatum
    invalid_date_data = {
        "first_name": "John",
        "last_name": "Doe",
        "title": "Mr.",
        "dob": "15-05-1985",  # Falsches Format (DD-MM-YYYY)
        "gender": "male",
        "physician": "Dr. Bob",
        "ancestry": "European",
        "inconsistency": None,
        "eyeid": "87654321-1234-5678-1234-567812345678"
    }

    # Sende die POST-Anfrage mit ungültigem Datum
    response = client.post(
        url_for('patient_create_bp.create_patient'),
        json=invalid_date_data
    )

    # Überprüfen, ob der Statuscode 400 ist und die Fehlermeldung korrekt ist
    assert response.status_code == 400
    assert response.is_json
    assert response.json['error'] == "Invalid date format. Expected YYYY-MM-DD."

def test_create_patient_db_error(client, monkeypatch):
    """
    Testet den Fall, in dem ein Datenbankfehler auftritt (sollte 500 zurückgeben).
    """

    # Simuliere einen Datenbankfehler
    def mock_commit():
        raise Exception("Database connection lost")

    # Patch db.session.commit, um den Fehler zu simulieren
    monkeypatch.setattr('app.db.session.commit', mock_commit)  # Korrigierter Pfad

    # Beispiel-Daten für einen neuen Patienten
    new_patient_data = {
        "first_name": "John",
        "last_name": "Doe",
        "title": "Mr.",
        "dob": "1990-01-01",
        "gender": "male",
        "physician": "Dr. Smith",
        "ancestry": "European",
        "inconsistency": None,
        "eyeid": "87654321-1234-5678-1234-567812345678"
    }

    # Sende die POST-Anfrage, um den neuen Patienten zu erstellen
    response = client.post(
        url_for('patient_create_bp.create_patient'),
        json=new_patient_data
    )

    # Überprüfen, ob der Statuscode 500 ist (Interner Serverfehler)
    assert response.status_code == 500
    assert response.is_json
    assert response.json['error'].startswith("Database error")
