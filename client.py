import selectors
import socket
import sys
import types

sel = selectors.DefaultSelector()

def start_connections(host, port, num_conns):
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
            recv_total=0,
            outb=b"",
            action="join"
        )
        sel.register(sock, events, data=data)

def service_connection(key, mask, user_input):
    #print(f"    Creating sock variable")
    sock = key.fileobj
    #print(f"    Creating data variable")
    data = key.data
    #print(f"    Checking for EVENT_READ")
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            print(f"Received {recv_data!r} from connection {data.connid}")
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print(f"Closing connection {data.connid}")
            sel.unregister(sock)
            sock.close()
    #print(f"    Checking for EVENT_WRITE")
    if mask & selectors.EVENT_WRITE:
        #print(f"        Checking for data.messages")
        if not data.outb and data.messages:
            #print(f"            Checking for data failure")
            data.outb = data.messages.pop(0)
        if data.outb: # THIS IS WHERE YOU WANT YOUR CODE
            #print(f"            Checking for data success")
            print(f"Sending {data.outb!r} to connection {data.connid}")
            data.outb = user_input
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <host> <port> <num_connections>")
    sys.exit(1)

host, port, num_conns = sys.argv[1:4]
start_connections(host, int(port), int(num_conns))

try:
    while True:

        #user_input = input("Enter coordinates: ").encode()
        user_input="DEBUG"

        #print(f"Processing events")
        events = sel.select(timeout=1)
        #print(f"Checking for valid events")
        if events:
            #print(f"FOR loop for events")
            for key, mask in events:
                #print(f"Connecting to server...")
                service_connection(key, mask, user_input)
        if not sel.get_map():
            #print(f"Couldn't find sel.get_map")
            break
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()