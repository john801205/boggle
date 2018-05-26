import itertools
import string

class TrieNode:

    def __init__(self):
        self.word = False
        self.count = 0
        self.node = [None] * 26

class Trie:

    def __init__(self):
        self.root = TrieNode()

    def exist(self, word):
        current = self.root

        for character in word:
            if current == None or current.count == 0:
                return False

            index = ord(character) - ord('a')
            current = current.node[index]

        return current != None and current.word

    def insert(self, word):
        if self.exist(word):
            return

        current = self.root
        for character in word:
            index = ord(character) - ord('a')
            if current.node[index] == None:
                current.node[index] = TrieNode()

            current.count += 1
            current = current.node[index]

        current.count += 1
        current.word = True

    def lookup(self, board, word):
        for i in range(len(board)):
            for j in range(len(board[i])):
                if Trie.__lookup(self.root, board, i, j, word, 0):
                    return True

        return False

    @staticmethod
    def __lookup(root, board, row, col, word, index):
        if index >= len(word):
            return root != None and root.word

        if (root == None or
            row < 0 or row >= len(board) or
            col < 0 or col >= len(board[row]) or
            (board[row][col] != '*' and board[row][col] != word[index])):
            return False

        orig = board[row][col]
        board[row][col] = None

        possibles = orig if orig != '*' else string.ascii_lowercase

        for char in possibles:
            current = root.node[ord(char) - ord('a')]

            for i, j in itertools.product(range(-1, 2), repeat=2):
                if Trie.__lookup(current, board, row+i, col+j, word, index+1):
                    board[row][col] = orig
                    return True

        board[row][col] = orig
        return False


