
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton,QHBoxLayout,QGridLayout,QFrame
from PyQt5.QtCore import Qt

class configItem(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addLayout(self.actionDesc())
        layout.addLayout(self.line())

        self.setLayout(layout)



    def actionDesc(self):
        layout = QGridLayout()

        layout.addWidget(self.leftLable("动作名称:"), 0, 0, 1, 3)
        layout.addWidget(self.leftLable("动作AAA"), 0, 1, 1, 7)

        layout.addWidget(self.leftLable("坐标类型:"), 1, 0, 1, 3)
        layout.addWidget(self.leftLable("单点坐标"), 1, 1, 1, 7)

        layout.addWidget(self.leftLable("动作描述:"), 2, 0, 1, 3)
        layout.addWidget(self.leftLable("描述描描述描述描述描述描述描述描述描"), 2, 1, 1, 7)

        layout.addWidget(self.leftLable("图片样例:"), 3, 0, 1, 3)
        layout.addWidget(self.leftLable("图片样例"), 3, 1, 1, 7)

        return layout

    def leftLable(self,name):
        lable = QLabel(name)
        lable.setAlignment(Qt.AlignLeft)
        return lable

    # 创建一条被包裹在布局中的横线
    def line(self):
        # 创建一个QFrame对象
        line = QFrame(self)
        # 设置横线的样式为水平方向
        line.setFrameShape(QFrame.HLine)
        layout = QHBoxLayout()
        layout.addWidget(line)
        return layout