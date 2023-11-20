import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QAction, QStatusBar
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# 工具栏：初识
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

        # 声明一个工具按钮，参数：工具按钮名称，操作的父级角色 (这里传递的是主窗口的引用）
        button_action = QAction("Your button", self)
        button_action.setStatusTip("This is your button")
        # 为工具按钮绑定一个事件处理函数
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        # 打开QAction的可切换开关，让triggered信号能传递该信息，会交替输出True和False。
        button_action.setCheckable(True)
        # 将工具按钮添加到工具栏中
        toolbar.addAction(button_action)

    def onMyToolBarButtonClick(self, s):
        print("click", s)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()