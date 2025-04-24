import json
import socket
import struct
import time

BUFSIZE = 1024

def setup(addr: str, port: int):
    sk: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect((addr, port))
    data = sk.recv(BUFSIZE)
    while not data:
        data = sk.recv(BUFSIZE)
    if struct.unpack("!I", data)[0] == 100:
        print("Connection successfully tested.")
    else:
        print("Failed to communicate with the robot.")
    sk.send(struct.pack("!I", 100))


    return sk

def receive(sk, decode=True):
    data = sk.recv(BUFSIZE)
    if not data:
        data = sk.recv(BUFSIZE)
    
    if decode:
        received: dict = json.loads(data.decode())
        if received["header"] == "sensor":
            ## display
            print(received)
        elif received["header"] == "terminate":
            exit()
        else:
            print("This is status data")
    else:
        return data
    return received
def read_data(sk):
    pass    


if __name__ == "__main__":
    sock: socket.socket = setup("127.0.0.1", 7777)
    while True:
        receive(sock)
        time.sleep(.1)