import os
import io
import pytest
from flask import url_for

# Test für den erfolgreichen Upload eines Bildes
def test_add_image_success(client, new_patient):
    # Dieser Block stellt den Anwendungskontext für die URL-Generierung bereit
    with client.application.test_request_context():
        # Erstelle die URL für das Hinzufügen eines Bildes, basierend auf der Patienten-ID
        # 'image_add_bp.add_image' bezieht sich auf den Endpunkt des Blueprints für das Hinzufügen von Bildern
        url = url_for('image_add_bp.add_image', patient_id=new_patient.id)
    
    # Öffne das Bild aus dem angegebenen Pfad im 'rb'-Modus (read binary)
    with open('tests/assets/test_image.png', 'rb') as img:
        # Erstelle die Datenstruktur für die Anfrage
        # 'image_path' ist der Name des Dateifelds im Formular, und 'img' enthält die Bilddatei
        data = {
            'image_path': (img, 'test_image.png')
        }
        
        # Sende eine POST-Anfrage an den Endpunkt mit der Bilddatei
        # 'multipart/form-data' wird benötigt, um Dateiuploads korrekt zu handhaben
        response = client.post(url, data=data, content_type='multipart/form-data')
        
        # Überprüfe, ob die Antwort einen Statuscode 201 (Created) hat, was auf einen erfolgreichen Upload hinweist
        assert response.status_code == 201

def test_add_image_no_file(client, new_patient):
    """
    Testet den Fehlerfall, wenn keine Bilddatei bereitgestellt wird.
    Dieser Test überprüft, ob der Server eine korrekte Fehlermeldung sendet, wenn der Benutzer 
    versucht, ein Bild hochzuladen, ohne tatsächlich eine Datei bereitzustellen.
    """
    
    # Generiere die URL für den Endpunkt, der Bilder zu einem bestimmten Patienten hinzufügt
    with client.application.test_request_context():
        url = url_for('image_add_bp.add_image', patient_id=new_patient.id)

    # Sende eine POST-Anfrage ohne Bilddaten (leeres 'data'-Diktat)
    response = client.post(
        url,
        content_type='multipart/form-data',
        data={}  # Keine Bilddatei in den Daten
    )

    # Prüfe, ob der HTTP-Statuscode 400 (Bad Request) zurückgegeben wird, was auf einen Fehler hinweist
    assert response.status_code == 400

    # Überprüfe, ob die Fehlermeldung korrekt im JSON-Format vorliegt
    assert response.get_json()['error'] == "No image file provided"


# Test für ungültige Dateiendung (z.B. TXT statt PNG/JPG)
def test_add_image_invalid_extension(client, new_patient):
    """
    Testet das Hochladen einer Datei mit ungültiger Dateiendung.
    Dieser Test überprüft, ob der Server eine Fehlermeldung sendet, wenn der Benutzer 
    eine Datei hochlädt, die nicht in einem unterstützten Bildformat (z.B. PNG, JPG) vorliegt.
    """
    
    # Generiere die URL für den Endpunkt zum Hochladen eines Bildes
    with client.application.test_request_context():
        url = url_for('image_add_bp.add_image', patient_id=new_patient.id)

    # Sende eine POST-Anfrage mit einer Datei, die eine ungültige Dateiendung hat (z.B. .txt)
    data = {
        'image_path': (io.BytesIO(b'image data'), 'test_image.txt')  # Ungültige .txt-Dateiendung
    }
    response = client.post(
        url,
        content_type='multipart/form-data',
        data=data
    )

    # Überprüfe, ob der HTTP-Statuscode 400 (Bad Request) zurückgegeben wird
    assert response.status_code == 400

    # Überprüfe, ob die Fehlermeldung "Invalid file extension" zurückgegeben wird
    assert response.get_json()['error'] == "Invalid file extension"

# Test für ungültiges Bildformat
def test_add_image_invalid_format(client, new_patient, monkeypatch):
    """
    Testet das Hochladen eines Bildes mit ungültigem Bildformat.
    Hier wird die Bildformatvalidierung simuliert, um sicherzustellen, 
    dass der Server bei einem ungültigen Format eine Fehlermeldung zurückgibt.
    """

    # Mock die Validatorfunktion, um ein ungültiges Format zurückzugeben
    # Diese Funktion ersetzt die Originalfunktion `validate_image_format` mit einer,
    # die immer False zurückgibt (was auf ein ungültiges Bildformat hinweist).
    def mock_validate_image_format(image_file):
        return False

    # Verwende `monkeypatch`, um die Originalfunktion durch die Mock-Funktion zu ersetzen.
    monkeypatch.setattr('app.utils.validators.image.validate_image_format', mock_validate_image_format)

    # Erzeuge die URL für den Endpunkt zum Hochladen eines Bildes
    with client.application.test_request_context():
        url = url_for('image_add_bp.add_image', patient_id=new_patient.id)

    # Sende eine POST-Anfrage mit einer gültigen Bilddatei, aber die Bildformat-Validierung wird fehlschlagen
    data = {
        'image_path': (io.BytesIO(b'image data'), 'test_image.png')  # Simuliere ein PNG-Bild
    }

    response = client.post(
        url,
        content_type='multipart/form-data',
        data=data
    )

    # Überprüfe, ob der HTTP-Statuscode 400 (Bad Request) zurückgegeben wird
    assert response.status_code == 400

    # Überprüfe, ob die Fehlermeldung "Invalid image format" zurückgegeben wird
    assert response.get_json()['error'] == "Invalid image format"


# Test für ungültiges Bildformat
def test_add_image_invalid_format(client, new_patient, monkeypatch):
    """
    Testet das Hochladen eines Bildes mit ungültigem Bildformat.
    Hier wird die Bildformat-Validierung so simuliert, dass sie fehlschlägt.
    """

    # Mock die Bildformat-Validatorfunktion, um ein ungültiges Format zurückzugeben.
    # Dies simuliert, dass die Funktion `validate_image_format` immer False zurückgibt,
    # was anzeigt, dass das Bildformat ungültig ist.
    def mock_validate_image_format(image_file):
        return False

    # Verwende `monkeypatch`, um die Originalfunktion `validate_image_format`
    # durch die Mock-Funktion zu ersetzen.
    monkeypatch.setattr('app.utils.validators.image.validate_image_format', mock_validate_image_format)

    # Erzeuge die URL für das Hochladen eines Bildes mit einem ungültigen Format.
    with client.application.test_request_context():
        url = url_for('image_add_bp.add_image', patient_id=new_patient.id)

    # Sende eine POST-Anfrage mit einem simulierten Bild im PNG-Format.
    # Da wir die Bildformatprüfung manipuliert haben, wird sie fehlschlagen.
    data = {
        'image_path': (io.BytesIO(b'image data'), 'test_image.png')  # Simuliere ein PNG-Bild
    }

    # Sende die POST-Anfrage an den Image-Upload-Endpunkt.
    response = client.post(
        url,
        content_type='multipart/form-data',
        data=data
    )

    # Überprüfe, ob der HTTP-Statuscode 400 (Bad Request) zurückgegeben wird,
    # da das Bildformat als ungültig angesehen wird.
    assert response.status_code == 400

    # Überprüfe, ob die Fehlermeldung "Invalid image format" korrekt im JSON zurückgegeben wird.
    assert response.get_json()['error'] == "Invalid image format"



