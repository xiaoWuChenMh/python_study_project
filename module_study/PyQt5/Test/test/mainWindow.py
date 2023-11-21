from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

class CustomWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        label = QLabel("Hello, Custom Widget!")
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

app = QApplication([])
widget1 = CustomWidget()
widget2 = CustomWidget()

widget1.show()
widget2.show()
app.exec_()