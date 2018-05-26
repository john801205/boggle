import flask
import itertools
import random
import string

from . import trie

bp = flask.Blueprint('board', __name__, url_prefix='/boggle')

dictionary = trie.Trie()
with open('dictionary.txt', 'r') as f:
    for word in f:
        dictionary.insert(word.strip())

@bp.route('/')
def index():
    board = flask.session.get('board', None)

    if board == None:
        rows, cols = 4, 4
        board = [[random.choice(string.ascii_lowercase+'*') for j in range(cols)] for i in range(rows)]
        flask.session['board'] = board

    return '<br>'.join(' '.join(row) for row in board)

@bp.route('/random')
def random_board():
    rows = 4
    cols = 4

    board = [[random.choice(string.ascii_lowercase+'*') for j in range(cols)] for i in range(rows)]
    flask.session['board'] = board

    return flask.jsonify({'board': board})

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

@bp.route('/lookup/<string:word>')
def lookup(word):
    board = flask.session.get('board', None)

    if board == None:
        flask.abort(400)

    result = {'status': dictionary.lookup(board, word)}
    return flask.jsonify(result)
