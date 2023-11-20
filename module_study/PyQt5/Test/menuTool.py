
class menuTool():
    def __init__(self,parent):
        menu = self.menuBar()
        over_menu = menu.addMenu("总览")
        over_menu.addSeparator()
        task_menu = menu.addMenu("任务")
        task_menu.addSeparator()
        tool_menu = menu.addMenu("工具")
        tool_menu.addSeparator()
