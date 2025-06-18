import json
import socket
import struct
import time

BUFSIZE = 38


def setup(addr: str, port: int):
    sk: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tries = 0
    while tries < 5:    
        try:
            sk.connect((addr, port))
            break
        except ConnectionRefusedError:
            tries += 1
        
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
    start_time = time.time()
    message_size = struct.unpack("!I", header)[0]
    data = b""
    
    while len(data) < message_size and time.time() - start_time< 1000:
        received = sk.recv(min(message_size - len(data), 1024))
        while not received:
            received = sk.recv(min(message_size - len(data), 1024))
        data += received

    if decode:
        decoded: dict = json.loads(data.decode())
        
    return decoded


def send(sk, motor_data: dict):
    motor.sendall("!I", len(json.dumps(data)))
    time.sleep(0.01)
    motor.sendall(json.dumps(data).encode())
    print("sent!")



if __name__ == "__main__":
    sock: socket.socket = setup("127.0.0.1", 7777)
    print("connected to 7777")
    time.sleep(0.5)
    interrupt = setup("127.0.0.1", 7778)
    print("connected to 7778")
    time.sleep(0.5)
    motor = setup("127.0.0.1", 7779)
    print("connected to 7779")
    while True:
        print(receive(sock))
        print("recv")
        motor.sendall(struct.pack("!I", len(json.dumps({"test": True}).encode())))
        time.sleep(0.1)
        motor.sendall(json.dumps({"test": True}).encode())
        print("sent")
        time.sleep(0.1)
