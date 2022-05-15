from . import create_app, dramatiq

# todo(doubravskytomas): solve loading correct config
app = create_app()
broker = dramatiq.broker
