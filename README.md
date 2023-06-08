# redi-python-intermediate

Welcome to my Python Intermediate final project. This is a text-based version of the popular card game, Cards Against Humanity.

Cards Against Humanity allows the open use of their cards, as long as you don't make money off of it. For more information, visit their website at https://www.cardsagainsthumanity.com/#downloads

In this project, I used the following:
- Object-oriented Programming
- Requests, Modules
- Error Handling


## installation

The version of Python this project was mainly programmed on was `3.9.9`. This version has however also been tested on `3.11.4`.

To run the game, the `requests` package needs to be installed. The specific version for `requests` is listed in the requirements.txt file in the top level directory of this project. To install `requests`, in the directory in which you've placed the project files, use the package manager [pip](https://pip.pypa.io/en/stable/).

```bash
pip install -r requirements.txt
```


## usage

To play this game, run the following in your terminal / command line from the directory in which you've placed the project files:

```bash
python3 game.py
```

Please note, running from an IDE like PyCharm will not show the screen clearing functionality in the code. Also, although there is code for screen clearing for macOS/linux, it is untested and unconfirmed to work.


## how to play

At the beginning of the game, there is an option to play with only the Family Edition (kid-friendly version). You must have at least 4 players to play. At each player's turn, their hand is not revealed until the player presses the Enter key; this is the opportunity for others to step away from the screen to give the player their privacy when they choose which card to submit.

Have fun!
