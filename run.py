# APP_4/run.py
from dotenv import load_dotenv
from app import create_app, db  # Importiere auch 'db' für die Datenbankverbindung
from flask import Flask
from sqlalchemy import text  # Importiere 'text' für SQL-Abfragen
import os 

# Erstelle die Flask-Anwendung mit der gewünschten Konfiguration
app = create_app('development')  # oder 'testing', 'production' je nach Bedarf


# load_dotenv()  # Lädt die Variablen aus der .env-Datei
# Lädt die Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Prüft, ob die Variablen geladen sind
print(os.getenv("DATABASE_URL"))
print(os.getenv("MYSQL_USER"))
print(os.getenv("MYSQL_PASSWORD"))

# @app.route('/db-test')
# def test_db_connection():
#     try:
#         # Verwende 'text()' für die SQL-Abfrage
#         result = db.session.execute(text('SELECT 1'))
#         return f"Verbindung zur Datenbank erfolgreich! Ergebnis: {result.fetchone()}"
#     except Exception as e:
#         return f"Fehler bei der Verbindung zur Datenbank: {e}"

if __name__ == '__main__':
    # Listet alle registrierten Routen auf
    print(app.url_map)
    app.run(debug=True, host="0.0.0.0")
