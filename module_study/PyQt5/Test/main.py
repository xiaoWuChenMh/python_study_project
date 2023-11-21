import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QStackedLayout,
    QDesktopWidget
)
from module_study.PyQt5.Test.tree_menu import TreeMenu

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("应用程序")
        self.setGeometry(100, 100, 1200, 700)

        self.menuMapping = {'师门': 0, '一条': 1, '战龙': 2, '配置文件': 3, '分辨率映射动作': 4}

        # 初始化窗口布局
        self.windowLayout()

        # 创建树形菜单
        self.initMenu()

        # 设置右侧操作栏
        self.initOperatingArea()

    # 窗口布局
    def windowLayout(self):
        """
         主窗口：左侧窗口、右侧窗口
         将窗口以移动到屏幕中央区域
        :return:
        """

        # 创建主窗口的布局
        main_layout = QHBoxLayout()

        # 创建左侧区域的布局
        self.left_layout = QVBoxLayout()

        # 创建右侧区域的布局
        self.right_layout = QStackedLayout()

        # 设置左右比例为3:7
        main_layout.addLayout(self.left_layout, 3)
        main_layout.addLayout(self.right_layout, 7)

        # 创建主窗口的中心部件，并设置布局
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # 将窗口移动到屏幕中央
        screenGeometry = QDesktopWidget().screenGeometry()
        x = (screenGeometry.width() - self.width()) // 2
        y = (screenGeometry.height() - self.height()) // 2
        self.move(x, y)

    # 初始菜单栏
    def initMenu(self):

        # 创建树形菜单
        self.tree_view = TreeMenu()

        # 将树形菜单添加到左侧布局中
        self.left_layout.addWidget(self.tree_view)

        # 连接树形菜单的点击信号到槽函数
        self.tree_view.clicked.connect(self.handle_menu_click)

    # 初始化右侧操作栏
    def initOperatingArea(self):
        self.right_layout.addWidget(QLabel("师门内容"))
        self.right_layout.addWidget(QLabel("一条内容"))
        self.right_layout.addWidget(QLabel("战龙内容"))
        self.right_layout.addWidget(QLabel("配置文件内容"))
        self.right_layout.addWidget(QLabel("分辨率映射动作内容"))
        # TODO: 需要将各个页面的内容进行初始化

    # 菜单栏项目点击处理逻辑
    def handle_menu_click(self, index):
        item = self.tree_view.model.itemFromIndex(index)
        # 二级菜单项被点击
        if item.parent():
            text = item.text()
            stackedIndex = self.menuMapping[text]
            # 堆叠布局可以快速切换页面
            self.right_layout.setCurrentIndex(stackedIndex)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

