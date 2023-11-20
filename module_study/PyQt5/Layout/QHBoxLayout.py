import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget,QHBoxLayout
from PyQt5.QtGui import QPalette, QColor
from module_study.PyQt5.parts.customize.Color import Color

# 线性水平布局
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        #创建一个虚拟对象QWidget，用来保存布局
        widget = QWidget()

        # 创建一个线性水平布局
        layout = QHBoxLayout()
        # 向布局中添加小部件
        layout.addWidget(Color('red'))
        layout.addWidget(Color('green'))
        layout.addWidget(Color('blue'))

        # 将布局保持到虚拟对象QWidget中
        widget.setLayout(layout)
        #将该虚拟对象放入主窗口
        self.setCentralWidget(widget)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()