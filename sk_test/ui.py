import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout


class SimpleWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Simple Window")
        self.resize(1280, 720)

        self.distance = QLabel(self)
        self.distance.setText("Distance: 0")

    def update_distance(self, value):
        self.distance.setText(f"Distance: {value}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleWindow()
    window.show()
    sys.exit(app.exec_())
