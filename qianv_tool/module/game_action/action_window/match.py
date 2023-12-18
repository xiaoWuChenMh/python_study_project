
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



    def find_task_receive( self ,text):
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
                image = self.devices.device_screenshot(self.serial)
                statu = True
            else:
                image = self.devices.device_screenshot(self.serial)
                statu = not self.buttonMatch.image_match(image, ACTION_WINDOW_CLOSE, offset=(-2,-6))
            # 找到任务 且 任务窗口还未关闭，说明当前任务已接
            if statu and  self.buttonMatch.image_match(image, ACTION_WINDOW_CLOSE, offset=(-2, -6)):
                self.devices.click(self.serial, ACTION_WINDOW_CLOSE)
                time.sleep(0.5)
                self.devices.click(self.serial, ACTION_WINDOW_CLOSE)
        return statu

    def find_task_position(self,position):
        """
        查找指定位置的“参与” 和 “已参加”按钮后，进行后续操作
        :param position:
        :return:
        """
        #根据位置获取 参与button 和 已参与butotn
        #有参与就点击，有已参与就退出，否则返回False
        pass


if __name__ == "__main__":

    from qianv_tool.module.devices.devices import Devices

    devices = Devices()
    devices_info = devices.devices_info
    for serial in devices_info:
        if serial=='emulator-5554':
            print(devices_info[serial])
            app = Match(devices, serial)
            # print(app.is_map('金陵'))
            print(app.find_task_receive('师门'))


