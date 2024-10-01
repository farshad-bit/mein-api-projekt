# Datei: tests/patient/test_patient_delete.py

import pytest
from flask import url_for
from unittest.mock import patch

def test_delete_patient_success(client, new_patient):
    """
    Testet den erfolgreichen Fall, in dem ein Patient erfolgreich gelöscht wird.
    """
    # Sende die DELETE-Anfrage, um den Patienten zu löschen
    response = client.delete(url_for('patient_delete_bp.delete_patient', id=new_patient.id))

    # Überprüfen, ob der Statuscode 200 ist (Erfolg)
    assert response.status_code == 200
    assert response.is_json
    assert response.json['message'] == f"Patient mit ID {new_patient.id} erfolgreich gelöscht"

def test_delete_patient_not_found(client):
    """
    Testet den Fall, in dem ein nicht existierender Patient gelöscht werden soll (404 Not Found).
    """
    # Sende die DELETE-Anfrage für einen Patienten, der nicht existiert
    response = client.delete(url_for('patient_delete_bp.delete_patient', id=9999))  # Nicht vorhandene ID

    # Überprüfen, ob der Statuscode 404 ist (Patient nicht gefunden)
    assert response.status_code == 404

    # Überprüfen, ob die Antwort entweder JSON ist oder HTML enthält
    if response.is_json:
        assert 'error' in response.json
        assert response.json['error'] == "Patient not found"
    else:
        assert b"Not Found" in response.data  # Überprüft den HTML-Inhalt für den 404-Fehler

def test_delete_patient_db_error(client, new_patient, monkeypatch):
    """
    Testet den Fall, in dem ein Datenbankfehler beim Löschen eines Patienten auftritt (500 Internal Server Error).
    """

    # Simuliere einen Datenbankfehler
    def mock_delete(patient):
        raise Exception("Database connection lost")

    # Patch die Methode delete innerhalb der db.session, um den Fehler zu simulieren
    monkeypatch.setattr('sqlalchemy.orm.scoping.scoped_session.delete', mock_delete)

    # Sende die DELETE-Anfrage, um den Patienten zu löschen
    response = client.delete(url_for('patient_delete_bp.delete_patient', id=new_patient.id))

    # Überprüfen, ob der Statuscode 500 ist (Interner Serverfehler)
    assert response.status_code == 500
    assert response.is_json
    assert response.json['error'].startswith("Fehler beim Löschen des Patienten")







