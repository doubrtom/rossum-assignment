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


def get_sqlalchemy_uri() -> str:
    """Return URI for SQLAlchemy to connect into DB."""
    dialect = get_required_environ("DB_DIALECT")
    username = get_required_environ("DB_USERNAME")
    password = get_required_environ("DB_PASSWORD")
    host = get_required_environ("DB_HOST")
    port = get_required_environ("DB_PORT")
    db_name = get_required_environ("DB_NAME")
    return f"{dialect}://{username}:{password}@{host}:{port}/{db_name}"


class Config:
    """Base configuration for Flask."""

    SECRET_KEY = get_required_environ("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = get_sqlalchemy_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        """Init new Flask app."""


class DevelopConfig(Config):
    """Develop - configuration for Flask."""

    DEBUG = True
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """Testing - configuration for Flask."""

    TESTING = True


class ProductionConfig(Config):
    """Production - configuration for Flask."""

    DEBUG = False


config_types = {
    "development": DevelopConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopConfig,
}
