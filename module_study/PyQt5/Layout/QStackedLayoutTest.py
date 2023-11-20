import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

from module_study.PyQt5.parts.customize.Color import Color


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        # ------------ 1、初始化需要的布局容器 ----------------
        # 线性垂直,最外层的布局容器，用于存储下面的两个布局容器
        pagelayout = QVBoxLayout()
        # 线性水平
        button_layout = QHBoxLayout()
        # 部件堆叠
        self.stacklayout = QStackedLayout()

        # ------------- 2、完成基础布局（未嵌入部件）-----------
        # 布局嵌套，完成基础布局，相当于建房子时的没装修时的粗胚
        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)

        # 设置红色选框的选项卡和显示内容
        btn = QPushButton("red")
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("red"))

        # 设置绿色选框的选项卡和显示内容
        btn = QPushButton("green")
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("green"))

        # 设置黄色选框的选项卡和显示内容
        btn = QPushButton("yellow")
        btn.pressed.connect(self.activate_tab_3)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("yellow"))

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

    def activate_tab_1(self):
        # 通过setCurrentIndex变更要显示的部件
        self.stacklayout.setCurrentIndex(0)

    def activate_tab_2(self):
        self.stacklayout.setCurrentIndex(1)

    def activate_tab_3(self):
        self.stacklayout.setCurrentIndex(2)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()