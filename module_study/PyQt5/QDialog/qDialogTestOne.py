import sys

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton,QDialogButtonBox,QVBoxLayout,QLabel

# 自定义一个对话框
class CustomDialog(QDialog):
    # parent 是初始化该类时传递过来的——对话框父类对象
    def __init__(self,parent=None):
        super().__init__(parent)

        # 对话框标题
        self.setWindowTitle("HELLO!")

        # ------------- 设置对话框包含的按钮 ----------------

        # 要显示 “确定”和 “取消” 按钮
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        # 初始化对话框按钮
        self.buttonBox = QDialogButtonBox(QBtn)
        # 将按钮的.accepted和.rejected信号 与 自定义对话框的处理程序连接起来
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # ------------- 将对话框按钮放置到对话框中 ------------
        # 创建一个布局组件
        self.layout = QVBoxLayout()
        message = QLabel("Something happened, is that OK?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        # 对话框弹出的触发按钮
        button = QPushButton("Press me for a dialog!")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    def button_clicked(self, s):
        print("click", s)

        dlg = CustomDialog(self)
        # 启动它：会创建一个全新的事件循环（特定于对话框）
        if dlg.exec():
            print("Success!")
        else:
            print("Cancel!")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()