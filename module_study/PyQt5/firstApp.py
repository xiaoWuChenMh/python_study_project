import sys

from PyQt5.QtCore import QSize, Qt
# 从模块中导入 需要的小部件 和 QApplication应用程序处理程，不建议直接使用*
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):

    # 子类化Qt类时，您必须始终调用 super__init__函数以允许 Qt 设置该对象。
    def __init__(self):
        super().__init__()
        # 设置主窗口的标题
        self.setWindowTitle("My App")
        # 设置窗口的宽度和高度：使用QSize对象定义宽高
        self.setFixedSize(QSize(400, 300))
        # 创建一个小部件-按钮
        button = QPushButton("Press Me!")

        # Set the central widget of the Window. 将小部件放置到窗口的中央
        self.setCentralWidget(button)

# 创建实例QApplication，并传入命令行参数（sys.argv），不需要使用命令行参数传入空列表（[]）
app = QApplication(sys.argv)

# 创建窗口对象（窗口：保存应用程序的用户界面 ）
window = MainWindow()

# 使窗口对象可见
window.show()

# 启动事件循环
app.exec()
