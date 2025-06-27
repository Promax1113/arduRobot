import sys
import os
import time
import pygame
import cv2 as cv
from PyQt5.QtCore import QThread, QTimer, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QGridLayout, QMessageBox, QTableWidget, QTableWidgetItem, QWidget, QApplication, QMainWindow, QSizePolicy, QPushButton
from controller import setup, receive, send, SettingsWindow
import json

class Thread(QThread):
    def __init__(self) -> None:
        super().__init__()
        self._run_flag = True

    def stop(self):
        self._run_flag = False
        self.wait()

class CameraThread(Thread):
    frame_ready_signal = pyqtSignal(QImage)

    def __init__(self, url) -> None:
        super().__init__()
        self.source = url

    def run(self) -> None:
        self.capture = cv.VideoCapture(self.source)
        while self._run_flag:
            ret, frame = self.capture.read()
            if not ret:
                frame = cv.imread("./ui/nocamera.png")
                rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                height, width, channel_count = rgb_frame.shape
                self.frame_ready_signal.emit(QImage(rgb_frame.data, width, height, width * channel_count, QImage.Format_RGB888))
                self.msleep(10)
            else:
                rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                height, width, channel_count = rgb_frame.shape

                bytes_per_line = width * channel_count

                qt_compatible_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                self.frame_ready_signal.emit(qt_compatible_image)

    def stop(self) -> None:
        super().stop()
        self.capture.release()

class GamepadInputThread(Thread):
    input_ready_signal = pyqtSignal(dict)

    def __init__(self) -> None:
        super().__init__()
        self.round_digits = 1
        self.input: dict[str, float] = {"rotation": 0, "movement": 0, "camera_pitch": 0, "camera_yaw": 0}
        self.clock = pygame.time.Clock()
        pygame.init()
        pygame.joystick.init()
        time.sleep(0.1)
        self.joystick = pygame.joystick.Joystick(0)

    def run(self):
        while self._run_flag:
           pygame.event.pump()
           self.input["rotation"] = round(self.joystick.get_axis(0), self.round_digits)
           self.input["movement"] = round(self.joystick.get_axis(1), self.round_digits)
           self.input["camera_pitch"] = round(self.joystick.get_axis(3), self.round_digits)
           self.input["camera_yaw"] = round(self.joystick.get_axis(4), self.round_digits)
           self.clock.tick(60)
           self.input_ready_signal.emit(self.input)

class MainWindow(QMainWindow):
    def __init__(self) -> None:


        super().__init__()
        self.settingsWindow = None
        self.setWindowTitle("Robot Interface")
        self.resize(800, 400)
        self.configure_layout()
        self.camera_thread = CameraThread("http://192.168.1.42:8080/onboard-camera")
        self.camera_thread.frame_ready_signal.connect(self.update_image)
        #self.camera_thread.start()

        self.data_socket = setup("127.0.0.1", 7777)
        time.sleep(0.3)
        self.interrupt_socket = setup("127.0.0.1", 7778)
        time.sleep(0.3)
        self.motor_socket = setup("127.0.0.1", 7779)
        
        print("socket made")
        self.input_data_thread = GamepadInputThread()
        self.input_data_thread.input_ready_signal.connect(self.update_inputs)
        self.input_data_thread.start()
        
        self.input = {}
    
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_and_send)
        self.timer.start(200)
        print("set timer")

    def update_inputs(self, inputs):
        self.input = inputs

    def update_and_send(self):
        data: dict = receive(self.data_socket, decode=True)
        send(self.motor_socket, self.input)
        self.update_sensor_data(data)

    def update_image(self, image):
        pixmap = QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(
            self.image_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)

    def dialog_box(self, title, description, icon):
        box = QMessageBox()
        box.setIcon(QMessageBox.Critical)         # Options: Information, Warning, Critical, Question

        box.setWindowTitle(title)
        box.setText(description)
        box.setDefaultButton(QMessageBox.StandardButton.Close)

        result = box.exec_()
        print(result)
        if result == QMessageBox:
            exit(-1)
    

    def update_sensor_data(self, data: dict):
        self.data_table.setColumnCount(2)
        self.data_table.setRowCount(len(data.keys()))
        i = 0
        for key, value in data.items():

            self.data_table.setItem(i, 0, QTableWidgetItem(key))
            self.data_table.setItem(i, 1, QTableWidgetItem(str(value)))
            i += 1
    def configure_layout(self):
        container = QWidget()
        self.setCentralWidget(container)

        self.windowLayout = QGridLayout()
        container.setLayout(self.windowLayout)
        self.shutdown_button = QPushButton()
        self.shutdown_button.setText("Shutdown")
        button = QPushButton()
        button.setText("Settings")
        button.clicked.connect(self.open_settings)
        self.windowLayout.addWidget(button, 0, 1)
        self.image_label = QLabel(self)
        self.image_label.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.data_table = QTableWidget()
        self.windowLayout.addWidget(self.shutdown_button, 0,0)
        self.windowLayout.addWidget(self.data_table, 1, 6)
        self.image_label.setMinimumSize(1, 1)  # Allow shrinking to very small
        self.windowLayout.addWidget(self.image_label, 1, 0, 5, 1)
    def open_settings(self):
        if self.settingsWindow is None:
            self.settingsWindow = SettingsWindow()  # Ensure top-level
        self.settingsWindow.show()
        self.settingsWindow.raise_()
        self.settingsWindow.activateWindow()

    def closeEvent(self, a0):
        self.camera_thread.stop()
        a0.accept()

def main():
    # 1. Create the QApplication object
    
    os.environ['SDL_JOYSTICK_DEVICE'] = '/dev/input/js0'


    app = QApplication(sys.argv)

    window = MainWindow()

    # 3. Show the window
    window.show()

    # 4. Enter the Qt event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
