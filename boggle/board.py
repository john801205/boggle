import flask
import itertools
import random
import string

from . import trie

bp = flask.Blueprint('board', __name__, url_prefix='/boggle')
dictionary = trie.Trie()

with open('dictionary2.txt', 'r') as f:
    for word in f:
        word = word.strip()
        dictionary.insert(word)

@bp.route('/')
def index():
    flask.session['board'] = [[1,2,3],[2,3,4]]
    return flask.redirect(flask.url_for('board.random_board'))

@bp.route('/random')
def random_board():
    rows = 4
    cols = 4
    board = [[random.choice(string.ascii_lowercase+'*') for j in range(cols)] for i in range(rows)]

    flask.session['rows'] = rows
    flask.session['cols'] = cols
    flask.session['board'] = board

    result = {'rows': rows, 'cols': cols, 'board': board}
    return flask.jsonify(result)

@bp.route('/shuffle')
def shuffle():
    rows = flask.session.get('rows', None)
    cols = flask.session.get('cols', None)
    board = flask.session.get('board', None)

    if rows == None or cols == None or board == None:
        flask.abort(401)

    board = itertools.chain_fromiterable(board)
    random.shuffle(board)
    board = [[board[i*cols+j] for j in range(cols)] for i in range(rows)]

    flask.session['board'] = board

    result = {'rows': rows, 'cols': cols, 'board': board}
    return flask.jsonify(result)

@bp.route('/lookup/<string:board>')
def lookup(word):
    pass
