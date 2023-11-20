import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        # 初始化一个按钮部件，并保留其引用
        self.button = QPushButton("Press Me!")
        # 设置当前按钮的状态为选择
        self.button.setCheckable(True)

        # --------- 通过connect()将信号连接到插槽----------------
        # 为按钮的 点击事件，绑定一个处理函数
        self.button.clicked.connect(self.the_button_was_clicked)
        # 为按钮的点击事件绑定处理函数，并获取事件发出的数据：选中状态
        self.button.clicked.connect(self.the_button_was_toggled)

        # Set the central widget of the Window.
        self.setCentralWidget(self.button)

    # button的自定义插槽，不接受数据
    def the_button_was_clicked(self):
        print("Clicked!")

    # button的自定义插槽，接受数据
    def the_button_was_toggled(self, checked):
        # 获取当前按钮的状态（是否被按下）
        self.button_is_checked = self.button.isChecked()
        # 修改按钮的文本
        self.button.setText("You already clicked me.")
        print("Checked?", checked)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()