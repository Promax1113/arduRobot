from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

class SettingsWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Settings")
        self.setup_layout()
        self.resize(400, 200)
    def setup_layout(self):
        layout = QVBoxLayout()
        self.option_label = QLabel("this is settings")
        layout.addWidget(self.option_label)
        self.setLayout(layout)
