# tests/integration/test_image_metadata_update.py

import pytest
from flask import url_for
from app.models.image import Image

@pytest.fixture
def image_with_metadata(db, new_patient):
    """Erstellt ein Bild mit Metadaten, das für den Test verwendet wird."""
    image = Image(
        image_path="uploads/test_image.jpg",
        patient_id=new_patient.id,
        date_taken="2023-01-01 10:00:00",
        description="Test description",
        tags="tag1, tag2"
    )
    db.session.add(image)
    db.session.commit()
    return image


def test_update_image_metadata_success(client, image_with_metadata):
    """
    Testet den erfolgreichen Fall, in dem Bild-Metadaten erfolgreich aktualisiert werden.
    """
    # Neue Metadaten zum Aktualisieren
    updated_data = {
        "date_taken": "2024-01-01 12:00:00",
        "description": "Updated description",
        "tags": "new_tag1, new_tag2"
    }

    # Sende die PUT-Anfrage zur Aktualisierung der Metadaten
    response = client.put(
        url_for('image_metadata_update_bp.update_image_metadata', image_id=image_with_metadata.id),
        json=updated_data
    )

    # Überprüfen, ob der Statuscode 200 ist (Erfolg)
    assert response.status_code == 200
    assert response.is_json
    assert response.json['message'] == "Bildmetadaten erfolgreich aktualisiert"

    # Überprüfen, ob die Metadaten tatsächlich aktualisiert wurden
    updated_image = Image.query.get(image_with_metadata.id)
    assert updated_image.date_taken.strftime('%Y-%m-%d %H:%M:%S') == "2024-01-01 12:00:00"
    assert updated_image.description == "Updated description"
    assert updated_image.tags == "new_tag1, new_tag2"

def test_update_image_metadata_invalid_date_format(client, image_with_metadata):
    """
    Testet, ob das System korrekt auf ungültiges Datumsformat reagiert.
    """
    # Ungültiges Datumsformat
    invalid_data = {
        "date_taken": "01-01-2024"
    }

    response = client.put(
        url_for('image_metadata_update_bp.update_image_metadata', image_id=image_with_metadata.id),
        json=invalid_data
    )

    # Überprüfen, ob der Statuscode 400 ist und die Fehlermeldung korrekt ist
    assert response.status_code == 400
    assert response.is_json
    assert response.json['error'] == "Ungültiges Datumsformat. Erwartet wird YYYY-MM-DD HH:MM:SS."

def test_update_image_metadata_description_too_long(client, image_with_metadata):
    """
    Testet, ob eine zu lange Beschreibung korrekt abgewiesen wird.
    """
    # Beschreibung länger als 255 Zeichen
    long_description = "x" * 256
    invalid_data = {
        "description": long_description
    }

    response = client.put(
        url_for('image_metadata_update_bp.update_image_metadata', image_id=image_with_metadata.id),
        json=invalid_data
    )

    # Überprüfen, ob der Statuscode 400 ist und die Fehlermeldung korrekt ist
    assert response.status_code == 400
    assert response.is_json
    assert response.json['error'] == "Beschreibung darf maximal 255 Zeichen lang sein."

def test_update_image_metadata_tags_too_long(client, image_with_metadata):
    """
    Testet, ob zu lange Tags korrekt abgewiesen werden.
    """
    # Tags länger als 255 Zeichen
    long_tags = "x" * 256
    invalid_data = {
        "tags": long_tags
    }

    response = client.put(
        url_for('image_metadata_update_bp.update_image_metadata', image_id=image_with_metadata.id),
        json=invalid_data
    )

    # Überprüfen, ob der Statuscode 400 ist und die Fehlermeldung korrekt ist
    assert response.status_code == 400
    assert response.is_json
    assert response.json['error'] == "Tags dürfen maximal 255 Zeichen lang sein."

def test_update_image_metadata_empty_data(client, image_with_metadata):
    """
    Testet den Fall, wenn keine Daten übergeben werden (leeres JSON).
    """
    # Sende eine PUT-Anfrage mit leerem JSON-Body
    response = client.put(
        url_for('image_metadata_update_bp.update_image_metadata', image_id=image_with_metadata.id),
        json={}
    )

    # Überprüfen, ob der Statuscode 400 ist und die Fehlermeldung korrekt ist
    assert response.status_code == 400
    assert response.is_json
    assert response.json['error'] == "Leere Daten. Es müssen Metadaten zur Aktualisierung übergeben werden."

def test_update_image_metadata_db_error(client, image_with_metadata, monkeypatch, db):
    """
    Testet den Fall, dass ein Datenbankfehler auftritt (sollte 500 zurückgeben).
    """
    # Simuliere einen Datenbankfehler
    def mock_commit():
        raise Exception("Database error")

    # Verwende das monkeypatching, um den commit in db.session zu simulieren
    monkeypatch.setattr(db.session, 'commit', mock_commit)

    updated_data = {
        "date_taken": "2024-01-01 12:00:00"
    }

    # Sende die PUT-Anfrage zur Aktualisierung der Metadaten
    response = client.put(
        url_for('image_metadata_update_bp.update_image_metadata', image_id=image_with_metadata.id),
        json=updated_data
    )

    # Überprüfen, ob der Statuscode 500 ist und die Fehlermeldung korrekt ist
    assert response.status_code == 500
    assert response.is_json
    assert response.json['error'] == "Fehler beim Speichern der Metadaten"
