import cv2
from mjpeg_streamer import MjpegServer, Stream

def setup_camera():

    stop_file = "./stopfile"

    capture = cv2.VideoCapture(0)

    server = MjpegServer("0.0.0.0", 8080)
    stream = Stream(name="onboard-camera", size=(1280, 720), quality=70, fps=30)

    server.add_stream(stream)
    server.start()

    try:
        while True:
            ret, frame = capture.read()
            if not ret:
                break

            stream.set_frame(frame)

    except KeyboardInterrupt:
        print("Stopping stream...")
    finally:
        server.stop()
        capture.release()