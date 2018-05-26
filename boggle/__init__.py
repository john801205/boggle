import flask
import os

from . import board, trie

def create_app(config=None):
    app = flask.Flask(__name__)

    if config is not None:
        app.config.from_mapping(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(board.bp)

    return app
