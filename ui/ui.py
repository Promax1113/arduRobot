import sys
import cv2 as cv
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget, QApplication, QMainWindow, QSizePolicy

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
class MainWindow(QMainWindow):
    def __init__(self) -> None:

        super().__init__()
        self.setWindowTitle("Robot Interface")
        self.resize(800, 400)
        self.configure_layout()
        

        self.camera_thread = CameraThread("http://127.0.0.1:8080/onboard-camera")
        self.camera_thread.frame_ready_signal.connect(self.update_image)
        self.camera_thread.start()

    def update_image(self, image):
        pixmap = QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(
            self.image_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)
    
    def configure_layout(self):
        container = QWidget()
        self.setCentralWidget(container)

        layout = QGridLayout()
        container.setLayout(layout)
        self.image_label = QLabel(self)
        self.image_label.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.image_label.setMinimumSize(1, 1)  # Allow shrinking to very small
        layout.addWidget(self.image_label)
        
    def closeEvent(self, a0):
        self.camera_thread.stop()
        a0.accept()

def main():
    # 1. Create the QApplication object
    app = QApplication(sys.argv)
    
    window = MainWindow()

    # 3. Show the window
    window.show()

    # 4. Enter the Qt event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
