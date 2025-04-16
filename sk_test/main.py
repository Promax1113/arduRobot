import json
import sys
import PyQt5 as qt
import time
import serial

import socket

import signal
import sys


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
    print("Ready!")

    return ser


def serialWrite(ser, data: str | int):
    ser.write(data.encode("utf-8") if type(data) == str else data)


def serialRead(ser):
    data = None
    while not data:
        data = ser.readline().decode("utf-8")
    return data


if __name__ == "__main__":
    ser = setup()
    sock = socket_setup()
    while True:
        data = ser.read_until()
        print(data)
        sock.sendall(json.dumps())
