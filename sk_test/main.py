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

class Socket(socket.socket):
    def __init__(self) -> None:
         super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        
    def receive(self):
        start_time = time.time()
        data = None
        while not data or time.time() - start_time < 500:
            data = self.recv(1024)
        return data

class MovementSocket(socket.socket):
    def __init__(self, port) -> None:
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        
        self.bind(("127.0.0.1", port))
        self.sender = None
        self.listen()

        print(f"Now awaiting connections on {self.getsockname()}!\n")
        while not self.sender:
            self.sender, _addr = self.accept()
            print(f"Connection incoming from {_addr}.")
            self.sender.sendto(struct.pack("!I", 1), _addr)
            data, addr = self.sender.recvfrom(BUFSIZE)
            while not data:
                data, addr = self.sender.recvfrom(BUFSIZE)
                if struct.unpack("!I", data)[0] == 1:
                    print("Connection test successful!")
                else:
                    print("Wasn't able to verify the connection is working.")


    def receive(self):
        header = None
        start = time.time()
        while not header and (time.time() - start) < 0.2:
            print("time spent", time.time() - start)
            header = self.sender.recv(4)
        
        if not header:
            return None

        data_size = struct.unpack("!I", header)[0]
        data = b"" 
        
        while len(data) < data_size:
            received = self.sender.recv(min(data_size - len(data), 1024))
            while not received:
                received = self.sender.recv(min(data_size - len(data), 1024))
            data += received
        print(data.decode())
        return json.loads(data.decode())

def socket_setup(port: int = 7777):
    sk = socket.socket()
    sk.bind(("127.0.0.1", port))
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



def serial_read(ser: serial.Serial):
    # Reset it so it gets the latest value, and not the ones waiting to be read.   
    json_data = ser.readline()
    return json.loads(json_data.decode())
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
    print("sent header")
    sk.sendall(data)
    print("sent")


def debug_serial_read():
    return {"timestamp": time.time(), "testdata": random.randint(0, 100)}


if __name__ == "__main__":
    camera_server = threading.Thread(target=camera.setup_camera)
    #camera_server.start()
    
    ser = setup()
    sensor_data = socket_setup(port=7777)
    interrupt_socket = socket_setup(port=7778)
    motor_socket = MovementSocket(port=7779)
    start_time = time.time()
    # time.sleep(5)
    while True:
        data = serial_read(ser)
        #data = debug_serial_read()
        print(f"{int(time.time() - start_time)}: {data}")
        try:
            send_data(sensor_data, data)
        except ConnectionResetError:
            print("connection was reset")
            sensor_data = socket_setup()
            interrupt_socket = socket_setup(port=7778)
            motor_socket = MovementSocket(port=7779)
        

        motor_data = motor_socket.receive()
        print(motor_data)
        serial_write(ser, motor_data)

        time.sleep(0.2)
