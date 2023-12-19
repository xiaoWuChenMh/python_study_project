
import time
from qianv_tool.module.logger import logger
from qianv_tool.module.base.button_match import ButtonMatch
from qianv_tool.module.game_action.task_sm.assets import *
from qianv_tool.module.game_action.mian_window.assets import HOME_TASK_FIRST_IS_YAO

class Match:

    def __init__( self, devices, serial, reply_wait=1 ):
        self.buttonMatch = ButtonMatch()
        self.devices: Devices = devices
        self.serial = serial
        # 窗口切换等待时间
        self.reply_wait = reply_wait

    def use_prop( self ):
        """ 使用道具 """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image, TASK_SM_USE_PROP, offset=(-2,-7)):
            self.devices.click(self.serial, TASK_SM_USE_PROP)

            return True
        return False


    def is_task_finish( self ):
        """ 任务是否完成"""
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image, TASK_SM_TASK_FINISH, offset=(-2,-7)):
            self.devices.click(self.serial, TASK_SM_TASK_FINISH)
            return True
        return False

    def click_first_task_list_area_strict( self ):
        """
        严谨的判断：是否点击第一个任务列表的区域,即师门
        """
        image = self.devices.device_screenshot(self.serial)
        offset = (0,0) # self.__is_yao_shou() 不能通过文字识别来判断了，会导致TASK_SM_FIRST_LIST识别不出来，是因为两张图相近，就懒了么？
        if self.buttonMatch.word_match(image,TASK_SM_FIRST_LIST,text=['师门','师'],offset=offset):
            self.devices.click(self.serial, TASK_SM_FIRST_LIST, offset)
            return True
        else:
            return False

    def is_first_task_list_area_strict( self ):
        """
        严谨的判断：第一个任务列表的区域是否为师门
        """
        image = self.devices.device_screenshot(self.serial)
        offset = self.__is_yao_shou()
        if self.buttonMatch.word_match(image,TASK_SM_FIRST_LIST,text='师门',offset=offset):
            return True
        else:
            return False

    def click_first_task_list_area( self ):
        """
        点击第一个任务列表的区域,即师门
        """
        offset=self.__is_yao_shou()
        self.devices.click(self.serial, TASK_SM_FIRST_LIST,offset)
        return True

    def is_submit_equipment(self):
        """是否触发提交装备"""
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image,TASK_SM_SUBMIT_EQUIPMENT_REAL,offset=(-5,-6)):
            self.devices.click(self.serial, TASK_SM_SUBMIT_EQUIPMENT_REAL)
            return True
        else:
            return False
    def click_submit_equipment_buy_other(self):
        """
         提交装备-npc商店购买
         TODO:还没有对应的资源按钮对象
        """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image,TASK_SM_SUBMIT_EQUIPMENT_STORE,offset=(-3,-6)):
            self.devices.click(self.serial, TASK_SM_SUBMIT_EQUIPMENT_STORE)
            return True
        else:
            return False

    def submit_equipment_real(self):
        """
         提交装备-正式提交
         TODO:还没有对应的资源按钮对象
        """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image,TASK_SM_SUBMIT_EQUIPMENT_START,offset=(0,0)):
            self.devices.click(self.serial, TASK_SM_SUBMIT_EQUIPMENT_START)
            return True
        else:
            return False


    def submit_equipment_confirm(self):
        """
         提交装备-确定提交-相对珍贵的装备会需要
         TODO:对应的资源按钮对象里的button属性需要修正
        """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image,TASK_SM_SUBMIT_EQUIPMENT_DECITION,offset=(0,0)):
            self.devices.click(self.serial, TASK_SM_SUBMIT_EQUIPMENT_DECITION)
            return True
        else:
            return False

    def __is_yao_shou( self ):
        """今日是否有妖兽入侵"""
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.word_match(image, HOME_TASK_FIRST_IS_YAO,text='妖兽入侵'):
            delta = HOME_TASK_FIRST_IS_YAO.area_size()
            return (0,delta[1]+5)
        else:
            return (0,0)

    # 提交法宝

    # 进入副本+出副本

if __name__ == "__main__":

    from qianv_tool.module.devices.devices import Devices

    devices = Devices()
    devices_info = devices.devices_info
    for serial in devices_info:
        if serial=='emulator-5554':
            print(devices_info[serial])
            app = Match(devices, serial)
            # print(app.is_map('金陵'))
            print(app.is_submit_equipment())


