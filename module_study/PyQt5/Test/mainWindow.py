import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QAction, QStatusBar
)
from PyQt5.QtGui import QIcon,QKeySequence
from PyQt5.QtCore import Qt,QSize

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("测试程序")
        # 设置窗口的宽度和高度：使用QSize对象定义宽高
        self.setFixedSize(QSize(700, 300))

        # ==================== 主窗口内容设置 ====================
        # 标签
        label = QLabel("Hello!")
        label.setAlignment(Qt.AlignCenter)
        # 在主窗口内容中央显示标签
        self.setCentralWidget(label)

        # =================== 菜单栏设置 ==========================

        # ---------------------- 初始化菜单栏 -------------------
        menu = self.menuBar()

        # ---------------------- 通过QAction创建菜单项 --------------------
        # 创建一个“文件” 菜单项
        button_action = QAction(QIcon("../icons/camera.png"),"文件", self)
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        # -- 添加快捷键
        button_action.setShortcut(QKeySequence("Ctrl+p"))
        # 创建一个“保存” 菜单项
        button_action2 = QAction("保存", self)
        button_action2.triggered.connect(self.onMyToolBarButtonClick)

        # ---------------------- 初始化菜单项 --------------------
        # 通过函数addMenu点击一个菜单
        file_menu = menu.addMenu("&File")
        # 向菜单中添加 “菜单项”
        file_menu.addAction(button_action)
        # -- 分割线
        file_menu.addSeparator()
        # 向菜单中添加一个 “子菜单”
        file_submenu = file_menu.addMenu("Submenu")
        # 向子菜单中添加 “菜单项”
        file_submenu.addAction(button_action2)

    def onMyToolBarButtonClick(self, s):
        print("click", s)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()