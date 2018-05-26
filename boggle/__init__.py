import flask
import os

from . import board, trie

def create_app():
    app = flask.Flask(__name__)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(board.bp)

    @app.route('/hello/')
    def hello():
        return 'Hello, world!\n'

    return app
