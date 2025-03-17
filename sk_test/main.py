import serial


def setup():
    try:
        ser = serial.Serial(port="/dev/ttyACM1", baudrate=9600)
    except serial.serialutil.SerialException as e:
        print(e)
        ser = None
        print("Awaiting serial...")

        while ser == None:
            try:
                ser = serial.Serial(port="/dev/ttyACM1", baudrate=9600)
            except:
                pass
    data = None
    while data != 100:
        data = int(ser.readline().decode("utf-8"))
    print("Ready!")

    serialWrite(ser, "component_status")
    print(serialRead(ser))


def serialWrite(ser, data: str | int):
    ser.write(data.encode("utf-8") if type(data) == str else data)


def serialRead(ser):
    data = None
    while not data:
        data = ser.readline().decode("utf-8")
    return data


setup()
