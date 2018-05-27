# Boggle
Boggle is a word game, in which players attempt to find words in a sequence of adjacent letters.

## Requirement
- Python (>= 3.6)
- Flask (>= 1.0.2)

## How to use
Create isolated Python environments

    virtualenv virtualenv
    source virtualenv/bin/activate

Install the required packages

    pip install -r requirements.txt

Run the web server

    python run.py

Finally, open the browser with http://127.0.0.1:5000/ and play with it!

## Design considerations

### Performance
To allow efficiently looking up the dictionary, I build a Trie structure first to store the dictionary. We can find whether a word exists in the dictionary through traversal from the Trie root. Then, we use depth first search on the board to check if the query word exists on the board.

### Security
To prevent some bad buy from selecting an easier board to cheat on the game, I use sessions to store the board for each player. The flask sessions is implemented by using a signed cookie. Hence, users cannot modify the content unless they know the secret key stored in the server.
