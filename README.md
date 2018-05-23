README
===========

# Testing Environment
Compiled with g++ 8.1.0 on Linux 4.16

# How to use
    make && make run

# Design
To allow efficiently looking up the dictionary, I build a Trie structure first to store the dictionary. Besides, the count variable inside each Trie node stores the number of words with the same prefix.Then, we use depth first search on the board to find possible words.
