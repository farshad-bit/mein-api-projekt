import pytest
from flask import url_for
from app.models.patient import Patient
from datetime import datetime


def test_update_patient_success(client, new_patient):
    """
    Testet den erfolgreichen Fall, in dem die Patientendaten erfolgreich aktualisiert werden.
    """
    updated_data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "dob": "1985-06-15",
        "gender": "female",
        "title": "Ms.",
        "physician": "Dr. Jane Smith",
        "ancestry": "African",
        "inconsistency": "None",
        "eyeid": "87654321-1234-5678-1234-567812345678"
    }

    # Sende eine PUT-Anfrage, um die Patientendaten zu aktualisieren
    response = client.put(
        url_for('patient_update_bp.update_patient', id=new_patient.id),
        json=updated_data
    )

    # Überprüfe, ob der Statuscode 200 ist (Erfolg)
    assert response.status_code == 200
    assert response.is_json
    assert response.json['message'] == "Patient erfolgreich aktualisiert"

    # Überprüfen, ob die Daten tatsächlich aktualisiert wurden
    updated_patient = Patient.query.get(new_patient.id)
    assert updated_patient.first_name == "Jane"
    assert updated_patient.last_name == "Doe"
    assert updated_patient.dob == datetime(1985, 6, 15).date()
    assert updated_patient.gender == "female"
    assert updated_patient.title == "Ms."
    assert updated_patient.physician == "Dr. Jane Smith"
    assert updated_patient.ancestry == "African"
    assert updated_patient.inconsistency == "None"
    assert updated_patient.eyeid == "87654321-1234-5678-1234-567812345678"

def test_update_patient_invalid_data(client, new_patient):
    """
    Testet den Fall, in dem die Patientendaten ungültig sind (sollte 400 zurückgeben).
    """
    invalid_data = {
        "first_name": "",  # Leerer Vorname ist ungültig
        "dob": "invalid-date-format"  # Ungültiges Datumsformat
    }

    # Sende eine PUT-Anfrage mit ungültigen Daten
    response = client.put(
        url_for('patient_update_bp.update_patient', id=new_patient.id),
        json=invalid_data
    )

    # Überprüfe, ob der Statuscode 400 ist (Bad Request)
    assert response.status_code == 400
    assert response.is_json
    assert 'error' in response.json

def test_update_patient_not_found(client):
    """
    Testet den Fall, in dem der Patient nicht gefunden wird (sollte 404 zurückgeben).
    """
    updated_data = {
        "first_name": "Test",
        "last_name": "NotFound",
        "dob": "1990-01-01",
        "gender": "male"
    }

    # Sende eine PUT-Anfrage für eine nicht existierende Patient-ID
    response = client.put(url_for('patient_update_bp.update_patient', id=9999), json=updated_data)

    # Überprüfe, ob der Statuscode 404 ist (Not Found)
    assert response.status_code == 404

    # Da die Antwort möglicherweise kein JSON ist, überprüfen wir, ob es HTML ist
    assert 'text/html' in response.content_type

    # Optional: Überprüfe den Inhalt der HTML-Antwort, um sicherzustellen, dass sie einen 404-Fehler anzeigt
    assert b'404 Not Found' in response.data




