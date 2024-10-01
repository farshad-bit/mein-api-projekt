# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import config
import pymysql
from app.db import db  # Verwende den Import von der neuen Datei
from app.controllers.patient.patient_create import patient_create_bp
from app.controllers.patient.patient_get import patient_get_bp
from app.controllers.patient.patient_update import patient_update_bp
from app.controllers.patient.patient_delete import patient_delete_bp
from app.controllers.patient.patient_index import index_bp

from app.controllers.image.image_add import image_add_bp
from app.controllers.image.image_delete import image_delete_bp
from app.controllers.image.image_get import image_get_bp
from app.controllers.image.image_metadata_update import image_metadata_update_bp
from app.controllers.image.image_update_path import image_update_path_bp
from app.swagger.swagger import configure_swagger


pymysql.install_as_MySQLdb()

# db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__, static_folder='static')  # Setze den static_folder Pfad
# Lade die Konfiguration basierend auf dem übergebenen Parameter
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialisiere Erweiterungen
    db.init_app(app)
    migrate.init_app(app, db)

    
    # Importiere und registriere deine Modelle und Controller/Blueprints
    from app.models.patient import Patient
    from app.models.image import Image


   # Importiere und registriere Blueprints für Patienten

    app.register_blueprint(patient_create_bp)


    app.register_blueprint(patient_delete_bp)


    app.register_blueprint(patient_get_bp)


    app.register_blueprint(patient_update_bp)


    app.register_blueprint(index_bp)

    # Importiere und registriere Blueprints für Bilder

    app.register_blueprint(image_add_bp)

    
    app.register_blueprint(image_delete_bp)


    app.register_blueprint(image_get_bp)


    app.register_blueprint(image_metadata_update_bp)


    app.register_blueprint(image_update_path_bp)

    # Swagger konfigurieren
    configure_swagger(app)

    return app
