# tests/integration/test_image_get.py

import pytest
from flask import url_for
from app.models.image import Image

@pytest.fixture
def new_patient_with_images(db, new_patient):
    """Fügt dem bestehenden Patienten einige Beispielbilder hinzu."""
    images = [
        Image(image_path="uploads/image1.jpg", patient_id=new_patient.id),
        Image(image_path="uploads/image2.jpg", patient_id=new_patient.id),
        Image(image_path="uploads/image3.jpg", patient_id=new_patient.id)
    ]
    db.session.bulk_save_objects(images)
    db.session.commit()
    
    return new_patient

def test_get_images_success(client, new_patient_with_images):
    """
    Testet den erfolgreichen Abruf der Bilder eines Patienten mit Pagination.
    """
    # Rufe die Bilder für den neuen Patienten ab (Seite 1, 2 Einträge pro Seite)
    response = client.get(url_for('image_get_bp.get_images', patient_id=new_patient_with_images.id, page=1, per_page=2))

    # Überprüfen, ob der Statuscode 200 ist (Erfolg)
    assert response.status_code == 200
    assert response.is_json

    # Überprüfen, ob die Antwort die richtigen Felder enthält
    data = response.json
    assert "page" in data
    assert "per_page" in data
    assert "total_pages" in data
    assert "total_images" in data
    assert "images" in data
    assert len(data['images']) == 2  # Es sollten 2 Bilder auf Seite 1 zurückgegeben werden


def test_get_images_pagination_invalid(client, new_patient_with_images):
    """
    Testet, ob eine ungültige Paginierungsanfrage (negative Seite oder per_page) einen 400-Fehler zurückgibt.
    """
    # Ungültige Pagination-Anfrage
    response = client.get(url_for('image_get_bp.get_images', patient_id=new_patient_with_images.id, page=-1, per_page=-10))

    # Überprüfen, ob der Statuscode 400 ist (Ungültige Anfrage)
    assert response.status_code == 400
    assert response.is_json
    assert "error" in response.json

def test_get_images_no_images_found(client, new_patient):
    """
    Testet den Fall, dass keine Bilder für einen Patienten vorhanden sind (sollte 404 zurückgeben).
    """
    # Rufe die Bilder für den neuen Patienten ab (keine Bilder vorhanden)
    response = client.get(url_for('image_get_bp.get_images', patient_id=new_patient.id))

    # Überprüfen, ob der Statuscode 404 ist (keine Bilder gefunden)
    assert response.status_code == 404
    assert response.is_json
    assert "message" in response.json
    assert response.json['message'] == f"Keine Bilder für den Patienten mit der ID {new_patient.id} gefunden"

def test_get_images_patient_not_found(client):
    """
    Testet den Fall, dass der Patient nicht existiert (sollte 404 zurückgeben).
    """
    # Rufe Bilder für einen nicht existierenden Patienten ab
    response = client.get(url_for('image_get_bp.get_images', patient_id=9999))

    # Überprüfen, ob die Antwort entweder JSON ist oder eine HTML-Fehlerseite enthält
    if response.is_json:
        assert "error" in response.json
    else:
        assert b"Not Found" in response.data  # Überprüfe, ob "Not Found" im HTML steht