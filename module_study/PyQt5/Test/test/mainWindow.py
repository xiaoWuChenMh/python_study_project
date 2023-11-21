import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTreeView, QStackedLayout, QTreeWidgetItem
from PyQt5.QtCore import Qt

class TreeMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.tree = QTreeView()
        self.tree.setHeaderHidden(True)
        self.tree.itemClicked.connect(self.handleItemClick)

        root = QTreeWidgetItem(self.tree)
        root.setText(0, "总览")

        task = QTreeWidgetItem(root)
        task.setText(0, "任务")

        subtask1 = QTreeWidgetItem(task)
        subtask1.setText(0, "师门")

        subtask2 = QTreeWidgetItem(task)
        subtask2.setText(0, "一条")

        subtask3 = QTreeWidgetItem(task)
        subtask3.setText(0, "战龙")

        config = QTreeWidgetItem(root)
        config.setText(0, "配置")

        subconfig1 = QTreeWidgetItem(config)
        subconfig1.setText(0, "配置文件")

        subconfig2 = QTreeWidgetItem(config)
        subconfig2.setText(0, "分辨率映射动作")

        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        self.setLayout(layout)

    def handleItemClick(self, item):
        # 根据点击的菜单项切换右1区域的内容
        index = self.tree.indexFromItem(item)
        self.stackedLayout.setCurrentIndex(index.row())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Window Title")
        self.setGeometry(100, 100, 1200, 700)

        leftWidget = QWidget()
        leftLayout = QVBoxLayout()
        leftWidget.setLayout(leftLayout)

        treeMenu = TreeMenu()

        rightWidget = QWidget()
        self.stackedLayout = QStackedLayout()
        rightWidget.setLayout(self.stackedLayout)

        leftLayout.addWidget(treeMenu)
        leftLayout.setStretch(0, 3)
        leftLayout.setStretch(1, 7)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(leftWidget)
        mainLayout.addWidget(rightWidget)

        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())