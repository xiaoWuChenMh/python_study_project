from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import sys

from random import randint

# 持久化窗口
class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0,100))
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 初始化子窗口
        self.w = AnotherWindow()
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.toggle_window)
        self.setCentralWidget(self.button)

    def toggle_window(self, checked):
        # 检查当前子窗口的显示状态，是否是可见的
        if self.w.isVisible():
            # 隐藏窗口
            self.w.hide()

        else:
            # 显式窗口
            self.w.show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()