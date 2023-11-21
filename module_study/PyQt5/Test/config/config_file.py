import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel
)
from module_study.PyQt5.Test.config.config_item import configItem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("带菜单栏的窗口")
        self.setGeometry(100, 100, 500, 400)

        # 创建菜单栏
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("文件")
        fileMenu.addAction("打开")
        fileMenu.addAction("保存")
        fileMenu.addAction("退出")

        # 创建新部件
        my_widget = configItem()

        # 将新部件添加到主窗口
        self.setCentralWidget(my_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())