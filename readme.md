# Pyhton Client-Server Battleship

A program written in Python that allows two players to connect to a server on different devices and play a game of Battleship against each other.

## Instructions for Build and Use

Steps to build and/or run the software:

1. Download and install Python version 3.14.5
2. In a Windows PowerShell terminal, navigate to the directory containing downloaded files.
3. Enter "python server.py \<host\> \<port\>", where the "host" is the IP address and "port" can be anything. An example looks like this: "python server.py 127.0.0.1 65432".
4. Open a new PowerShell terminal in the same directory.
5. Enter "python client.py \<host\> \<port\> \<number of connections\>", where the "host" and "port" are identical to that of the server. The number of connections is usually 1, since it signifies that one player will connect using the client.
6. Type a name and hit Enter to finish connecting to the server.
7. Repeat steps 4-7 for the second player to start the game.

Instructions for using the software:

1. When connecting, both players must enter a name and the game will start.
2. Players will take turns firing at each other's game board. The turn player will be prompted to input firing coordinates in a certain format, and the server will tell the both players whether the shot hit or miss. The turn will then change to opposing player.
3. Once all ships have been sunk in a board, the player who played last will be declared the winner!

## Development Environment

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* Visual Studio Code 1.123.0
* Python 3.14.5

## Useful Websites to Learn More

I found these websites useful in developing this software:

* [Website Title](https://docs.python.org/3.13/library/socket.html)
* [Socket Programming in Python (Guide)](https://realpython.com/python-sockets/)
* [Python Constants: Improve Your Code's Maintainability](https://realpython.com/python-constants/#understanding-constants-and-variables)

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] If a player disconnects, the same player or another player can connect to the server.
