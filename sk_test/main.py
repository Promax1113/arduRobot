import sys
import PyQt5 as qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
import time
import serial
import ui

PORT = "/dev/ttyACM0"


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


def update_distance_label():
    global ser
    window.update_distance(int(serialRead(ser)))


if __name__ == "__main__":
    ser = setup()
    app = QApplication(sys.argv)
    window = ui.SimpleWindow()
    window.show()
    timer = qt.QtCore.QTimer()
    timer.timeout.connect(update_distance_label)
    timer.start(1000)
    sys.exit(app.exec_())
