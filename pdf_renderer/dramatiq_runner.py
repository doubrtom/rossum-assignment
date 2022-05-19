import os

from . import create_app, dramatiq

app = create_app(os.environ.get('CONFIG_ENV', 'development'))
broker = dramatiq.broker
