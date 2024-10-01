from app.models.image import Image
from flask import current_app

def can_delete_patient(patient_id):
    """
    Überprüft, ob ein Patient gelöscht werden kann, indem geprüft wird, 
    ob es zugehörige Datensätze (z.B. Bilder) gibt.
    
    :param patient_id: Die ID des zu löschenden Patienten
    :return: Tuple (bool, str): True, wenn der Patient gelöscht werden kann, sonst False und eine Fehlermeldung
    """
    # Überprüfen, ob der Patient noch zugehörige Bilder hat
    images = Image.query.filter_by(patient_id=patient_id).all()
    if images:
        current_app.logger.warning(f"Patient {patient_id} kann nicht gelöscht werden, da noch {len(images)} Bilder existieren.")
        return False, f"Patient hat noch {len(images)} zugehörige Bilder und kann nicht gelöscht werden."

    return True, None
