# tests/integration/test_image_update_path.py

import os
import pytest
from flask import url_for
from app.models.image import Image

@pytest.fixture
def image_with_path(db, new_patient):
    """Erstellt ein Bild mit einem gültigen Pfad für den Test."""
    image = Image(
        image_path="uploads/test_image.jpg",
        patient_id=new_patient.id
    )
    db.session.add(image)
    db.session.commit()
    return image

def test_update_image_path_success(client, image_with_path, monkeypatch, app):
    """
    Testet den erfolgreichen Fall, in dem der Bildpfad erfolgreich aktualisiert wird.
    """
     # Simuliere die maximale Dateigröße in der App-Konfiguration
    monkeypatch.setitem(app.config, 'MAX_CONTENT_LENGTH', 16 * 1024 * 1024)  # 16 MB

    # Simuliere die Existenz des alten Pfades und das erfolgreiche Verschieben
    def mock_rename(old_path, new_path):
        pass  # Simuliere erfolgreiches Umbenennen der Datei

    def mock_exists(path):
        return True  # Simuliere, dass der alte Pfad existiert

    monkeypatch.setattr(os, 'rename', mock_rename)
    monkeypatch.setattr(os.path, 'exists', mock_exists)

    # Neue Bildpfad-Daten
    updated_data = {
        "image_path": "uploads/test_image.jpg"
    }

    # Sende die PUT-Anfrage zur Aktualisierung des Bildpfads
    response = client.put(
        url_for('image_update_path_bp.update_image_path', image_id=image_with_path.id),
        json=updated_data
    )

    # Überprüfen, ob der Statuscode 200 ist (Erfolg)
    assert response.status_code == 200
    assert response.is_json
    assert response.json['message'] == "Bildpfad erfolgreich aktualisiert"

    # Überprüfen, ob der Bildpfad in der Datenbank aktualisiert wurde
    updated_image = Image.query.get(image_with_path.id)
    assert updated_image.image_path == "uploads/test_image.jpg"

def test_update_image_path_no_path_provided(client, image_with_path):
    """
    Testet den Fall, dass kein Bildpfad übergeben wird (sollte 400 zurückgeben).
    """
    # Leerer JSON-Body ohne image_path
    response = client.put(
        url_for('image_update_path_bp.update_image_path', image_id=image_with_path.id),
        json={}
    )

    # Überprüfen, ob der Statuscode 400 ist und die Fehlermeldung korrekt ist
    assert response.status_code == 400
    assert response.is_json
    assert response.json['error'] == "Image path is required"


def test_update_image_path_invalid_path(client, image_with_path, monkeypatch):
    """
    Testet den Fall, dass der neue Bildpfad ungültig ist (sollte 400 zurückgeben).
    """

    # Mock für die Validierungsfunktion
    def mock_validate_image_path(image_path, allowed_extensions, max_size):
        return False, "Invalid image path"

    monkeypatch.setattr('app.utils.validators.image.validate_image_path', mock_validate_image_path)

    # Mock für os.path.exists, damit es so aussieht, als ob die Datei nicht existiert
    monkeypatch.setattr('os.path.exists', lambda path: False)

    # Sende eine PUT-Anfrage mit einem ungültigen Pfad
    response = client.put(
        url_for('image_update_path_bp.update_image_path', image_id=image_with_path.id),
        json={"image_path": "invalid_path.jpg"}
    )

    # Überprüfen, ob der Statuscode 400 ist und die Fehlermeldung korrekt ist
    assert response.status_code == 400
    assert response.is_json
    assert response.json['error'] == "File does not exist"


def test_update_image_path_rename_failure(client, image_with_path, monkeypatch, app):
    """
    Testet den Fall, dass beim Verschieben der Datei ein Fehler auftritt (sollte 500 zurückgeben).
    """

    def mock_rename(old_path, new_path):
        raise OSError("Rename failed")  # Simuliere ein Fehler beim Umbenennen

    def mock_exists(path):
        return True  # Simuliere, dass der alte Pfad existiert

    # Setze MAX_CONTENT_LENGTH in der Konfiguration
    monkeypatch.setitem(app.config, 'MAX_CONTENT_LENGTH', 16 * 1024 * 1024)  # 16 MB

    monkeypatch.setattr(os, 'rename', mock_rename)
    monkeypatch.setattr(os.path, 'exists', mock_exists)

    # Sende die PUT-Anfrage zur Aktualisierung des Bildpfads
    response = client.put(
        url_for('image_update_path_bp.update_image_path', image_id=image_with_path.id),
        json={"image_path": "uploads/test_image.jpg"}
    )

    # Überprüfen, ob der Statuscode 500 ist und die Fehlermeldung korrekt ist
    assert response.status_code == 500
    assert response.is_json
    assert response.json['error'] == "Failed to move file: Rename failed"
