import flask
import itertools
import os
import random
import string

from . import trie

bp = flask.Blueprint('board', __name__, url_prefix='/boggle')

dictionary = trie.Trie()
dictpath = os.path.join(os.path.dirname(__file__), 'dictionary.txt')
with open(dictpath, 'r') as f:
    for word in f:
        dictionary.insert(word.strip())

@bp.route('/')
def index():
    board = flask.session.get('board', None)

    if board == None:
        rows, cols = 4, 4
        board = [[random.choice(string.ascii_lowercase+'*') for j in range(cols)] for i in range(rows)]
        flask.session['board'] = board

    return flask.render_template('index.html', board=board)

@bp.route('/new')
def new():
    rows = 4
    cols = 4

    board = [[random.choice(string.ascii_lowercase+'*') for j in range(cols)] for i in range(rows)]
    flask.session['board'] = board

    return flask.redirect(flask.url_for('board.index'))

@bp.route('/shuffle')
def shuffle():
    board = flask.session.get('board', None)

    if board == None:
        flask.abort(400)

    rows = len(board)
    cols = len(board[0])

    board = list(itertools.chain.from_iterable(board))
    random.shuffle(board)
    board = [[board[i*cols+j] for j in range(cols)] for i in range(rows)]

    flask.session['board'] = board

    return flask.jsonify({'board': board})

@bp.route('/lookup')
def lookup():
    board = flask.session.get('board', None)
    word = flask.request.args.get('word', None)

    if board == None or word == None:
        flask.abort(400)

    result = {'status': dictionary.lookup(board, word)}
    return flask.jsonify(result)
