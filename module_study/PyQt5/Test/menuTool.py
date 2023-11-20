from PyQt5.QtWidgets import QAction

class menuTool():
    def __init__(self,parent):
        menu = self.menuBar()
        over_menu = menu.addMenu("总览")
        over_menu.addSeparator()
        task_menu = menu.addMenu("任务")
        task_menu.addSeparator()
        tool_menu = menu.addMenu("配置")
        tool_menu.addSeparator()

        # 创建一个“动作配置” 菜单项
        config_file = QAction("配置文件", parent)
        config_file.triggered.connect(self.onMyToolBarButtonClick)
        action_mapping = QAction("窗口尺寸点击映射", parent)
        action_mapping.triggered.connect(self.onMyToolBarButtonClick)
        tool_menu.addAction(config_file)
        tool_menu.addAction(action_mapping)


    def onMyToolBarButtonClick(self, s):
        print("click", s)