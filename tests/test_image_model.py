# Datei: tests/test_image_model.py

import pytest
from app.models.image import Image
from app.db import db
from datetime import datetime

def test_image_creation(new_image):
    """Testet die Erstellung eines Bildes."""
    saved_image = Image.query.get(new_image.id)
    assert saved_image is not None
    assert saved_image.image_path == 'uploads/test_image.jpg'
    assert saved_image.description == 'A sample image'
    assert saved_image.tags == 'sample, test'
    assert isinstance(saved_image.date_taken, datetime)


def test_image_serialization(new_image):
    """Testet die Serialisierung eines Bildobjekts."""
    serialized_data = new_image.serialize()
    assert isinstance(serialized_data, dict)
    assert serialized_data['image_path'] == 'uploads/test_image.jpg'
    assert 'date_taken' in serialized_data
    assert serialized_data['description'] == 'A sample image'
    assert serialized_data['tags'] == 'sample, test'
    assert serialized_data['patient_id'] == new_image.patient_id
    assert 'id' in serialized_data
