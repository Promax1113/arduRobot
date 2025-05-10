import json
import random
import time
import serial

import socket

import struct
import sys


BUFSIZE = 1024
PORT = "/dev/ttyACM0"


def socket_setup(port: int = 7777):
    sk = socket.socket()
    sk.bind(("0.0.0.0", port))
    sock = None
    sk.listen()

    print(f"Now awaiting connections on {sk.getsockname()}!\n")
    while not sock:
        sock, _addr = sk.accept()
        print(f"Connection incoming from {_addr}.")
        sock.send(struct.pack("!I", 100))
        data = sock.recv(BUFSIZE)
        while not data:
            data = sock.recv(BUFSIZE)
        if struct.unpack("!I", data)[0] == 100:
            print("Connection test successful!")
        else:
            print("Wasn't able to verify the connection is working.")

    return sock


def setup():
    global PORT
    try:
        ser = serial.Serial(port=PORT, baudrate=9600)
    except serial.serialutil.SerialException as e:
        print(e)
        ser = None
        print("Awaiting serial...")

        while ser == None:
            try:
                ser = serial.Serial(port=PORT, baudrate=9600)
            except:
                pass
    data = None
    while data != 100:
        data = int(ser.readline().decode("utf-8"))
    print(f"Ready! Arduino connected via serial on {PORT}.")

    return ser


def serial_write(ser, data: str | int):
    ser.write(data.encode("utf-8") if type(data) == str else data)


def serial_read(ser):
    # Reset it so it gets the latest value, and not the ones waiting to be read.
    ser.reset_input_buffer()
    data = None
    while not data:
        data = ser.readline().decode("utf-8").strip()
    return data


def send_data(sk, data, encode=True):
    data = json.dumps(data)
    if encode:
        data = data.encode()
    header = struct.pack("!I", len(data))
    sk.sendall(header)
    sk.sendall(data)


def debug_serial_read():
    return random.randint(0, 30)


if __name__ == "__main__":
    ser = setup()
    sock = socket_setup()
    start_time = time.time()
    while True:
        data = serial_read(ser)
        # data = debug_serial_read()
        print(f"{int(time.time() - start_time)}: {data}", end="\r")
        try:
            send_data(sock, {"header": "sensor", "distance": data})
        except ConnectionResetError:
            print("connection was reset")
            sock = socket_setup()
        time.sleep(0.1)
