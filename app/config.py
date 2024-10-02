import os

class Config:
    """
    Allgemeine Basiskonfigurationen für alle Umgebungen.
    Diese Klasse wird von den anderen spezifischen Konfigurationsklassen vererbt.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://dev_user:new_password@app_4-db-1/db_name')
    # Deaktiviert die SQLAlchemy Änderungsverfolgung
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Geheimschlüssel für die Session-Sicherheit (wird von Umgebungsvariablen überschrieben)
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')

    # SQLAlchemy-Engine-Optionen (kann in den Umgebungen überschrieben werden)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,          # Anzahl der permanenten Verbindungen
        'max_overflow': 20,       # Zusätzliche Verbindungen, wenn der Pool voll ist
        'pool_timeout': 30,       # Zeit (in Sekunden), die eine Verbindung maximal wartet
        'pool_recycle': 86400     # Verbindungen nach 30 Minuten Inaktivität recyceln
    }

    @staticmethod
    def init_app(app):
        """
        Zusätzliche Initialisierung für spezielle Umgebungen, falls benötigt.
        Zum Beispiel für Logging, externe Services, etc.
        """
        pass


class DevelopmentConfig(Config):
    """
    Konfiguration für die Entwicklungsumgebung.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://dev_user:new_password@app_4-db-1/db_name')  # Dev-Datenbank
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')  # Korrekt die Umgebungsvariable

class TestConfig(Config):
    """
    Konfiguration für die Testumgebung.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'mysql+pymysql://test_user:new_password@app_4-db-1/test_db')  # Test-Datenbank
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')  # Dynamisch setzen, falls in Umgebungsvariablen vorhanden

    # Testumgebung erfordert in der Regel keine Pool-Optionen für die Datenbankverbindung
    SQLALCHEMY_ENGINE_OPTIONS = {}
    # Setze SERVER_NAME auf localhost, um URL-Generierung zu ermöglichen
    SERVER_NAME = "localhost"


class ProductionConfig(Config):
    """
    Konfiguration für die Produktionsumgebung.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://dev_user:new_password@app_4-db-1/db_name')  # Prod-Datenbank
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')  # Dynamisch setzen, falls in Umgebungsvariablen vorhanden

    # Produktionsspezifische SQLAlchemy-Engine-Optionen
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,          # Größere Poolgröße in der Produktion, um mehr gleichzeitige Verbindungen zu verarbeiten
        'max_overflow': 50,       # Mehr Overflow-Verbindungen in der Produktion
        'pool_timeout': 30,       # Maximale Zeit, bevor eine Verbindung abgelehnt wird
        'pool_recycle': 86400     # Verbindungen nach 30 Minuten inaktivität recyceln
    }


# Dictionary, das die Konfigurationen nach Umgebung zuordnet
config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
