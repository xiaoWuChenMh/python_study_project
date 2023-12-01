from PyQt5.QtWidgets import QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem,QFont

class TreeMenu(QTreeView):
    def __init__(self):
        super().__init__()
        self.model = QStandardItemModel()
        self.setModel(self.model)

        # 隐藏表头(这样就不会显示行号了）
        self.setHeaderHidden(True)

        # 添加第一级菜单项
        devices_item = QStandardItem("设备")
        run_item = QStandardItem("运行")
        task_item = QStandardItem("任务")
        tool_item = QStandardItem("工具")
        config_item = QStandardItem("配置")
        self.model.appendRow([devices_item])
        self.model.appendRow([run_item])
        self.model.appendRow([task_item])
        self.model.appendRow([tool_item])
        self.model.appendRow([config_item])

        # 添加任务菜单下的二级菜单项
        shi_men_item = QStandardItem("师门")
        yi_long_item = QStandardItem("一条")
        zhan_long_item = QStandardItem("战龙")
        task_item.appendRow([shi_men_item])
        task_item.appendRow([yi_long_item])
        task_item.appendRow([zhan_long_item])

        # 添加配置菜单下的二级菜单项
        config_file_item = QStandardItem("配置文件")
        mapping_item = QStandardItem("分辨率映射动作")
        config_item.appendRow([config_file_item])
        config_item.appendRow([mapping_item])

        # 设置菜单项字体大小为20
        font = QFont()
        font.setPointSize(12)
        devices_item.setFont(font)
        run_item.setFont(font)
        task_item.setFont(font)
        tool_item.setFont(font)
        config_item.setFont(font)
        shi_men_item.setFont(font)
        yi_long_item.setFont(font)
        zhan_long_item.setFont(font)
        config_file_item.setFont(font)
        mapping_item.setFont(font)

        print("树形菜单初始化成功")
