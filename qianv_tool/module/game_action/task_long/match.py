
import time
from qianv_tool.module.logger import logger
from qianv_tool.module.base.button_match import ButtonMatch
from qianv_tool.module.game_action.task_long.assets import *
from qianv_tool.module.game_action.mian_window.assets import HOME_TASK_FIRST_IS_YAO,HOME_TASK_FIRST_IS_SHI


class Match:

    def __init__( self, devices, serial, reply_wait ):
        self.buttonMatch = ButtonMatch()
        self.devices: Devices = devices
        self.serial = serial
        self.reply_wait = reply_wait
        self.long_text = ['条龙','龙']

    def is_task_map( self ):
        """
        是否还在任务地图, 有喇叭干扰时会判断失败。
        """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image,TASK_LONG_IS_MAP, offset=(-3,-1)):
            return True
        else:
            return False

    def is_task_finsh_frame( self ):
        """
        是否一轮任务结束了时的弹框
        """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image,TASK_LONG_TASK_RECEIVE, offset=(0,-5)):
            return True
        else:
            return False

    def is_task_finsh( self ):
        """
        一轮任务结束，点击继续执行
        """
        if self.is_task_finsh_frame():
            self.devices.click(self.serial, TASK_LONG_TASK_RECEIVE)
            return True
        else:
            return False

    def click_first_task_list_area_strict( self ):
        """
        严谨的判断：是否点击第一个任务列表的区域,即一条龙任务
        """
        image = self.devices.device_screenshot(self.serial)
        offset = self.__is_task_first_offset()
        if self.buttonMatch.word_match(image,TASK_LONG_FIRST_LIST,text=self.long_text,offset=offset):
            self.devices.click(self.serial, TASK_LONG_FIRST_LIST, offset=offset)
            return True
        else:
            return False


    def click_first_task_list_area( self ):
        """
        点击第一个任务列表的区域,即一条龙任务
        """
        offset = self.__is_task_first_offset(15)
        image = self.devices.device_screenshot(self.serial)
        self.buttonMatch.word_match(image, TASK_LONG_FIRST_LIST, text=self.long_text, offset=offset)
        self.devices.click(self.serial, TASK_LONG_FIRST_LIST,offset=offset)
        return True

    def __is_task_first_offset( self,move=5 ):
        """
         任务栏是否需要位移
            今日是否有妖兽入侵、十世镜
        """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image, HOME_TASK_FIRST_IS_YAO,offset=(0,0)):
            delta = HOME_TASK_FIRST_IS_YAO.area_size()
            return (0, delta[1]+move, 0, 0)
        elif self.buttonMatch.image_match(image, HOME_TASK_FIRST_IS_SHI,offset=(0,-6)):
            delta = HOME_TASK_FIRST_IS_SHI.area_size()
            return (0, delta[1]+move, 0, delta[1]+5)
        else:
            return (0, 0)


if __name__ == "__main__":

    from qianv_tool.module.devices.devices import Devices

    devices = Devices()
    devices_info = devices.devices_info
    for serial in devices_info:
        if serial=='emulator-5554':
            print(devices_info[serial])
            app = Match(devices, serial, 1)
            # print(app.click_first_task_list_area())


