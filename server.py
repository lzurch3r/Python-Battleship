import selectors
import socket
import sys
import types
import json
import random

import game

sel = selectors.DefaultSelector()

# Global variables
players = []
current_turn = None
game_over = False

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(
        addr=addr,
        inb=b"",
        outb=b"",
        player_id=None,
        name=None,
        board=None,
        hidden_board=None
        )
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            message = json.loads(recv_data.decode())
            action = message["action"]
            if action == "join":
                handle_join(key, message)
            elif action == "fire":
                handle_fire(key, message)
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

def handle_join(key, message):
    global current_turn

    if len(players) != 2:
        key.data.player_id = len(players) + 1
        key.data.name = message["name"]
        players.append(key)
        
        if len(players) == 1:
            key.data.outb += json.dumps({"result": "wait"}).encode()
        elif len(players) == 2:
            BOARD_PLAYER_1 = game.buildBoard(True, game.SHIPS)
            BOARD_PLAYER_2 = game.buildBoard(True, game.SHIPS)
            hidden_board_player_1 = game.buildBoard(False, game.SHIPS)
            hidden_board_player_2 = game.buildBoard(False, game.SHIPS)

            players[0].data.board = BOARD_PLAYER_1
            players[0].data.hidden_board = hidden_board_player_1
            players[1].data.board = BOARD_PLAYER_2
            players[1].data.hidden_board = hidden_board_player_2
            
            current_turn = random.choice([1, 2])
            
            for player in players:
                if player.data.player_id == current_turn:
                    player.data.outb += json.dumps({"player_name": player.data.name, "result": "your_turn", "board": player.data.hidden_board}).encode()
                else:
                    player.data.outb += json.dumps({"result": "wait"}).encode()

def handle_fire(key, message):
    global current_turn
    player_id = key.data.player_id
    opponent = players[0] if key.data.player_id == 2 else players[1]

    if player_id == current_turn:
        key.data.hidden_board, result, ship = game.fire(opponent.data.board, game.SHIPS, key.data.hidden_board, message["coord"])

        if result == "win":
            key.data.outb += json.dumps({"result": "win"}).encode()
            opponent.data.outb += json.dumps({"result": "lose"}).encode()
        else:
            # flip turn and send your_turn/end_turn as normal
            key.data.outb += json.dumps({"result": result, "ship": ship, "board": key.data.hidden_board}).encode()
            current_turn = 1 if current_turn == 2 else 2 
            opponent.data.outb += json.dumps({
                "player_name": opponent.data.name,
                "opponent_name": key.data.name,
                "action": "opponent_shot",
                "coord": message["coord"],
                "result": "your_turn",
                "board": opponent.data.hidden_board
                }).encode()
    else:
        players[player_id - 1].data.outb += json.dumps({"result": "wait"}).encode()

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
print(f"Waiting for players to connect...")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()