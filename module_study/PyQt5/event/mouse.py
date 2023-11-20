import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit

# 将鼠标事件添加到主窗口类
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Click in this window")
        self.setCentralWidget(self.label)

    # 鼠标移动了
    def mouseMoveEvent(self, e):
        self.label.setText("mouseMoveEvent")
        print("mouseMoveEvent")

    # 鼠标按钮被按下
    def mousePressEvent(self, e):
        self.label.setText("mousePressEvent")
        print("mousePressEvent")

    # 释放鼠标按钮
    def mouseReleaseEvent(self, e):
        self.label.setText("mouseReleaseEvent")
        print("mouseReleaseEvent")

    # 检测到双击
    def mouseDoubleClickEvent(self, e):
        # 双击触发的事件：mousePressEvent、mouseReleaseEvent、mouseDoubleClickEvent、mouseReleaseEvent
        self.label.setText("mouseDoubleClickEvent")
        print("mouseDoubleClickEvent")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()