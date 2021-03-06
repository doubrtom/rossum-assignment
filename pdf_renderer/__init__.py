# pylint: disable=import-outside-toplevel,unused-import,cyclic-import
import os
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_dramatiq import Dramatiq
from flasgger import Swagger

from config import config_types
from .openapi import template as openapi_template


# Init extensions
db = SQLAlchemy()
migrate = Migrate()
swagger = Swagger(template=openapi_template)
ma = Marshmallow()
dramatiq = Dramatiq()


def page_not_found(err):
    """Error handler for page not found."""
    response = err.get_response()
    response.data = json.dumps(
        {
            "error_message": err.description,
        }
    )
    response.content_type = "application/json"
    return response


def create_app(config=None):
    """Flask app factory."""
    app = Flask(__name__)
    config_name = config

    if not isinstance(config, str):
        config_name = os.getenv("FLASK_CONFIG", "default")

    selected_config = config_types[config_name]
    app.config.from_object(selected_config)
    selected_config.init_app(app)

    # Set up extensions
    db.init_app(app)
    migrate.init_app(app, db, directory=os.path.join("pdf_renderer", "migrations"))
    swagger.init_app(app)
    ma.init_app(app)
    dramatiq.init_app(app)

    # Load models - needed for migrations
    from . import models  # noqa: F401

    # Create app blueprints
    from . import api

    app.register_blueprint(api.api_bp)

    # Register error handlers
    app.register_error_handler(404, page_not_found)

    return app
