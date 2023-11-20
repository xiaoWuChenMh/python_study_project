import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QAction, QStatusBar
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# 工具栏：配置状态信息
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("My Awesome App")

        # ---------------- 主窗口内容设置 ------------------------
        # 标签
        label = QLabel("Hello!")
        label.setAlignment(Qt.AlignCenter)
        # 在主窗口内容中央显示标签
        self.setCentralWidget(label)
        # ---------------- 工具栏设置 ------------------------
        # 初始化一个工具栏
        toolbar = QToolBar("My main toolbar")
        # 将工具栏添加到主窗口上
        self.addToolBar(toolbar)

        # 创建一个“文件” 工具按钮
        button_action1 = QAction("文件", self)
        button_action1.setStatusTip("创建新文件") # 1、添加状态信息
        button_action1.triggered.connect(self.onMyToolBarButtonClick)
        toolbar.addAction(button_action1)

        # 创建一个“保存” 工具按钮
        button_action2 = QAction("保存", self)
        button_action2.setStatusTip("保存文件") # 1、添加状态信息
        button_action2.triggered.connect(self.onMyToolBarButtonClick)
        toolbar.addAction(button_action2)

        # 2、获取状态对象，并传递给主窗口
        self.setStatusBar(QStatusBar(self))

    def onMyToolBarButtonClick(self, s):
        print("click", s)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()