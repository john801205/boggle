#include <cctype>
#include <climits>

#include <array>
#include <fstream>
#include <iostream>
#include <queue>
#include <string>

struct TrieNode
{
  bool                   leaf;
  unsigned               count;
  std::array<TrieNode *, 26> node;

  TrieNode(): leaf(false), count(0), node()
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

struct QueueNode
{
  unsigned count;
  int i, j;

  QueueNode(unsigned count, int i, int j): count(count), i(i), j(j) {}
};

bool operator<(const QueueNode &lhs, const QueueNode &rhs)
{
  return lhs.count < rhs.count;
}

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

  root->leaf = true;
  root->count++;
}

int lookup(TrieNode                           *root,
           std::array<std::array<char, 4>, 4> &board,
           int                                 row,
           int                                 col,
           std::string                        &stack)
{
  if (row < 0 || row >= 4 ||
      col < 0 || col >= 4 ||
      root == nullptr ||
      root->count == 0)
    return 0;

  // std::cerr << row << ' ' << col << ' ' << stack << '\n';

  int count = 0;
  if (root->leaf)
  {
    std::cerr << stack << '\n';
    count++;
  }

  std::priority_queue<QueueNode> pqueue;

  for (int i = -1; i <= 1; i++)
  {
    for (int j = -1; j <= 1; j++)
    {
      int r = row+i, c = col+j;
      if (r < 0 || r >= 4 || c < 0 || c >= 4 || board[r][c] == 0)
        continue;

      if (board[r][c] == '*')
      {
        pqueue.emplace(root->count, r, c);
      }
      else
      {
        int index = board[r][c] - 'a';

        if (root->node[index] == nullptr)
          continue;

        pqueue.emplace(root->node[index]->count, r, c);
      }
    }
  }

  while (!pqueue.empty())
  {
    const auto node = pqueue.top();
    pqueue.pop();

    char orig = board[node.i][node.j];
    board[node.i][node.j] = 0;

    if (orig == '*')
    {
      for (char c = 'a'; c <= 'z'; c++)
      {
        stack.push_back(c);
        count += lookup(root->node[c-'a'], board, node.i, node.j, stack);
        stack.pop_back();
      }
    }
    else
    {
      stack.push_back(orig);
      count += lookup(root->node[orig-'a'], board, node.i, node.j, stack);
      stack.pop_back();
    }

    board[node.i][node.j] = orig;
  }

  root->count -= count;
  // std::cerr << row << ' ' << col << '\t' << count << ' ' << root->count << '\n';

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
      // std::cerr << board[i][j] << ' ';
    }
    // std::cerr << '\n';
  }

  TrieNode root;
  std::ifstream dict_stream ("dictionary.txt");
  std::string word;

  while (std::getline(dict_stream, word))
    insertWord(&root, word);

  std::priority_queue<QueueNode> pqueue;

  for (int i = 0; i < 4; i++)
  {
    for (int j = 0; j < 4; j++)
    {
      if (board[i][j] == '*')
      {
        pqueue.emplace(root.count, i, j);
      }
      else
      {
        int index = board[i][j] - 'a';
        if (root.node[index] == nullptr)
          continue;

        pqueue.emplace(root.node[index]->count, i, j);
      }
    }
  }

  while (!pqueue.empty())
  {
    const auto node = pqueue.top();
    pqueue.pop();

    std::string stack;
    // std::cerr << node.count << '\t' << node.i << ' ' << node.j << '\n';

    char orig = board[node.i][node.j];
    board[node.i][node.j] = 0;

    if (orig == '*')
    {
      for (char c = 'a'; c <= 'z'; c++)
      {
        stack.push_back(c);
        lookup(root.node[c-'a'], board, node.i, node.j, stack);
        stack.pop_back();
      }
    }
    else
    {
      stack.push_back(orig);
      lookup(root.node[orig-'a'], board, node.i, node.j, stack);
      stack.pop_back();
    }

    board[node.i][node.j] = orig;
  }


  return 0;
}
