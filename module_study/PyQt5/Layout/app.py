import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget,QVBoxLayout
from PyQt5.QtGui import QPalette, QColor
from module_study.PyQt5.parts.customize.Color import Color

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        layout = QVBoxLayout()

        layout.addWidget(Color('red'))
        layout.addWidget(Color('green'))
        layout.addWidget(Color('blue'))

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()