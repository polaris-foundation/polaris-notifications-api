from pathlib import Path

import connexion
from connexion import FlaskApp
from flask import Flask
from flask_batteries_included import augment_app as fbi_augment_app
from flask_batteries_included.config import is_not_production_environment
from she_logging import logger

from dhos_notifications_api import blueprint_api, blueprint_development
from dhos_notifications_api.config import init_config
from dhos_notifications_api.helper.cli import add_cli_command


def create_app(testing: bool = False) -> Flask:

    openapi_dir: Path = Path(__file__).parent / "openapi"
    connexion_app: FlaskApp = connexion.App(
        __name__,
        specification_dir=openapi_dir,
        options={"swagger_ui": is_not_production_environment()},
    )
    connexion_app.add_api("openapi.yaml", strict_validation=True)

    # Create a Flask app.
    app: Flask = fbi_augment_app(app=connexion_app.app, use_auth0=True, testing=testing)

    # Apply config
    init_config(app)

    app.register_blueprint(blueprint_api.api_blueprint)
    app.logger.info("Registered API blueprint")

    # Register development endpoint if in a lower environment
    if is_not_production_environment():
        app.register_blueprint(blueprint_development.development_blueprint)
        app.logger.info("Registered development blueprint")

    add_cli_command(app)

    # Done!
    logger.info("App initialised")

    return app
