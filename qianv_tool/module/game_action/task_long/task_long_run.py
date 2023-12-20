
import math
import time
from qianv_tool.module.logger import logger
from qianv_tool.module.game_action.task_long.match import Match as MatchLong
from qianv_tool.module.game_action.mian_window.match import Match as MatchMain
from qianv_tool.module.game_action.pop_frame.match import Match as MatchFrame
from qianv_tool.module.game_action.shopping.match import Match as MatchShopping
from qianv_tool.module.game_action.action_window.match import Match as MatchAction



class TaskSmRun:


    def __init__( self, devices, serial, position, reply_wait=1,switch_map=3, dungeon_min_time=120,execute_num=25 ):
        # 设备管理对象
        self.devices: Devices = devices
        # 设备ID
        self.serial = serial
        # 响应等待时间
        self.reply_wait = reply_wait
        # 过图等待时间
        self.switch_map = switch_map
        # 副本最小执行时间（默认120秒）
        self.dungeon_min_time = dungeon_min_time
        # 任务所处位置（0-自动查找，1-第一位，2-第二位，...）
        self.position = position
        # 任务执行次数，默认25次
        self.execute_num = execute_num
        # 执行轮数（向上取整）
        self.execute_round_num = math.ceil(execute_num/5)


        # 任务启动失败重试次数
        self.try_num = 3
        #当前执行次数
        self.curr_execute_num=1
        #当前执行轮次
        self.curr_execute_round_num=1
        # 卡图阈值
        self.stuck_threshold = 3
        self.stuck_try = 0
        # 副本标识(判断副本内计数)
        self.in_dungeon_count =0
        # 进入副本后是否需要睡眠
        self.is_sleep = True


        # 匹配动作行为的对象
        self.match_long = MatchLong(devices,serial,reply_wait)
        self.match_shopping = MatchShopping(devices,serial,reply_wait)
        self.match_main = MatchMain(devices,serial,reply_wait)
        self.match_action = MatchAction(devices,serial,reply_wait)
        self.match_frame = MatchFrame(devices,serial,reply_wait)

    def run(self):
        """
        启动任务，会尝试3次
        """
        try_num = self.try_num
        while try_num>0:
            if self.__activation():
                logger.info(f'日常任务-龙:激活成功,开始执行任务逻辑')
                self.__execution()
                break
            else:
                try_num  = try_num-1
                logger.info(f'日常任务-龙:激活失败,剩余尝试次数{try_num}。')

        if try_num==0:
            logger.info(f'日常任务-龙：激活失败且超过尝试次数，退出任务！')
            return False
        else:
            return True


    def __activation(self):
        """
        激活任务
        """
        self.match_main.restart_team_follow(3)
        if self.match_long.click_first_task_list_area_strict():
            return True
        if self.position==0 and self.match_action.find_task_receive('龙'):
            return True
        else:
            return self.match_action.find_task_position(self.position)



    def __execution(self):
        """
        执行一条龙逻辑
        :return:
        """
        while True:
            self.__npc_dialogue()
            self.__click_task_list()
            self.__continue_task()
            self.__in_dungeon()
            self.__process_stuck
            if self.curr_execute_num>=self.execute_num :
                logger.info(f'日常任务-龙: 当前执行次数达到{self.curr_execute_num},退出任务！')
                break
            if self.curr_execute_round_num>=self.execute_round_num:
                logger.info(f'日常任务-龙: 当前执行轮数达到{self.curr_execute_round_num},退出任务！')
                break

    def __npc_dialogue(self):
        """npc对话相关"""
        if self.match_frame.click_top_npc_dialogue():
            logger.info(f'日常任务-龙:click top npc dialogue;')
            time.sleep(self.reply_wait)
            self.stuck_try += 1
            self.in_dungeon_count = 0
            self.is_sleep = True
        if self.match_frame.click_botton_npc_text_dialogue():
            logger.info(f'日常任务-龙:click npc speak tex;')
            time.sleep(self.reply_wait)

    def __click_task_list(self):
        """点击任务列表"""
        if self.match_long.click_first_task_list_area_strict():
            logger.info(f'日常任务-龙:click task list;')
            time.sleep(self.reply_wait)
            self.match_main.cancel_gua_ji()

    def __continue_task(self):
        """询问是否继续执行任务"""
        if self.match_long.is_task_finsh():
            time.sleep(self.switch_map)
            self.stuck_try = 1
            self.curr_execute_round_num+=1
            logger.info(f'日常任务-龙: 当前准备执行第{self.curr_execute_round_num}轮任务')

    def __in_dungeon(self):
        """副本内执行逻辑"""
        if self.__is_dungeon():
            self.stuck_try = 0
            self.in_dungeon_count+=1
            if self.in_dungeon_count>3 and self.is_sleep:
                logger.info(f'日常任务-龙: 确定刚进入副本，程序睡眠{self.dungeon_min_time}秒')
                time.sleep(self.dungeon_min_time-3)
                self.curr_execute_num+=1
                self.is_sleep =False
                self.match_main.click_gua_ji_area()
            logger.info(f'日常任务-龙: 当前在副本内')
        else:
            self.match_main.cancel_gua_ji()

    def __process_stuck(self):
        """
        流程卡住处理
        :return:
        """
        if self.stuck_try>=self.stuck_threshold:
            self.match_main.restart_team_follow(3)
            self.stuck_try = 0
            time.sleep(self.reply_wait * 3)
        

    def __is_dungeon( self ):
        """
         是否在任务地图内: 因为有喇叭干扰，切图过小无法识别，选择双判断吧，先判图，没找到看文字
        """
        text = ['蛙鸣池', '蒲家村角落', '金銮殿', '金銮', '桃花扇', '湖中屋', '夜宴', '仙人口袋', '水妖', '水妖巢穴']
        if self.match_long.is_task_map():
            return True
        elif self.match_main.is_map(text=text):
            return True
        else:
            return False



if __name__ == "__main__":

    from qianv_tool.module.devices.devices import Devices

    devices = Devices()
    devices_info = devices.devices_info
    for serial in devices_info:
        app = TaskSmRun(devices, serial, 0, execute_num=40,dungeon_min_time=140)
        app.run()
