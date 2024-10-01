import pytest
from flask import url_for

def test_get_patient_success(client, new_patient):
    """
    Testet den erfolgreichen Abruf eines Patienten.
    """
    # Sende eine GET-Anfrage für den vorhandenen Patienten
    response = client.get(url_for('patient_get_bp.get_patient', patient_id=new_patient.id))

    # Überprüfe, ob der Statuscode 200 ist (Erfolg)
    assert response.status_code == 200

    # Überprüfe, ob die Antwort JSON ist
    assert response.is_json

    # Überprüfe, ob die Patientendaten in der Antwort korrekt sind
    response_data = response.json
    assert response_data['id'] == new_patient.id
    assert response_data['first_name'] == "John"
    assert response_data['last_name'] == "Doe"
    assert response_data['dob'] == "1990-01-01"
    assert response_data['gender'] == "male"
    assert response_data['eyeid'] == new_patient.eyeid

def test_get_patient_invalid_id(client):
    """
    Testet den Fall, in dem eine ungültige Patient-ID übergeben wird (sollte 404 zurückgeben).
    """
    # Simuliere eine ungültige ID, z.B. eine negative Zahl
    invalid_id = -1
    response = client.get(url_for('patient_get_bp.get_patient', patient_id=invalid_id))

    # Überprüfe, ob der Statuscode 404 ist (Not Found)
    assert response.status_code == 404

    # Falls die Antwort kein JSON ist, überprüfe einfach, ob es HTML sein könnte
    assert 'text/html' in response.content_type

    # Überprüfe den Inhalt der 404-Seite
    assert b'404 Not Found' in response.data


def test_get_patient_not_found(client):
    """
    Testet den Fall, in dem ein Patient nicht existiert (sollte 404 zurückgeben).
    """
    # Simuliere eine nicht existierende Patient-ID
    non_existing_id = 9999
    response = client.get(url_for('patient_get_bp.get_patient', patient_id=non_existing_id))

    # Überprüfe, ob der Statuscode 404 ist (Not Found)
    assert response.status_code == 404

    # Falls die Antwort kein JSON ist, überprüfe einfach, ob es HTML sein könnte
    assert 'text/html' in response.content_type

    # Überprüfe den Inhalt der 404-Seite
    assert b'404 Not Found' in response.data

def test_get_patient_invalid_format(client):
    """
    Testet den Fall, in dem die Patient-ID kein Integer ist (sollte 404 zurückgeben, da die Route nur Integer akzeptiert).
    """
    # Verwende die URL direkt anstelle von url_for, um die Konvertierung zu umgehen
    response = client.get("/patients/abc")

    # Überprüfe, ob der Statuscode 404 ist (Not Found), da die Route nur Integer akzeptiert
    assert response.status_code == 404

    # Optional: Überprüfe den Content-Type der Antwort
    assert 'text/html' in response.content_type


