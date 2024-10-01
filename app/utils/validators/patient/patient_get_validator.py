from flask import current_app

def validate_patient_id(patient_id):
    """
    Überprüft, ob die gegebene Patient-ID ein gültiger Integer ist.
    
    :param patient_id: ID des Patienten
    :return: Tuple (bool, str): True, wenn die ID gültig ist, sonst False und eine Fehlermeldung
    """
    if not isinstance(patient_id, int) or patient_id <= 0:
        current_app.logger.error(f"Ungültige Patient-ID: {patient_id}")
        return False, "Ungültige Patient-ID. Die ID muss eine positive Ganzzahl sein."
    
    return True, None
