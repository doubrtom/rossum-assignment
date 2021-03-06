import os


class ImproperlyConfiguredError(Exception):
    """Raise when invalid config."""


def get_required_environ(key: str) -> str:
    """Return required ENV variable or raise error if missing."""
    try:
        return os.environ[key]
    except KeyError:
        error_msg = f"Missing env variable: {key}"
        raise ImproperlyConfiguredError(error_msg) from KeyError


def get_sqlalchemy_uri(testing: bool = False) -> str:
    """Return URI for SQLAlchemy to connect into DB."""
    dialect = get_required_environ("DB_DIALECT")
    username = get_required_environ("DB_USERNAME")
    password = get_required_environ("DB_PASSWORD")
    host = get_required_environ("DB_HOST")
    port = get_required_environ("DB_PORT")
    if testing:
        db_name = get_required_environ("DB_NAME_TEST")
    else:
        db_name = get_required_environ("DB_NAME")
    return f"{dialect}://{username}:{password}@{host}:{port}/{db_name}"


class Config:
    """Base configuration for Flask."""

    SECRET_KEY = get_required_environ("SECRET_KEY")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    SQLALCHEMY_DATABASE_URI = get_sqlalchemy_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DRAMATIQ_BROKER = get_required_environ("DRAMATIQ_BROKER")
    DRAMATIQ_BROKER_URL = get_required_environ("DRAMATIQ_BROKER_URL")
    IMAGE_MAX_WIDTH = 1200
    IMAGE_MAX_HEIGHT = 1600

    @staticmethod
    def init_app(app):
        """Init new Flask app."""


class DevelopmentConfig(Config):
    """Develop - configuration for Flask."""

    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """Testing - configuration for Flask."""

    TESTING = True
    DRAMATIQ_BROKER = "dramatiq.brokers.stub:StubBroker"
    DRAMATIQ_BROKER_URL = ""
    SQLALCHEMY_DATABASE_URI = get_sqlalchemy_uri(True)


class ProductionConfig(Config):
    """Production - configuration for Flask."""


config_types = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
