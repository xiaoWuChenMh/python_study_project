
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget,QGridLayout
from PyQt5.QtGui import QPalette, QColor
from module_study.PyQt5.parts.customize.Color import Color

# 排列在网格中的小部件
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        layout = QGridLayout()

        # 坐标参数信息：y，x
        # 有多个格是根据你定义的坐标边界来算的，下面的边界是[2,1],因为从0开始所以是[3,2]
        layout.addWidget(Color('red'), 0, 0)
        layout.addWidget(Color('green'), 1, 0)
        layout.addWidget(Color('blue'), 1, 1)
        layout.addWidget(Color('purple'), 2, 1)

        # 创建一个虚拟对象QWidget，用来保存布局
        widget = QWidget()
        # 将布局保持到虚拟对象QWidget中
        widget.setLayout(layout)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()