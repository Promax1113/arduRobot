import json
import socket
import struct
import time

BUFSIZE = 38


def setup(addr: str, port: int):
    sk: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect((addr, port))
    data = sk.recv(BUFSIZE)
    while not data:
        data = sk.recv(BUFSIZE)
    if struct.unpack("!I", data)[0] == 1:
        print("Connection successfully tested.")
    else:
        print("Failed to communicate with the robot.")
    sk.send(struct.pack("!I", 1))

    return sk


def receive(sk, decode=True):
    header = None
    while not header:
        header = sk.recv(4)

    message_size = struct.unpack("!I", header)[0]
    data = b""

    while len(data) < message_size:
        received = sk.recv(min(message_size - len(data), 1024))
        while not received:
            received = sk.recv(min(message_size - len(data), 1024))
        data += received

    if decode:
        decoded: dict = json.loads(data.decode())
        if decoded["header"] == "sensor":
            ## display
            print(decoded, end="\r")
        elif decoded["header"] == "terminate":
            exit()
        else:
            print("This is status data")
    else:
        return data
    return decoded


def read_data(sk):
    pass


if __name__ == "__main__":
    sock: socket.socket = setup("127.0.0.1", 7777)
    while True:
        receive(sock)
        time.sleep(0.1)
