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

    def answers(self, board):
        result = set()

        for i in range(len(board)):
            for j in range(len(board[i])):
                stack = ''
                Trie.query(self.root, board, i, j, stack, result)

        return result

    @staticmethod
    def query(root, board, row, col, stack, result):
        if (row < 0 or row >= 4 or
            col < 0 or col >= 4 or
            board[row][col] == None or
            root == None or
            root.count == 0):
            return 0

        count = 0
        if root.word:
            count += 1
            root.word = False
            result.add(stack)

        orig = board[row][col]
        board[row][col] = None

        possibilities = orig if orig != '*' else string.ascii_lowercase

        for possible in possibilities:
            new_stack = stack + possible
            index = ord(possible) - ord('a')

            for i in range(-1, 2):
                for j in range(-1, 2):
                    count += Trie.query(root.node[index], board, row+i, col+j, new_stack, result)

        board[row][col] = orig
        root.count -= count;

        return count;





