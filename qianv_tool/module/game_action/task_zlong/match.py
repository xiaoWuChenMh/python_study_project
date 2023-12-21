import math
import time
from qianv_tool.module.logger import logger
from qianv_tool.module.base.button_match import ButtonMatch
from qianv_tool.module.game_action.task_zlong.assets import *
from qianv_tool.module.game_action.mian_window.assets import HOME_TASK_FIRST_IS_YAO

class Match:

    def __init__( self, devices, serial, reply_wait=1 ):
        self.buttonMatch = ButtonMatch()
        self.devices: Devices = devices
        self.serial = serial
        # 窗口切换等待时间
        self.reply_wait = reply_wait
        self.sm_text = ['师门','师','帅']


    def is_task_fail_click(self):
        """ 任务是否失败 """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image,TASK_ZLONG_FAIL,offset=(0,0)):
            self.devices.click(self.serial,TASK_ZLONG_FAIL)
            return True
        else:
            return False

    def is_task_finish_click(self):
        """ 任务是否结束 """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image,TASK_ZLONG_FINISH,offset=(0,0)):
            self.devices.click(self.serial,TASK_ZLONG_FINISH)
            return True
        else:
            return False

    def is_task_kill_click(self):
        """ 是否为刺杀任务 """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image,TASK_ZLONG_Kill,offset=(0,0)):
            self.devices.click(self.serial,TASK_ZLONG_Kill)
            return True
        else:
            return False

    def is_last_deat_click(self):
        """ 最后的任务是否为劲敌"""
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image,TASK_ZLONG_LAST_BEAT,offset=(0,0)):
            self.devices.click(self.serial,TASK_ZLONG_LAST_BEAT)
            return True
        else:
            return False

    def is_last_run_click(self):
        """ 最后的任务是否为幻？？ """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image,TASK_ZLONG_LAST_RUN,offset=(0,0)):
            self.devices.click(self.serial,TASK_ZLONG_LAST_RUN)
            return True
        else:
            return False

    def is_last_run_click(self):
        """ 最后的任务是否为幻？？ """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image,TASK_ZLONG_LAST_RUN,offset=(0,0)):
            self.devices.click(self.serial,TASK_ZLONG_LAST_RUN)
            return True
        else:
            return False

    def is_out_map_tag(self):
        """ 是否为出副本标识 """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image,TASK_ZLONG_OUT_MAP_TAG,offset=(0,0)):
            return True
        else:
            return False




if __name__ == "__main__":


    from qianv_tool.module.devices.devices import Devices

    # devices = Devices()
    # devices_info = devices.devices_info
    # for serial in devices_info:
    #     if serial=='emulator-5554':
    #         print(devices_info[serial])
    #         app = Match(devices, serial)
    #         print(app.calculate_points())


