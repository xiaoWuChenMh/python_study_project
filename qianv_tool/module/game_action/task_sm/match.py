
import time
from qianv_tool.module.logger import logger
from qianv_tool.module.base.button_match import ButtonMatch
from qianv_tool.module.game_action.task_sm.assets import *
from qianv_tool.module.game_action.mian_window.assets import HOME_TASK_FIRST_IS_YAO,HOME_TASK_FIRST_IS_SHI

class Match:

    def __init__( self, devices, serial, reply_wait=1 ):
        self.buttonMatch = ButtonMatch()
        self.devices: Devices = devices
        self.serial = serial
        # 窗口切换等待时间
        self.reply_wait = reply_wait
        self.sm_text = ['师门','内奸','研习','拜访','赠言','师父','教训','寻物','巡逻','鬼怪','历练','完成','青凤','河灯']

    def use_prop( self, input_image=None):
        """ 使用道具 """
        image =  image = self.devices.device_screenshot(self.serial) if input_image is None else input_image
        if self.buttonMatch.image_match(image, TASK_SM_USE_PROP, offset=(-2,-7)):
            self.devices.click(self.serial, TASK_SM_USE_PROP)
            return True
        return False


    def is_task_finish( self, input_image=None ):
        """ 任务是否完成"""
        image =  image = self.devices.device_screenshot(self.serial) if input_image is None else input_image
        if self.buttonMatch.image_match(image, TASK_SM_TASK_FINISH, offset=(-2,-7)):
            self.devices.click(self.serial, TASK_SM_TASK_FINISH)
            return True
        return False

    def click_first_task_list_area_strict( self ):
        """
        严谨的判断：是否点击第一个任务列表的区域,即师门
        """
        image = self.devices.device_screenshot(self.serial)
        offset=self.__is_task_first_offset()
        if self.buttonMatch.word_match(image,TASK_SM_FIRST_LIST,text=self.sm_text,offset=offset):
            self.devices.click(self.serial, TASK_SM_FIRST_LIST, offset)
            return True
        else:
            return False

    def is_first_task_list_area_strict( self ):
        """
        严谨的判断：第一个任务列表的区域是否为师门
        """
        image = self.devices.device_screenshot(self.serial)
        offset=self.__is_task_first_offset()
        if self.buttonMatch.word_match(image,TASK_SM_FIRST_LIST,text=self.sm_text,offset=offset):
            return True
        else:
            return False

    def click_first_task_list_area( self ):
        """
        点击第一个任务列表的区域,即师门
        """
        offset=self.__is_task_first_offset()
        self.devices.click(self.serial, TASK_SM_FIRST_LIST,offset)
        return True

    def click_submit_equipment(self, input_image=None):
        """是否触发提交装备"""
        image = self.devices.device_screenshot(self.serial) if input_image is None else input_image
        if self.buttonMatch.image_match(image,TASK_SM_SUBMIT_EQUIPMENT_START,offset=(-5,-6)):
            self.devices.click(self.serial, TASK_SM_SUBMIT_EQUIPMENT_START)
            return True
        else:
            return False
    def is_submit_equipment(self):
        """是否触发提交装备"""
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image,TASK_SM_SUBMIT_EQUIPMENT_START,offset=(-5,-6)):
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

    def submit_equipment_real(self, input_image=None):
        """
         提交装备-正式提交
         TODO:还没有对应的资源按钮对象
        """
        image = self.devices.device_screenshot(self.serial) if input_image is None else input_image
        if self.buttonMatch.image_match(image,TASK_SM_SUBMIT_EQUIPMENT_REAL,offset=(-3,-6)):
            self.devices.click(self.serial, TASK_SM_SUBMIT_EQUIPMENT_REAL)
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

    def is_out_map_tag(self, input_image=None):
        """ 是否为出副本标识 """
        image = self.devices.device_screenshot(self.serial) if input_image is None else input_image
        if self.buttonMatch.image_match(image,TASK_SM_OUT_MAP_TAG,offset=(-9,-8)):
            return True
        else:
            return False

    def click_advanced_notice( self ,input_image=None):
        """点击师门进阶通知"""
        image = self.devices.device_screenshot(self.serial) if input_image is None else input_image
        if self.buttonMatch.image_match(image, TASK_SM_ADVANCED_NOTICE, offset=(-2,-7)):
            self.devices.click(self.serial, TASK_SM_ADVANCED_NOTICE)
            return True
        else:
            return False
    def click_notice_confirm( self ,input_image=None):
        """点击 通知确认按钮"""
        image = self.devices.device_screenshot(self.serial) if input_image is None else input_image
        if self.buttonMatch.image_match(image, TASK_SM_NOTICE_CONFIRM, offset=(-5,-6), interval=0.5,threshold=0.83):
            self.devices.click(self.serial, TASK_SM_NOTICE_CONFIRM,offset=(-5,-6),)
            return True
        else:
            return False
    def click_instance_exit_notice( self ,input_image=None):
        """点击 通知确认按钮"""
        image = self.devices.device_screenshot(self.serial) if input_image is None else input_image
        if self.buttonMatch.image_match(image, TASK_INSTANCE_EXIT_NOTICE, offset=(-2,-7)):
            self.devices.click(self.serial, TASK_INSTANCE_EXIT_NOTICE)
            return True
        else:
            return False
    def get_screenshot( self ):
        """获取截图"""
        image = self.devices.device_screenshot(self.serial)
        return image

    def __is_task_first_offset( self, move=17 ):
        """
         任务栏是否需要位移
            今日是否有妖兽入侵、十世镜
        """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image, HOME_TASK_FIRST_IS_YAO,offset=(0,0)):
            delta = HOME_TASK_FIRST_IS_YAO.area_size()
            return (0, delta[1]+move, 0, delta[1]+move)
        elif self.buttonMatch.image_match(image, HOME_TASK_FIRST_IS_SHI,offset=(0,-6)):
            delta = HOME_TASK_FIRST_IS_SHI.area_size()
            return (0, delta[1]+move, 0,delta[1]+move)
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
            # print(app.is_map('金陵'))
            print(app.click_notice_confirm())


