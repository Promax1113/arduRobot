import json
import random
import time
import serial

import socket

import struct
import threading

import camera

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
        sock.sendto(struct.pack("!I", 1), _addr)
        data, addr = sock.recvfrom(BUFSIZE)
        while not data:
            data, addr = sock.recvfrom(BUFSIZE)
        if struct.unpack("!I", data)[0] == 1:
            print("Connection test successful!")
        else:
            print("Wasn't able to verify the connection is working.")

    return sock


def setup():
    global PORT
    try:
        ser = serial.Serial(port=PORT, baudrate=9600)
    except serial.SerialException as e:
        print(e)
        ser = None
        print("Awaiting serial...")

        while ser == None:
            try:
                ser = serial.Serial(port=PORT, baudrate=9600)
            except:
                pass
    ser.reset_input_buffer()
    data = None
    while data != 1:
        data = ser.readline()
        print(data)
        data = int(data.decode())
    ser.write(bytes([1]))
    print(f"Ready! Arduino connected via serial on {PORT}.")

    return ser


def serial_write(ser: serial.Serial, data: dict[str, int]| str | int):
    if type(data) == str:
        ser.write(data.encode())
    elif type(data) == dict:
        ser.write((json.dumps(data) + "\n").encode())
    elif type(data) == int:
        ser.write(bytes([data]))
    else:
        raise TypeError("Unsupported data type for serial_write")



def serial_read(ser):
    # Reset it so it gets the latest value, and not the ones waiting to be read.
    ser.reset_input_buffer()

    lenght_bytes = ser.read(2)
    lenght = (lenght_bytes[0] << 8) | lenght_bytes[1]
    return json.loads(ser.read(lenght).decode())

    # data = None
    # while not data:
    #     data = ser.readline().decode("utf-8").strip()
    # print(data)
    # return json.loads(data)


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
    camera_server = threading.Thread(target=camera.setup_camera)
    camera_server.start()
    
    ser = setup()
    sock = socket_setup()
    start_time = time.time()
    while True:
        data = serial_read(ser)
        # data = debug_serial_read()
        print(f"{int(time.time() - start_time)}: {data}", end="\r")
        try:
            send_data(sock, data)
        except ConnectionResetError:
            print("connection was reset")
            sock = socket_setup()
        data = {"motor1": random.randint(0, 1), "motor2": random.randint(0, 1)}
        print(data)
        serial_write(ser, data)

        time.sleep(0.3)
