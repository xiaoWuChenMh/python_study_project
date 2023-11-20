import sys

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press me for a dialog!")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    def button_clicked(self, s):
        # 初始化 QMessageBox 对象
        dlg = QMessageBox(self)
        # 设置：对话框标题
        dlg.setWindowTitle("I have a question!")
        # 设置：对话框内文本
        dlg.setText("This is a simple dialog")
        # 设置：对话框内包含的按钮
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # 设置: 图标
        dlg.setIcon(QMessageBox.Question)
        # 启动它：会创建一个全新的事件循环（特定于对话框）
        button = dlg.exec()
        # 判断对话框的返回结果
        if button == QMessageBox.Yes:
            print("Yes!")
        else:
            print("No!")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()