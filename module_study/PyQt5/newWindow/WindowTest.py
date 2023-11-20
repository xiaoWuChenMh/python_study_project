from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import sys

from random import randint

# 自定义类：用于创建子窗口
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

# 自定义类：用于创建主窗口
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # 用于持有子窗口的实例对象
        self.w = None  # No external window yet.
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)

    # 新建一个窗口，多次使用
    def show_new_window(self, checked):
        # 该判断：用于告知系统不用新建窗口，用老的子窗口即可，去掉就会每次都新建一个窗口
        if self.w is None:
            self.w = AnotherWindow()
        self.w.show()

    # 同一个按钮：第一次按新建窗口，再按一次关闭窗口
    def show_new_close_window(self, checked):

        if self.w is None:
            self.w = AnotherWindow()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()