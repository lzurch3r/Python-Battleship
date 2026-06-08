import selectors
import socket
import sys
import types
import json

import game

sel = selectors.DefaultSelector()

def start_connections(host, port, num_conns, name):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print(f"Starting connection {connid} to {server_addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            connid=connid,
            outb=json.dumps({"action": "join", "name": f"{name}"}).encode()
        )
        sel.register(sock, events, data=data)

def service_connection(key, mask):
    #print(f"    Creating sock variable")
    sock = key.fileobj
    #print(f"    Creating data variable")
    data = key.data
    #print(f"    Checking for EVENT_READ")
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            print(f"Received {recv_data!r} from connection {data.connid}")
            response = json.loads(recv_data.decode())
            result = response.get("result")
            
            if result == "wait":
                print("Waiting for opponent...")
            elif result == "your_turn":
                game.clearConsole()
                if response.get("action") == "opponent_shot":
                    print(f"{response["opponent_name"]} fired at {response["coord"][0]+response["coord"][1]}!")
                if response.get("board"):
                    game.displayBoard(response["board"])
                print(f"{response["player_name"]}, it's your turn!")
                user_input = game.promptCoordinates()
                data.outb = json.dumps({"action": "fire", "coord": user_input}).encode()

                sel.modify(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)
            elif result in ["hit", "miss", "sunk"]:
                game.clearConsole()
                print(f"Shot result: {result.upper()}!")
                game.displayBoard(response["board"])
                if response.get("ship"):
                    print(f"You sunk their {response['ship']}!")
                print("Waiting for opponent's turn...")
            elif result == "win":
                print("CONGRATULATIONS! You won the game!")
                sel.unregister(sock)
                sock.close()
            elif result == "lose":
                print("GAME OVER. Your fleet has been destroyed.")
                sel.unregister(sock)
                sock.close()
        if not recv_data:
            print(f"Closing connection {data.connid}")
            sel.unregister(sock)
            sock.close()
    #print(f"    Checking for EVENT_WRITE")
    if mask & selectors.EVENT_WRITE:
        #print(f"        Checking for data.messages")   
        if data.outb:
            #print(f"            Checking for data success")
            print(f"Sending {data.outb!r} to connection {data.connid}")
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

            if not data.outb:
                sel.modify(sock, selectors.EVENT_READ, data=data)    

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <host> <port> <num_connections>")
    sys.exit(1)

player_name = input("Enter your name: ")
host, port, num_conns = sys.argv[1:4]
start_connections(host, int(port), int(num_conns), player_name)

try:
    while True:

        #user_input = input("Enter coordinates: ").encode()
        #user_input="DEBUG"

        #print(f"Processing events")
        events = sel.select(timeout=1)
        #print(f"Checking for valid events")
        if events:
            #print(f"FOR loop for events")
            for key, mask in events:
                #print(f"Connecting to server...")
                service_connection(key, mask)
        if not sel.get_map():
            #print(f"Couldn't find sel.get_map")
            break
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()