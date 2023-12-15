
from qianv_tool.module.logger import logger
from qianv_tool.module.base.button import ButtonGrid
from qianv_tool.module.devices.devices import Devices
from qianv_tool.module.base.button_match import ButtonMatch
from qianv_tool.module.game_action.mian_window.assets import *

class Match:

    def __init__(self,devices,serial):
        self.buttonMatch = ButtonMatch()
        self.devices:Devices = devices
        self.serial = serial

    def start_gua_ji(self):
        """
         启动挂机：如果没有就启动
        :return:
        """
        image = self.devices.screenshot(self.serial)
        if self.buttonMatch.word_match(image,START_GUA_JI,model=2):
            self.devices.click(self.serial,START_GUA_JI)
            return True
        # 检查是否在过挂机中，是，返回True
        else:
            return False

    def cancel_gua_ji(self):
        image = self.devices.screenshot(self.serial)
        # 检查是否已启动，是，击它，返回True
        # 检查是否未启动，是，返回True
        pass

    def open_team(self):
        # 检查当前是否打开了队伍
        # 没有就点击
        pass

    def open_task(self):
        # 检查当前是否打开了任务
        # 没有就点击
        pass

    def click_dialog(self):
        # 检查当前是否有对话
        # 有就点击
        pass

    def click_action(self):
        # 检查当前是否有动作页面
        # 有就点击第一个
        pass

    def is_map(self):
        # 是否处在某某地图中
        pass