import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QApplication, QLabel, QMainWindow, QMenu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    # 在子类上创建一个名为 的方法contextMenuEvent，它将接收该类型的所有事件。
    def contextMenuEvent(self, e):
        context = QMenu(self)
        # 往菜单栏添加二级菜单,并在其下添加菜单项
        file = context.addMenu("文件")
        new = file.addAction(QAction("新建", self))
        self.save = file.addAction(QAction("保存", self))
        self.save.triggered.connect(self.saveMenu)

        # 给菜单项目添加菜单项
        context.addAction(QAction("刷新", self))
        context.addAction(QAction("格式化", self))
        context.addAction(QAction("关闭", self))

        # 将初始位置传递给exec函数时，这必须相对于定义时传入的父级。在本例中，我们self作为父级传递，因此我们可以使用全局位置。
        context.exec(e.globalPos())

    def saveMenu(self):
        print(self.save.text())

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()