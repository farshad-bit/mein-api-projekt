from flask_swagger_ui import get_swaggerui_blueprint

def configure_swagger(app):
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.yaml'  # Der Pfad zur Swagger-Dokumentation
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL, 
        API_URL, 
        config={'app_name': "Meine Flask-API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
