# app/services/image_service.py

import os
from PIL import Image as PILImage  # Pillow für Bildverarbeitung

# Funktion zum Erstellen eines Thumbnails
def create_thumbnail(image_path, thumbnail_size=(150, 150)):
    if not os.path.exists(image_path):
        raise FileNotFoundError("Original image not found")

    thumbnail_dir = os.path.join(os.path.dirname(image_path), 'thumbnails')
    if not os.path.exists(thumbnail_dir):
        os.makedirs(thumbnail_dir)

    thumbnail_path = os.path.join(thumbnail_dir, os.path.basename(image_path))

    with PILImage.open(image_path) as img:
        img.thumbnail(thumbnail_size)
        img.save(thumbnail_path)

    return thumbnail_path
