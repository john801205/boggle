import flask
import random

from . import trie

bp = flask.Blueprint('board', __name__, url_prefix='/boggle')

@bp.route('/')
def index():
    return flask.redirect(flask.url_for('board.random_board'))

@bp.route('/random')
def random_board():
    board = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz*') for i in range(16))
    return flask.redirect(flask.url_for('board.show_board', board=board))

@bp.route('/board/<string:board>')
def show_board(board):
    if not is_valid_board(board):
        return flask.redirect(flask.url_for('board.random_board'))

    return board

@bp.route('/board/<string:board>/lookup')
def lookup(board):

    dictionary = trie.Trie()

    with open('dictionary.txt', 'r') as f:
        for word in f:
            word = word.strip()
            dictionary.insert(word)

    result = dictionary.answers([['*', '*', '*', '*'],
                                 ['*', '*', '*', '*'],
                                 ['*', '*', '*', '*'],
                                 ['*', '*', '*', '*']])

    return '\n'.join(sorted(list(result)))

@bp.route('/board/<string:board>/lookup/<string:word>')
def lookup_word(board, word):
    pass

def is_valid_board(board):
    return isinstance(board, str) and len(board) == 16
