import os
import pytest
from app.config import DevelopmentConfig, TestConfig, ProductionConfig

@pytest.fixture(autouse=True)
def clear_env_vars():
    """
    Fixture, um sicherzustellen, dass alle Umgebungsvariablen vor jedem Test aufgeräumt werden.
    Dies sorgt dafür, dass jeder Test mit einem sauberen Zustand startet.
    """
    # os.environ.pop('DATABASE_URL', None)
    os.environ.pop('TEST_DATABASE_URL', None)
    os.environ.pop('SECRET_KEY', None)
    yield
    # os.environ.pop('DATABASE_URL', None)
    os.environ.pop('TEST_DATABASE_URL', None)
    os.environ.pop('SECRET_KEY', None)

def test_development_config():
    """
    Testet die Entwicklungsumgebungskonfiguration (DevelopmentConfig).
    Überprüft, ob die Umgebungsvariablen korrekt geladen werden und ob der Debug-Modus aktiviert ist.
    """
    # Setze Umgebungsvariablen für den Test
    os.environ['DATABASE_URL'] = 'mysql+pymysql://dev_user:new_password@app_4-db-1/db_name'
    os.environ['SECRET_KEY'] = 'supersecretkey'

    # Initialisiere die Konfiguration
    config = DevelopmentConfig()

    # Assertions: Überprüfe, ob die Konfiguration korrekt geladen wurde
    assert config.SQLALCHEMY_DATABASE_URI == 'mysql+pymysql://dev_user:new_password@app_4-db-1/db_name'
    assert config.SECRET_KEY == 'supersecretkey'
    assert config.DEBUG is True
    assert config.SQLALCHEMY_ENGINE_OPTIONS['pool_size'] == 10  # Standardoptionen

def test_test_config():
    """
    Testet die Testumgebungskonfiguration (TestConfig).
    Überprüft, ob die Testdatenbank und Testeinstellungen korrekt geladen werden.
    """
    # Setze Umgebungsvariablen für den Test
    os.environ['TEST_DATABASE_URL'] = 'mysql+pymysql://test_user:new_password@app_4-db-1/test_db'
    os.environ['SECRET_KEY'] = 'supersecretkey'

    # Initialisiere die Konfiguration
    config = TestConfig()

    # Assertions: Überprüfe, ob die Konfiguration korrekt geladen wurde
    assert config.SQLALCHEMY_DATABASE_URI == 'mysql+pymysql://test_user:new_password@app_4-db-1/test_db'
    assert config.SECRET_KEY == 'supersecretkey'
    assert config.TESTING is True
    assert config.SQLALCHEMY_ENGINE_OPTIONS == {}  # Keine Pool-Optionen für Testumgebung

def test_production_config():
    """
    Testet die Produktionsumgebungskonfiguration (ProductionConfig).
    Überprüft, ob die Produktionsdatenbank und Produktionsoptionen korrekt geladen werden.
    """
    # Setze Umgebungsvariablen für den Test
    os.environ['DATABASE_URL'] = 'mysql+pymysql://dev_user:new_password@app_4-db-1/db_name'
    os.environ['SECRET_KEY'] = 'supersecretkey'

    # Initialisiere die Konfiguration
    config = ProductionConfig()

    # Assertions: Überprüfe, ob die Konfiguration korrekt geladen wurde
    assert config.SQLALCHEMY_DATABASE_URI == 'mysql+pymysql://dev_user:new_password@app_4-db-1/db_name'
    assert config.SECRET_KEY == 'supersecretkey'
    assert config.SQLALCHEMY_ENGINE_OPTIONS['pool_size'] == 20  # Produktionsspezifische Pool-Optionen
    assert config.SQLALCHEMY_ENGINE_OPTIONS['max_overflow'] == 50

def test_default_config():
    """
    Testet, ob die Standardkonfiguration (DevelopmentConfig) verwendet wird, wenn keine spezifische Umgebung gesetzt ist.
    """
    # Setze keine Umgebungsvariablen, damit die Standardkonfiguration geladen wird
    config = DevelopmentConfig()

    # Assertions: Überprüfe, ob die Standardwerte korrekt geladen wurden
    assert config.SQLALCHEMY_DATABASE_URI == 'mysql+pymysql://dev_user:new_password@app_4-db-1/db_name'
    assert config.SECRET_KEY == 'supersecretkey'  # Standardwert
    assert config.DEBUG is True
    assert config.SQLALCHEMY_ENGINE_OPTIONS['pool_size'] == 10  # Standardoptionen

