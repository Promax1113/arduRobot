import socket

sk = socket.socket()

sk.connect(("192.168.1.50", 7777))
data = sk.recv(2048)
print(data)
sk.sendall("Hi".encode())
