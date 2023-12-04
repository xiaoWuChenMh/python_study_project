import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QLabel

class MyApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Menu and Content Example')

        # 创建水平布局
        main_layout = QHBoxLayout()

        # 创建菜单
        menu_layout = QVBoxLayout()
        menu_label = QLabel("Menu")
        menu_combo_box = QComboBox()
        menu_combo_box.addItem("Option 1")
        menu_combo_box.addItem("Option 2")
        menu_combo_box.addItem("Option 3")
        menu_layout.addWidget(menu_label)
        menu_layout.addWidget(menu_combo_box)

        # 创建内容
        content_layout = QVBoxLayout()

        # 默认内容
        default_widget = QWidget()
        default_layout = QVBoxLayout()
        default_label = QLabel("Default Content")
        default_input = QLineEdit()
        default_button = QPushButton("Submit")
        default_layout.addWidget(default_label)
        default_layout.addWidget(default_input)
        default_layout.addWidget(default_button)
        default_widget.setLayout(default_layout)

        # 选项1内容
        option1_widget = QWidget()
        option1_layout = QVBoxLayout()
        option1_label = QLabel("Option 1 Content")
        option1_input = QLineEdit()
        option1_button = QPushButton("Submit")
        option1_layout.addWidget(option1_label)
        option1_layout.addWidget(option1_input)
        option1_layout.addWidget(option1_button)
        option1_widget.setLayout(option1_layout)

        # 选项2内容
        option2_widget = QWidget()
        option2_layout = QVBoxLayout()
        option2_label = QLabel("Option 2 Content")
        option2_input = QLineEdit()
        option2_button = QPushButton("Submit")
        option2_layout.addWidget(option2_label)
        option2_layout.addWidget(option2_input)
        option2_layout.addWidget(option2_button)
        option2_widget.setLayout(option2_layout)

        # 添加内容到内容布局中
        content_layout.addWidget(default_widget)
        content_layout.addWidget(option1_widget)
        content_layout.addWidget(option2_widget)

        # 默认情况下显示默认内容
        option1_widget.hide()
        option2_widget.hide()

        # 将菜单和内容添加到主布局中
        main_layout.addLayout(menu_layout)
        main_layout.addLayout(content_layout)

        # 设置菜单选项变动时的响应
        menu_combo_box.currentIndexChanged.connect(
            lambda: self.on_menu_change(menu_combo_box.currentIndex(), [default_widget, option1_widget, option2_widget])
        )

        # 设置主布局
        self.setLayout(main_layout)

    def on_menu_change(self, index, widgets):
        for i, widget in enumerate(widgets):
            if i == index:
                widget.show()
            else:
                widget.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApplication()
    window.show()
    sys.exit(app.exec_())