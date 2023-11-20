import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget,QVBoxLayout,QHBoxLayout
from PyQt5.QtGui import QPalette, QColor
from module_study.PyQt5.parts.customize.Color import Color

# 布局嵌套
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        #创建一个虚拟对象QWidget，用来保存布局
        widget = QWidget()

        # 初始化3个布局：线性、垂直、垂直
        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()

        layout2.addWidget(Color('red'))
        layout2.addWidget(Color('yellow'))
        layout2.addWidget(Color('purple'))

        layout1.addLayout(layout2)

        layout1.addWidget(Color('green'))

        layout3.addWidget(Color('red'))
        layout3.addWidget(Color('purple'))

        layout1.addLayout(layout3)

        # 将布局保持到虚拟对象QWidget中
        widget.setLayout(layout1)
        # 将该虚拟对象放入主窗口
        self.setCentralWidget(widget)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()