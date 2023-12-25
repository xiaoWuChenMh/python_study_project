
import time
from qianv_tool.module.logger import logger
from qianv_tool.module.base.button_match import ButtonMatch
from qianv_tool.module.game_action.action_window.assets import *


class Match:

    def __init__( self, devices, serial, reply_wait):
        self.buttonMatch = ButtonMatch()
        self.devices: Devices = devices
        self.serial = serial
        self.reply_wait = reply_wait
        # 活动按钮是否被点击了
        self.action_button_click = False



    def find_task_receive( self ,text, reply_wait=1):
        """
         查找，并领取任务，因为喇叭和飘花会影响文字识别，所以只有在活动页面内就多次尝试寻找并点击，所以要不要加一个根据位置直接点击的（我觉得很有必要）？
         text:活动文本，师门、龙、重温、宗派、货运、门派、战龙、跑商
         正常流程：点击“参与”，会关闭活动页；
         异常流程：
            1、喇叭和飘花，需要等它们的影响消失后才能准确识别（不建议比较活的大区使用文字识别）
            2、当前已经参与了: 如果找到 且 没有退出活动页面 就算参与状态，需要操作退出活动窗口
        注意1:正常流程能激活任务，异常流程2无法激活任务，还需要点击任务栏，默认点第一个吧
        注意2：返回True的情况：1没有打开活动窗口；2、激活任务；3、任务已参与；

        """
        result = False
        image = self.devices.device_screenshot(self.serial)
        statu = not self.buttonMatch.image_match(image, ACTION_WINDOW_CLOSE, offset=(-2,-6))
        while not statu :
            delta = ACTION_WINDOW_TASK_SITE.area_size()
            delta = (delta[0]-6, delta[1])
            target_button = self.buttonMatch.grid_button_word_match(image, ACTION_WINDOW_TASK_TAG, delta, (2, 4), text, offset=(-2,-3),)
            if target_button:
                self.devices.click(self.serial, target_button)
                time.sleep(reply_wait)
                image = self.devices.device_screenshot(self.serial)
                statu = True
                result = True
                self.action_button_click = True
            else:
                self.devices.click(self.serial, ACTION_WINDOW_CLOSE)
                time.sleep(reply_wait)
                image = self.devices.device_screenshot(self.serial)
                statu = not self.buttonMatch.image_match(image, ACTION_WINDOW_CLOSE, offset=(-2,-6))
            # 找到任务 且 任务窗口还未关闭，说明当前任务已接
            if statu and  self.buttonMatch.image_match(image, ACTION_WINDOW_CLOSE, offset=(-2, -6)):
                self.devices.click(self.serial, ACTION_WINDOW_CLOSE)
                time.sleep(reply_wait)
                image = self.devices.device_screenshot(self.serial)
            # 当已参与了任务，上一个关闭只会消除浮层，所以还得需要一个关闭操作
            if statu and  self.buttonMatch.image_match(image, ACTION_WINDOW_CLOSE, offset=(-2, -6)):
                self.devices.click(self.serial, ACTION_WINDOW_CLOSE)
                self.action_button_click = False
                time.sleep(reply_wait)
        return statu and result

    def is_active_window(self):
        """
         当前是否为活动窗口
        """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image, ACTION_WINDOW_CLOSE, offset=(-2, -6)):
            return True
        else:
            return False
    def find_task_position(self,position, text, reply_wait):
        """
        查找指定位置的“参与” 和 “已参加”按钮后，进行后续操作
        :param position:
        :return:
        """
        image = self.devices.device_screenshot(self.serial)
        if position >=1 and position <= 8:
            ACTION_WINDOW_BUTTON, offset = self.__position_button_mapping(position)
            if self.buttonMatch.image_match(image, ACTION_WINDOW_BUTTON, offset=offset):
                self.devices.click(self.serial, ACTION_WINDOW_BUTTON)
                time.sleep(reply_wait)
                self.action_button_click = True
            else:
                self.action_button_click = False
            image = self.devices.device_screenshot(self.serial)
            if self.buttonMatch.image_match(image, ACTION_WINDOW_CLOSE, offset=(-2, -6)):
                self.devices.click(self.serial, ACTION_WINDOW_CLOSE)
            return True
        else :
            return self.find_task_receive(text,reply_wait)

    def __position_button_mapping( self, position):
        if position == 1 :
           return ACTION_WINDOW_BUTTON1,(8, 5, 0 ,-5)
        elif position == 2 :
            return ACTION_WINDOW_BUTTON2,(5, 6, -5 ,-6)
        elif position == 3 :
           return ACTION_WINDOW_BUTTON3,(5, 5, -8 ,-3)
        elif position == 4 :
            return ACTION_WINDOW_BUTTON4,(5, 5, -8 ,-3)
        elif position == 5 :
            return ACTION_WINDOW_BUTTON5,(5, 5, -8 ,-6)
        elif position == 6 :
            return ACTION_WINDOW_BUTTON6,(8, 8, -3 ,-4)
        elif position == 7 :
            return ACTION_WINDOW_BUTTON7,(5, 5, -8 ,-6)
        else:
            return ACTION_WINDOW_BUTTON8,(8, 8, -1 ,-3)


if __name__ == "__main__":

    from qianv_tool.module.devices.devices import Devices

    devices = Devices()
    devices_info = devices.devices_info
    for serial in devices_info:
        if serial=='emulator-5554':
            print(devices_info[serial])
            app = Match(devices, serial,2)
            # print(app.is_map('金陵'))
            print(app.is_active_window())


