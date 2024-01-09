import math
import time
from qianv_tool.module.logger import logger
from qianv_tool.module.base.button_match import ButtonMatch
from qianv_tool.module.game_action.task_zlong.assets import *
from qianv_tool.module.game_action.mian_window.assets import HOME_TASK_FIRST_IS_YAO,HOME_TASK_FIRST_IS_SHI

class Match:

    def __init__( self, devices, serial, reply_wait=1 ):
        self.buttonMatch = ButtonMatch()
        self.devices: Devices = devices
        self.serial = serial
        # 窗口切换等待时间
        self.reply_wait = reply_wait
        self.zl_text = ['战龙','讽刺','雕像','清理','施展','手段','信物','刺探','更换','资金','劲敌','终结','求生']


    def is_task_fail_click(self):
        """ 任务是否失败-点击放弃任务 """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image,TASK_ZLONG_FAIL,offset=(8,9,0,-9)):
            self.devices.click(self.serial,TASK_ZLONG_FAIL,offset=(8,9,0,-9))
            time.sleep(self.reply_wait)
            return True
        else:
            return False
    def give_up_task(self):
        """ 确定放弃任务 """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image,TASK_ZLONG_FAIL_ABIRT,offset=(0,0)):
            self.devices.click(self.serial,TASK_ZLONG_FAIL_ABIRT,offset=(0,0))
            time.sleep(self.reply_wait)
            return True
        else:
            return False

    def is_task_finish_click(self):
        """ 任务是否结束 """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image,TASK_ZLONG_FINISH,offset=(0,0)):
            self.devices.click(self.serial,TASK_ZLONG_FINISH,offset=(0,0))
            return True
        else:
            return False

    def is_task_kill_click(self, input_image=None):
        """ 是否为刺杀任务 """
        image = self.devices.device_screenshot(self.serial) if input_image is None else input_image
        if self.buttonMatch.image_match(image,TASK_ZLONG_Kill,offset=(0,0)):
            self.devices.click(self.serial,TASK_ZLONG_Kill,offset=(0,0))
            return True
        else:
            return False

    def is_last_deat_click(self, input_image=None):
        """ 最后的任务是否为劲敌"""
        image = self.devices.device_screenshot(self.serial) if input_image is None else input_image
        if self.buttonMatch.image_match(image,TASK_ZLONG_LAST_BEAT,offset=(0,0)):
            self.devices.click(self.serial,TASK_ZLONG_LAST_BEAT,offset=(0,0))
            return True
        else:
            return False

    def is_last_run_click(self, input_image=None):
        """ 最后的任务是否为幻？？ """
        image = self.devices.device_screenshot(self.serial) if input_image is None else input_image
        if self.buttonMatch.image_match(image,TASK_ZLONG_LAST_RUN,offset=(0,0)):
            self.devices.click(self.serial,TASK_ZLONG_LAST_RUN,offset=(0,0))
            return True
        else:
            return False


    def is_out_map_tag(self):
        """ 是否为出副本标识 """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image,TASK_ZLONG_OUT_MAP_TAG,offset=(-9,-8)):
            return True
        else:
            return False


    def use_prop( self , input_image=None):
        """ 使用道具 """
        image = self.devices.device_screenshot(self.serial) if input_image is None else input_image
        if self.buttonMatch.image_match(image, TASK_ZLOONG_USE_PROP, offset=(-2,-7)):
            self.devices.click(self.serial, TASK_ZLOONG_USE_PROP, offset=(-2,-7))
            return True
        return False

    def is_curr_task_finish( self ):
        """判断当前任务是否完成"""
        image = self.devices.device_screenshot(self.serial)
        offset = self.__is_task_first_offset()
        if self.buttonMatch.word_match(image,TASK_ZLONG_FIRST_LIST,text='刺探完成',offset=offset):
            return True
        return False

    def click_first_task_list_area_strict( self ):
        """
        严谨的判断：是否点击第一个任务列表的区域,即战龙
        """
        image = self.devices.device_screenshot(self.serial)
        offset = self.__is_task_first_offset()
        if self.buttonMatch.word_match(image,TASK_ZLONG_FIRST_LIST,text=self.zl_text,offset=offset):
            self.devices.click(self.serial, TASK_ZLONG_FIRST_LIST, offset)
            return True
        else:
            return False

    def click_first_task_list_area( self ):
        """
        非严谨的判断：是否点击第一个任务列表的区域,即战龙
        """
        image = self.devices.device_screenshot(self.serial)
        offset = self.__is_task_first_offset()
        self.devices.click(self.serial, TASK_ZLONG_FIRST_LIST, offset=offset)
        return True

    def run_positions_exe( self ):
        """
        求生任务中跑动的位置
        """
        time.sleep(4)
        self.devices.click(self.serial, TASK_ZLONG_ESCAPE_STEP_1)
        time.sleep(2)
        self.devices.click(self.serial, TASK_ZLONG_ESCAPE_STEP_2)
        time.sleep(1)
        self.devices.click(self.serial, TASK_ZLONG_ESCAPE_STEP_3)
        time.sleep(1)
        self.devices.click(self.serial, TASK_ZLONG_ESCAPE_STEP_4)
        time.sleep(2)
        self.devices.click(self.serial, TASK_ZLONG_ESCAPE_STEP_5)
        time.sleep(2)
        self.devices.click(self.serial, TASK_ZLONG_ESCAPE_STEP_6)
        time.sleep(2)
        self.devices.click(self.serial, TASK_ZLONG_ESCAPE_STEP_7)
        time.sleep(2)
        self.devices.click(self.serial, TASK_ZLONG_ESCAPE_STEP_8)
        time.sleep(3)
        self.devices.click(self.serial, TASK_ZLONG_ESCAPE_STEP_1)
    def come_bank( self ):
        """
         点击帮会窗口
        """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image,TASK_ZLONG_BAND, offset=(4, 5, -4, -4)):
            self.devices.click(self.serial, TASK_ZLONG_BAND, offset=(4, 5, -4, -4))
            time.sleep(self.reply_wait)
            return self.__click_come_bank_button()
        else:
            self.devices.click(self.serial, TASK_ZLONG_CLICK_TOOL, offset=(0, 0))
            time.sleep(self.reply_wait)
            self.devices.click(self.serial, TASK_ZLONG_BAND, offset=(0, 0))
            time.sleep(self.reply_wait)
            return self.__click_come_bank_button()

    def __click_come_bank_button( self ):
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image, TASK_ZLONG_COME_BAND, offset=(4, 5, -4, -4)):
            self.devices.click(self.serial, TASK_ZLONG_COME_BAND, offset=(4, 5, -4, -4))
            time.sleep(self.reply_wait)
            self.devices.click(self.serial, TASK_ZLONG_BAND_CLOSE, offset=(7, 9, -4, -4))
            return True
        else:
            return False

    def get_screenshot( self ):
        """获取截图"""
        image = self.devices.device_screenshot(self.serial)
        return image

    def __is_task_first_offset( self ):
        """
         任务栏是否需要位移
            今日是否有妖兽入侵、十世镜
        """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image, HOME_TASK_FIRST_IS_YAO,offset=(0,0)):
            delta = HOME_TASK_FIRST_IS_YAO.area_size()
            return (0, delta[1]+5, 0, delta[1]+5)
        elif self.buttonMatch.image_match(image, HOME_TASK_FIRST_IS_SHI,offset=(0,-6)):
            delta = HOME_TASK_FIRST_IS_SHI.area_size()
            return (0, delta[1]+2, 0,delta[1]+2)
        else:
            return (0, 0)

if __name__ == "__main__":


    from qianv_tool.module.devices.devices import Devices

    devices = Devices()
    devices_info = devices.devices_info
    for serial in devices_info:
        if serial=='emulator-5558':
            print(devices_info[serial])
            app = Match(devices, serial)
            # print(app.is_run())
            print(app.is_curr_task_finish())


