# tests/image/test_delete_image.py

import pytest
from unittest.mock import patch
from app.models.image import Image
from app.models.patient import Patient

def test_delete_image_success(client, new_image):
    """
    Testet das erfolgreiche Löschen eines Bildes und seines Thumbnails.
    """
    print(f"Testing delete for image ID: {new_image.id}")
    
    with patch('app.controllers.image.image_delete.is_writable', return_value=True):
        with patch('app.controllers.image.image_delete.os.path.exists') as mock_exists:
            # Thumbnail existiert
            mock_exists.side_effect = lambda path: path == 'uploads/test_image.jpg' or path == 'uploads/thumbnails/test_image.jpg'


            
            with patch('app.controllers.image.image_delete.validate_image_format', return_value=True):
                with patch('app.controllers.image.image_delete.os.remove') as mock_remove:
                    response = client.delete(f'/images/{new_image.id}')
                    print(f"Response status code: {response.status_code}")
                    print(f"Response JSON: {response.json}")

                    assert response.status_code == 200
                    assert response.is_json
                    assert response.json['message'] == 'Bild und Thumbnail erfolgreich gelöscht'
                    
                    # Überprüfe, ob os.remove für Bild und Thumbnail aufgerufen wurde
                    assert mock_remove.call_count == 2
                    mock_remove.assert_any_call('uploads/test_image.jpg')
                    mock_remove.assert_any_call('uploads/thumbnails/test_image.jpg')

def test_delete_image_not_found(client):
    """
    Testet das Löschen eines nicht vorhandenen Bildes (sollte 404 zurückgeben).
    """
    # Sende eine DELETE-Anfrage für ein Bild mit einer ID, die nicht existiert (z.B. ID 9999)
    response = client.delete('/images/9999')  # Annahme: ID 9999 existiert nicht
    
    # Ausgabe des Statuscodes und der JSON-Antwort für Debugging
    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json}")
    
    # Überprüfen, ob der Statuscode 404 ist (Bild wurde nicht gefunden)
    assert response.status_code == 404, f"Expected 404, but got {response.status_code}"
    
    # Überprüfen, ob die Antwort JSON-Daten enthält
    assert response.is_json, "Expected JSON response"
    
    # Überprüfen, ob die Antwort einen 'error'-Schlüssel enthält
    assert 'error' in response.json, "Expected 'error' key in response JSON"
    
    # Überprüfen, ob die Fehlermeldung korrekt ist
    assert response.json['error'] == 'Image not found', f"Expected 'Image not found', but got {response.json['error']}"

def test_delete_image_directory_not_writable(client, new_image):
    """
    Testet das Löschen eines Bildes, wenn das Verzeichnis nicht beschreibbar ist (sollte 500 zurückgeben).
    """
    # Patch 'is_writable', damit es False zurückgibt und das Verzeichnis als nicht beschreibbar behandelt wird
    with patch('app.controllers.image.image_delete.is_writable', return_value=False):
        # Sende eine DELETE-Anfrage zum Löschen des Bildes
        response = client.delete(f'/images/{new_image.id}')
        
        # Ausgabe des Statuscodes und der JSON-Antwort für Debugging
        print(f"Response status code: {response.status_code}")
        print(f"Response JSON: {response.json}")
        
        # Überprüfen, ob der Statuscode 500 ist (Interner Serverfehler)
        assert response.status_code == 500, f"Expected 500, but got {response.status_code}"
        
        # Überprüfen, ob die Antwort JSON-Daten enthält
        assert response.is_json, "Expected JSON response"
        
        # Überprüfen, ob die Fehlermeldung korrekt ist
        assert response.json['error'] == 'Directory not writable', f"Expected 'Directory not writable', but got {response.json['error']}"

def test_delete_image_thumbnail_not_exists(client, new_image):
    """
    Testet das Löschen eines Bildes, wenn das Thumbnail nicht existiert. Das Bild sollte trotzdem gelöscht werden.
    """
    with patch('app.controllers.image.image_delete.is_writable', return_value=True):
        with patch('app.controllers.image.image_delete.os.path.exists') as mock_exists:
            # Simuliere, dass das Bild existiert, aber nicht das Thumbnail
            mock_exists.side_effect = lambda path: path == 'uploads/test_image.jpg'
            
            with patch('app.controllers.image.image_delete.validate_image_format', return_value=True):
                with patch('app.controllers.image.image_delete.os.remove') as mock_remove:
                    # Sende eine DELETE-Anfrage, um das Bild zu löschen
                    response = client.delete(f'/images/{new_image.id}')
                    
                    # Ausgabe des Statuscodes und der JSON-Antwort für Debugging
                    print(f"Response status code: {response.status_code}")
                    print(f"Response JSON: {response.json}")

                    # Überprüfen, ob der Statuscode 200 ist (Erfolg)
                    assert response.status_code == 200, f"Expected 200, but got {response.status_code}"
                    
                    # Überprüfen, ob die Antwort JSON-Daten enthält
                    assert response.is_json, "Expected JSON response"
                    
                    # Überprüfen, ob die Erfolgsmeldung korrekt ist
                    assert response.json['message'] == 'Bild und Thumbnail erfolgreich gelöscht', f"Expected success message, but got {response.json['message']}"
                    
                    # Überprüfe, ob os.remove für Bild und Thumbnail aufgerufen wurde
                    # Da das Thumbnail nicht existiert, wird nur das Bild entfernt, der Aufruf von os.remove sollte nur einmal erfolgen
                    assert mock_remove.call_count == 1, f"Expected 1 call to os.remove, but got {mock_remove.call_count}"
                    mock_remove.assert_any_call('uploads/test_image.jpg')

def test_delete_image_invalid_format(client, new_image):
    """
    Testet das Löschen eines Bildes mit ungültigem Format (sollte 400 zurückgeben).
    """
    # Simuliere, dass das Verzeichnis beschreibbar ist
    with patch('app.controllers.image.image_delete.is_writable', return_value=True):
        # Simuliere, dass das Bild existiert
        with patch('app.controllers.image.image_delete.os.path.exists', return_value=True):
            # Simuliere, dass das Bildformat ungültig ist
            with patch('app.controllers.image.image_delete.validate_image_format', return_value=False):
                # Sende eine DELETE-Anfrage, um das Bild zu löschen
                response = client.delete(f'/images/{new_image.id}')
                
                # Ausgabe des Statuscodes und der JSON-Antwort für Debugging
                print(f"Response status code: {response.status_code}")
                print(f"Response JSON: {response.json}")
                
                # Überprüfen, ob der Statuscode 400 ist (Ungültige Anfrage)
                assert response.status_code == 400, f"Expected 400, but got {response.status_code}"
                
                # Überprüfen, ob die Antwort JSON-Daten enthält
                assert response.is_json, "Expected JSON response"
                
                # Überprüfen, ob die Fehlermeldung im JSON enthalten ist
                assert 'error' in response.json, "Expected 'error' key in response JSON"
                
                # Überprüfen, ob die Fehlermeldung korrekt ist
                assert response.json['error'] == 'Invalid file format', f"Expected 'Invalid file format', but got {response.json['error']}"


def test_delete_image_thumbnail_deletion_error(client, new_image):
    """
    Testet das Löschen eines Bildes, wenn das Löschen des Thumbnails fehlschlägt (sollte 500 zurückgeben).
    """
    # Simuliere, dass das Verzeichnis beschreibbar ist
    with patch('app.controllers.image.image_delete.is_writable', return_value=True):
        # Simuliere, dass sowohl das Bild als auch das Thumbnail existieren
        with patch('app.controllers.image.image_delete.os.path.exists') as mock_exists:
            mock_exists.side_effect = lambda path: path == 'uploads/test_image.jpg' or path == 'uploads/thumbnails/test_image.jpg'
            
            # Simuliere, dass das Bildformat gültig ist
            with patch('app.controllers.image.image_delete.validate_image_format', return_value=True):
                
                # Simuliere, dass beim Löschen des Thumbnails ein Fehler auftritt
                with patch('app.controllers.image.image_delete.os.remove', side_effect=Exception('Deletion error')) as mock_remove:
                    # Sende eine DELETE-Anfrage, um das Bild zu löschen
                    response = client.delete(f'/images/{new_image.id}')
                    
                    # Ausgabe des Statuscodes und der JSON-Antwort für Debugging
                    print(f"Response status code: {response.status_code}")
                    print(f"Response JSON: {response.json}")
                    
                    # Überprüfen, ob der Statuscode 500 ist (Interner Serverfehler)
                    assert response.status_code == 500, f"Expected 500, but got {response.status_code}"
                    
                    # Überprüfen, ob die Antwort JSON-Daten enthält
                    assert response.is_json, "Expected JSON response"
                    
                    # Überprüfen, ob die Fehlermeldung im JSON enthalten ist
                    assert 'error' in response.json, "Expected 'error' key in response JSON"
                    
                    # Überprüfen, ob die Fehlermeldung korrekt ist
                    assert response.json['error'] == 'Failed to delete thumbnail: Deletion error', f"Expected 'Failed to delete thumbnail: Deletion error', but got {response.json['error']}"

def test_delete_image_image_deletion_error(client, new_image):
    """
    Testet das Löschen eines Bildes, wenn das Löschen des Bildes fehlschlägt (sollte 500 zurückgeben).
    """
    with patch('app.controllers.image.image_delete.is_writable', return_value=True):
        with patch('app.controllers.image.image_delete.os.path.exists') as mock_exists:
            # Thumbnail existiert
            mock_exists.side_effect = lambda path: path == 'uploads/test_image.jpg' or path == 'uploads/thumbnails/test_image.jpg'
            with patch('app.controllers.image.image_delete.validate_image_format', return_value=True):
                # Mock os.remove: Erstes Mal für Thumbnail, erfolgreich; zweites Mal für Bild, fehlschlagend
                with patch('app.controllers.image.image_delete.os.remove') as mock_remove:
                    mock_remove.side_effect = [None, Exception('Deletion error')]
                    response = client.delete(f'/images/{new_image.id}')
                    print(f"Response status code: {response.status_code}")
                    print(f"Response JSON: {response.json}")
                    assert response.status_code == 500
                    assert response.is_json
                    assert 'error' in response.json
                    assert response.json['error'] == 'Failed to delete file: Deletion error'

def test_delete_image_database_deletion_error(client, new_image):
    """
    Testet das Löschen eines Bildes, wenn das Löschen des Datenbankeintrags fehlschlägt (sollte 500 zurückgeben).
    """
    with patch('app.controllers.image.image_delete.is_writable', return_value=True):
        with patch('app.controllers.image.image_delete.os.path.exists') as mock_exists:
            # Thumbnail existiert
            mock_exists.side_effect = lambda path: path == 'uploads/test_image.jpg' or path == 'uploads/thumbnails/test_image.jpg'
            with patch('app.controllers.image.image_delete.validate_image_format', return_value=True):
                with patch('app.controllers.image.image_delete.os.remove', return_value=None):
                    with patch('app.controllers.image.image_delete.db.session.delete', side_effect=Exception('Database deletion error')) as mock_delete:
                        response = client.delete(f'/images/{new_image.id}')
                        print(f"Response status code: {response.status_code}")
                        print(f"Response JSON: {response.json}")
                        assert response.status_code == 500
                        assert response.is_json
                        assert 'error' in response.json
                        assert response.json['error'] == 'Failed to delete database entry: Database deletion error'