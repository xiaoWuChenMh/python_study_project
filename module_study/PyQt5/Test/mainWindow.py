import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QAction, QStatusBar
)
from PyQt5.QtGui import QIcon,QKeySequence
from PyQt5.QtCore import Qt,QSize
from module_study.PyQt5.parts.customize.Color import Color

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
        menuTool.menuTool(self)

    def onMyToolBarButtonClick(self, s):
        print("click", s)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()