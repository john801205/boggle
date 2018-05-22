#include <array>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

struct TrieNode
{
  bool                   word;
  unsigned               count;
  std::array<TrieNode *, 26> node;

  TrieNode(): word(false), count(0), node()
  {
    for (int i = 0; i < 26; i++)
      node[i] = nullptr;
  }

  ~TrieNode()
  {
    for (int i = 0; i < 26; i++)
      delete node[i];
  }
};

void insertWord(TrieNode *root, const std::string &s)
{
  for (const auto &c: s)
  {
    int index = c - 'a';

    if (root->node[index] == nullptr)
      root->node[index] = new TrieNode();

    root->count++;
    root = root->node[index];
  }

  root->word = true;
  root->count++;
}

int lookup(TrieNode                           *root,
           std::array<std::array<char, 4>, 4> &board,
           int                                 row,
           int                                 col,
           std::string                        &stack)
{
  if (row < 0 || row >= 4
      || col < 0 || col >= 4
      || root == nullptr
      || root->count == 0
      || board[row][col] == 0)
    return 0;

  int count = 0;
  if (root->word)
  {
    std::cout << stack << '\n';
    count++;
    root->word = false;
  }

  char orig = board[row][col];
  board[row][col] = 0;

  std::vector<char> possibles;
  if (orig == '*')
  {
    for (char guess = 'a'; guess <= 'z'; guess++)
      possibles.emplace_back(guess);
  }
  else
  {
    possibles.emplace_back(orig);
  }

  for (const auto &possible: possibles)
  {
    stack.push_back(possible);

    for (int i = -1; i <= 1; i++)
      for (int j = -1; j <= 1; j++)
        count += lookup(root->node[possible-'a'], board, row+i, col+j, stack);

    stack.pop_back();
  }

  board[row][col] = orig;
  root->count -= count;

  return count;
}

int main()
{
  std::ifstream board_stream ("TestBoard.txt");
  std::array<std::array<char, 4>, 4> board;

  for (int i = 0; i < 4; i++)
  {
    for (int j = 0; j < 4; j++)
    {
      char c = board_stream.get();

      while (c == ' ' || c == ',')
        c = board_stream.get();

      board[i][j] = std::tolower(c);
    }
  }

  TrieNode root;
  std::ifstream dict_stream ("dictionary.txt");
  std::string word;

  while (std::getline(dict_stream, word))
    insertWord(&root, word);

  for (int i = 0; i < 4; i++)
  {
    for (int j = 0; j < 4; j++)
    {
      std::string stack;
      lookup(&root, board, i, j, stack);
    }
  }

  return 0;
}
