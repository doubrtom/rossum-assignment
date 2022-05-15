import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flasgger import Swagger

from config import config_types

db = SQLAlchemy()
migrate = Migrate()
swagger = Swagger()
ma = Marshmallow()


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
    migrate.init_app(app, db)
    swagger.init_app(app)
    ma.init_app(app)

    # Create app blueprints
    @app.route("/")
    def index():
        return "Index"

    return app
