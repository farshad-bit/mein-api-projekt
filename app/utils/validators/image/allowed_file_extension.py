# app/utils/validators/image/allowed_file_extension.py

from flask import current_app

def allowed_file_extension(filename, allowed_extensions):
    """
    Überprüft, ob die Datei eine zulässige Dateiendung hat.
    
    :param filename: Name der Datei
    :param allowed_extensions: Zulässige Dateiendungen (Set)
    :return: True, wenn die Dateiendung gültig ist, sonst False
    """
    try:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
    except Exception as e:
        current_app.logger.error(f"Error validating file extension: {str(e)}")
        return False
