
import time

from qianv_tool.module.logger import logger
from qianv_tool.module.base.button_match import ButtonMatch
from qianv_tool.module.game_action.mian_window.assets import *

class Match:

    def __init__(self,devices, serial, reply_wait):
        self.buttonMatch = ButtonMatch()
        self.devices:Devices = devices
        self.serial = serial
        self.reply_wait = reply_wait

    def start_gua_ji(self):
        """
         启动挂机:
            检查挂机功能是否未启动，是-点击-返回true；否-首先检查挂机功能是否启动，是-返回true；否-返回False
        :return:
        """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.word_match(image,HOME_GUA_JI_NOT,model=2):
            self.devices.click(self.serial,HOME_GUA_JI_NOT)
            return True
        if self.buttonMatch.word_match(image,HOME_GUA_JI_HAVE,model=1):
            return True
        else:
            return False

    def cancel_gua_ji(self):
        """
         取消挂机：
            首先检查挂机功能是否启动，是-点击-返回true；否-检查挂机功能是否未启动，是-返回true；否-返回False
        """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.word_match(image, HOME_GUA_JI_HAVE, model=1):
            self.devices.click(self.serial, HOME_GUA_JI_HAVE)
            return True
        if self.buttonMatch.word_match(image, HOME_GUA_JI_NOT, model=1):
            return True
        else:
            return False
    def click_gua_ji_area( self ):
        """
        点击挂机位置区域
        """
        image = self.devices.device_screenshot(self.serial)
        self.devices.click(self.serial, HOME_GUA_JI_NOT)
        return True

    def click_first_task_list_area( self ):
        """
        点击第一个任务列表的区域
        注意周周六日的活动影响，会有偏移
        """
        offset=self.__is_yao_shou()
        self.devices.click(self.serial, HOME_TASK_FIRST_COMM,offset)
        return True

    def open_team_list(self):
        """
        打开队伍列表,首先检查是否打开了，没有就打开
        """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image, HOME_SELECT_TEAM,offset=(-4,0),interval=1,threshold=0.83):
            return True
        elif self.buttonMatch.image_match(image, HOME_SELECT_TASK, interval=0.5):
            self.devices.click(self.serial, HOME_SELECT_TEAM)
            return True
        else:
            return False

    def open_task_list(self):
        """
        打开任务列表,首先检查是否打开了，没有就打开
        """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image, HOME_SELECT_TASK):
            return True
        elif self.buttonMatch.image_match(image, HOME_SELECT_TEAM,offset=(-4,0),interval=0.5,threshold=0.83):
            self.devices.click(self.serial, HOME_SELECT_TASK)
            return True
        else:
            return False

    def open_active_window(self):
        """
         打开活动窗口
        """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image, HOME_ACTIVE,offset=(-7,-1),interval=0.5):
            self.devices.click(self.serial, HOME_ACTIVE)
            return True
        else:
            return False
    def is_map(self,text,model=1):
        """
        通过小地图的标题来判断当前是否处在某个地图中
        :param text: 待匹配的地图标题
        :param model:匹配模式 1-模糊（默认）；2-严格
        :return:
        """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.word_match(image, HOME_MAP_TITLE, model=model, text=text):
            return True
        else:
            return False
    def click_map_line_area(self):
        """
         点击地图线路区域
        """
        image = self.devices.device_screenshot(self.serial)
        self.devices.click(self.serial, HOME_MAP_TITLE)
        return True

    def restart_team_follow( self,min_people_num=3 ):
        """
         重新启动队伍跟随
        :param min_people_num:最小队伍任务，默认3人
        :return:
        """
        if not self.open_team_list():
            return False
        image = self.devices.device_screenshot(self.serial)
        if min_people_num<=5 and self.buttonMatch.image_match(image, HOME_5TEM_FOLLOW, offset=(-6,-7)):
            self.devices.click(self.serial, HOME_5TEM_FOLLOW_CANCEL)
            time.sleep(1)  # 等待1秒钟
            self.devices.click(self.serial, HOME_5TEM_FOLLOW)
            return True
        elif min_people_num<=4 and self.buttonMatch.image_match(image, HOME_4TEM_FOLLOW, offset=(6,5,-4,-5)):
            self.devices.click(self.serial, HOME_4TEM_FOLLOW_CANCEL)
            time.sleep(1)  # 等待1秒钟
            self.devices.click(self.serial, HOME_4TEM_FOLLOW)
            return True
        elif min_people_num<=3 and self.buttonMatch.image_match(image, HOME_3TEM_FOLLOW, offset=(-6,-5)):
            self.devices.click(self.serial, HOME_3TEM_FOLLOW_CANCEL)
            time.sleep(1)  # 等待1秒钟
            self.devices.click(self.serial, HOME_3TEM_FOLLOW)
            return True
        elif min_people_num<=2 and self.buttonMatch.image_match(image, HOME_2TEM_FOLLOW, offset=(-5,-6)) :
            self.devices.click(self.serial, HOME_2TEM_FOLLOW_CANCEL)
            time.sleep(1)  # 等待1秒钟
            self.devices.click(self.serial, HOME_2TEM_FOLLOW)
            return True
        else:
            return False

    def press_drug_quick(self):
        """按下药品快捷键"""
        self.devices.click(self.serial, HOME_DRUG_QUICK)

    def use_skill(self,index):
        """
        根据技能索引，释放相应的技能
        :param index:
        :return:
        """
        if index == 1:
            self.devices.click(self.serial,HOME_SKILL_BUTTON1)
        elif index == 2:
            self.devices.click(self.serial,HOME_SKILL_BUTTON2)
        elif index == 3:
            self.devices.click(self.serial,HOME_SKILL_BUTTON3)
        elif index == 4:
            self.devices.click(self.serial,HOME_SKILL_BUTTON4)
        elif index == 5:
            self.devices.click(self.serial,HOME_SKILL_BUTTON5)
        else:
            return False
        return True

    def __is_yao_shou( self ):
        """今日是否有妖兽入侵"""
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.word_match(image, HOME_TASK_FIRST_IS_YAO,text='妖兽入侵'):
            delta = HOME_TASK_FIRST_IS_YAO.area_size()
            return (0,delta[1]+5)
        else:
            return (0,0)

if __name__ == "__main__":

    from qianv_tool.module.devices.devices import Devices
    devices = Devices()
    devices_info = devices.devices_info
    for serial in devices_info:
        print(devices_info[serial])
        if serial!='emulator-5554':
            app = Match(devices, serial, 1)
            print(app.is_map('湖中屋'))
            # print(app.open_active_window())

