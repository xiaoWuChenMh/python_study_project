
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class configItem(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        label = QLabel("这是一个新部件")
        layout.addWidget(label)

        button = QPushButton("点击我")
        layout.addWidget(button)

        self.setLayout(layout)