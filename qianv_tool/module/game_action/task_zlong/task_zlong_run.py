
import time
import multiprocessing
from qianv_tool.module.logger import logger
from qianv_tool.module.game_action.task_zlong.match import Match as MatchZlong
from qianv_tool.module.game_action.mian_window.match import Match as MatchMain
from qianv_tool.module.game_action.pop_frame.match import Match as MatchFrame
from qianv_tool.module.game_action.shopping.match import Match as MatchShopping
from qianv_tool.module.game_action.action_window.match import Match as MatchAction


class TaskZlongRun:


    def __init__( self, devices, serial, position, reply_wait=2,switch_map=3,use_prop_wait=6):
        # 设备管理对象
        self.devices: Devices = devices
        # 设备ID
        self.serial = serial
        # 响应等待时间
        self.reply_wait = reply_wait
        # 过图等待时间
        self.switch_map = switch_map
        # 使用道具后的等待时间
        self.use_prop_wait = use_prop_wait
        # 任务所处位置（0-自动查找，1-第一位，2-第二位，...）
        self.position = position

        # 任务启动失败重试次数
        self.try_num = 3
        # 匹配动作行为的对象
        self.match_zhan_long = MatchZlong(devices,serial,reply_wait)
        self.match_shopping = MatchShopping(devices,serial,reply_wait)
        self.match_main = MatchMain(devices,serial,reply_wait)
        self.match_action = MatchAction(devices,serial,reply_wait)
        self.match_frame = MatchFrame(devices,serial,reply_wait)
        # 让人物移动一下
        # devices.swipe(serial, 600, 300, 700, 500)

    def run(self):
        """
        启动任务，会尝试3次
        """
        try_num = self.try_num
        while try_num>0:
            if self.__activation():
                logger.info(f'日常任务-战龙（{self.serial}）:激活成功,开始执行任务逻辑')
                self.__execution()
                break
            else:
                try_num  = try_num-1
                logger.info(f'日常任务-战龙（{self.serial}）:激活失败,剩余尝试次数{try_num}。')
        if try_num==0:
            logger.info(f'日常任务-战龙（{self.serial}）：激活失败且超过尝试次数，退出任务！')
            return False
        else:
            return True


    def __activation(self):
        """
        激活任务
        """
        self.match_action.close_active_window()
        if self.match_zhan_long.click_first_task_list_area_strict():
            return True
        if self.match_main.open_active_window():
            time.sleep(self.reply_wait)
            if self.position==0 and self.match_action.find_task_receive('战龙'):
                self.position = self.match_action.buttonMatch.grid_word_index
                return True
            if self.position>0:
                return self.match_action.find_task_position(self.position,'战龙')
            else:
                return False
        else:
            return False


    def __execution(self):
        """
        执行师门逻辑
        :return:
        """
        while True:
            self.__use_prop()
            self.__click_task_dialogue()
            self.__click_npc_speak_text()
            self.__task_failure()
            self.__final_enemy()
            self.__final_escape()
            self.__try_receive_task()
            # 激活任务
            if self.match_zhan_long.is_task_finish_click():
                logger.info(f'日常任务-战龙（{self.serial}）: 任务完成，退出自动操作！')
                break

    def __try_receive_task( self ):
        self.match_action.close_active_window()
        if self.match_zhan_long.click_first_task_list_area_strict():
            return True
        if self.match_main.open_active_window():
            time.sleep(self.reply_wait)
            if self.position==0 and self.match_action.find_task_receive('战龙'):
                self.match_zhan_long.click_first_task_list_area_strict()
                return True
            if self.position>0:
                self.match_action.find_task_position(self.position, '战龙')
                self.match_zhan_long.click_first_task_list_area_strict()
                return
            else:
                return False
        else:
            return False

    def __use_prop(self):
        """使用道具"""
        if self.match_zhan_long.is_task_kill_click():
            logger.info(f'日常任务-战龙（{self.serial}）: 触发刺杀任务！')
            start_time = time.time()
            time_total = 0
            # 未检测到任务栏有完成标识 且 执行时间未超过2分钟，就一直释放技能
            while not self.match_zhan_long.is_curr_task_finish() and time_total<120:
                for index in (1,2,3,4,5):
                    self.match_main.use_skill(index)
                    time.sleep(0.5)
                self.match_main.press_drug_quick()
                time_total = time.time() - start_time
        if self.match_zhan_long.use_prop():
            logger.info(f'日常任务-战龙（{self.serial}）: 使用道具！')
            time.sleep(self.reply_wait)

    def __click_task_dialogue(self):
        """点击任务对话框"""
        if self.match_frame.click_top_npc_dialogue():
            logger.info(f'日常任务-战龙（{self.serial}）: 点击npc对话框')
            time.sleep(self.reply_wait)

    def __click_npc_speak_text(self):
        """点击底部npc的文案"""
        while self.match_frame.click_botton_npc_text_dialogue():
            logger.info(f'日常任务-战龙（{self.serial}）: 点击npc对话的文字')
            time.sleep(0.5)

    def __task_failure( self ):
        """
        任务失败处理逻辑
        """
        if self.match_zhan_long.is_task_fail_click():
            logger.info(f'日常任务-战龙（{self.serial}）: 任务失败-放弃任务')
            self.match_zhan_long.give_up_task()
            logger.info(f'日常任务-战龙（{self.serial}）: 任务失败-回帮')
            self.match_zhan_long.come_bank()

    def __final_enemy( self ):
        """最终战龙-劲敌"""
        if self.match_zhan_long.is_last_deat_click():
            logger.info(f'日常任务-战龙（{self.serial}）: 最终战龙-劲敌')
            while self.match_zhan_long.is_out_map_tag():
                for index in (1, 2, 3, 4, 5):
                    self.match_main.use_skill(index)
                    time.sleep(0.5)
                self.match_main.press_drug_quick()

    def __final_escape( self ):
        """最终战龙-求生"""
        if self.match_zhan_long.is_last_run_click():
            logger.info(f'日常任务-战龙（{self.serial}）: 最终战龙-求生')
            time.sleep(self.switch_map)
            self.match_zhan_long.run_positions_exe()


def run_exe(serial,devices):
    app = TaskZlongRun(devices, serial, 5, 1)
    app.run()

if __name__ == "__main__":


    from qianv_tool.module.devices.devices import Devices

    multi_process = []
    devices = Devices()
    devices_info = devices.devices_info

    for serial in devices_info:
        if serial=='emulator-5554':
            run_exe(serial,devices)

    # for serial in devices_info :
    #     print(devices_info[serial])
    #     process = multiprocessing.Process(target=run_exe, args=(serial,devices,))
    #     multi_process.append(process)
    #     process.start()
    # # join 方法可以让主线程等待所有子线程执行完毕后再结束。
    # for process in multi_process:
    #     process.join()