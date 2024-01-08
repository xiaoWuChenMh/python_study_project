
import math
import time
import multiprocessing
from qianv_tool.module.logger import logger
from qianv_tool.module.game_action.task_long.match import Match as MatchLong
from qianv_tool.module.game_action.mian_window.match import Match as MatchMain
from qianv_tool.module.game_action.pop_frame.match import Match as MatchFrame
from qianv_tool.module.game_action.shopping.match import Match as MatchShopping
from qianv_tool.module.game_action.action_window.match import Match as MatchAction



class TaskLongRun:


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

        # 任务状态
        self.status = 0
        #状态标记时间
        self.status_tag_time = 0
        #特殊状态需要的超时判断时间（默认60秒）
        self.timeout = 60
        # 任务启动失败重试次数
        self.try_num = 3
        #当前执行次数
        self.curr_execute_num= 0
        #当前执行轮次
        self.curr_execute_round_num= 0
        # 卡图阈值
        self.stuck_threshold = 3
        self.stuck_try = 0
        # 副本标识(判断副本内计数)
        self.in_dungeon_count =1
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
        self.match_main.restart_team_follow()
        if  self.match_main.open_active_window():
            time.sleep(self.reply_wait)
            if self.position==0 and self.match_action.find_task_receive('龙'):
                self.position = self.match_action.buttonMatch.grid_word_index
                self.__activation_status()
                return True
            elif self.position>0 and self.match_action.find_task_position(self.position, '龙'):
                self.__activation_status()
                return True
            else:
                return False
        else:
            return False

    def __activation_status( self ):
        """修改激活状态"""
        if self.match_action.action_button_click:
            self.status = 0
            self.status_tag_time = time.time()
        else:
            self.status = 1

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
            self.__process_stuck()
            self.__status_timeout_decide()
            if self.__is_finish():
                break

    def __npc_dialogue(self):
        """npc对话相关"""
        if self.status in (0,1,2) and self.match_frame.click_top_npc_dialogue():
            time.sleep(self.reply_wait)
            self.stuck_try += 1
            self.in_dungeon_count = 0
            self.is_sleep = True
            if self.status == 2:
                self.status = 3
            if self.status == 0:
                self.status = 1
        while self.status in (1,3) and self.match_frame.click_botton_npc_text_dialogue():
            if self.status == 3:
                self.status = 1

    def __click_task_list(self):
        """点击任务列表"""
        if self.status == 1 and self.match_long.click_first_task_list_area():
            time.sleep(self.reply_wait)

    def __continue_task(self):
        """询问是否继续执行任务"""
        if self.status == 1 and self.match_long.is_task_finsh():
            time.sleep(self.switch_map)
            self.match_long.is_task_finsh()
            self.stuck_try = 1
            self.curr_execute_round_num+=1
            self.status = 2
            logger.info(f'日常任务-龙: 当前准备执行第{self.curr_execute_round_num}轮任务')

    def __in_dungeon(self):
        """副本内执行逻辑"""
        if self.status != 1 :
            return False
        if self.__is_dungeon():
            # 取消跟随【有时候到了副本中还有时跟随状态】
            self.stuck_try = 0
            self.in_dungeon_count+=1
            if self.in_dungeon_count>3 and self.is_sleep:
                logger.info(f'日常任务-龙: 确定刚进入副本，程序睡眠{self.dungeon_min_time}秒')
                self.curr_execute_num+=1
                self.is_sleep =False
                self.match_main.start_gua_ji()
                # 有时会报错：KeyboardInterrupt
                time.sleep(self.dungeon_min_time - 3)
        else:
            self.match_main.cancel_gua_ji()

    def __process_stuck(self):
        """
        流程卡住处理
        :return:
        """
        if self.status == 1 and self.stuck_try>=self.stuck_threshold:
            self.__npc_dialogue()
            self.match_main.restart_team_follow()
            self.stuck_try = 0
            time.sleep(self.switch_map )
        

    def __is_dungeon( self ):
        """
         是否在任务地图内: 因为有喇叭干扰，切图过小无法识别，选择双判断吧，先判图，没找到看文字
        """
        text = ['蛙鸣池', '蒲家村角落', '金銮殿', '金銮', '桃花扇', '湖中屋', '夜宴', '仙人口袋', '水妖', '水妖巢穴']
        if self.match_long.is_task_map():
            logger.info(f'日常任务-龙: 基于图片匹配，得知当前处在副本中')
            return True
        elif self.match_main.is_map(text=text):
            logger.info(f'日常任务-龙: 基于文字匹配，得知当前处在副本中')
            return True
        else:
            return False

    def __is_finish(self):
        """任务是否完成"""
        if self.curr_execute_num >= self.execute_num:
            logger.info(f'日常任务-龙: 当前执行次数达到{self.curr_execute_num},退出任务！')
            return True
        if self.curr_execute_round_num >= self.execute_round_num:
            logger.info(f'日常任务-龙: 当前执行轮数达到{self.curr_execute_round_num},退出任务！')
            return True

    def __status_timeout_decide(self):
        """
        状态超时判断
        :return:
        """
        if self.status not in (0,):
            return True
        time_total = time.time()-self.status_tag_time
        if time_total>self.timeout:
            self.status = 1
        return True

def run_exe(serial,devices):
    app = TaskLongRun(devices, serial, 1, 1,dungeon_min_time=180,execute_num=45)
    app.run()

if __name__ == "__main__":

    from qianv_tool.module.devices.devices import Devices

    multi_process = []
    devices = Devices()
    devices_info = devices.devices_info

    #
    for serial in devices_info:
        if serial=='emulator-5554':
            run_exe(serial,devices)

    # for serial in devices_info :
    #     print(devices_info[serial])
    #     # process = threading.Thread(target=run_exe, args=(serial,))
    #     process = multiprocessing.Process(target=run_exe, args=(serial,devices,))
    #     multi_process.append(process)
    #     process.start()
    # # join 方法可以让主线程等待所有子线程执行完毕后再结束。
    # for process in multi_process:
    #     process.join()