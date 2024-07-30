
import time
import multiprocessing
from qianv_tool.module.logger import logger
from qianv_tool.module.game_action.util import (random_sleep,time_sleep)
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

        # 任务状态
        self.status = 0
        # 状态标记时间
        self.status_tag_time = 0
        # 特殊状态需要的超时判断时间（默认60秒）
        self.timeout = 60
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
            self.__clean_environment()
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
        激活任务前，执行了类似一条龙的清理任务比较好
        """
        # 取消挂机
        self.match_main.cancel_gua_ji()
        if self.status in (0, 10, 12) and self.match_main.open_active_window():
            time.sleep(self.reply_wait)
            if self.position==0 and self.match_action.find_task_receive('战龙'):
                self.position = self.match_action.buttonMatch.grid_word_index
                self.__activation_status()
                return True
            if self.position>0 and self.match_action.find_task_position(self.position,'战龙'):
                self.__activation_status()
                return True
            else:
                return False
        else:
            return False

    def __activation_status( self ):
        """修改激活状态"""
        if self.match_action.action_button_click:
            self.status = 10
            self.status_tag_time = time.time()
        else:
            self.status = 12
            self.match_zhan_long.click_first_task_list_area()

    def __execution(self):
        """
        执行师门逻辑
        :return:
        """
        while True:
            image = self.match_zhan_long.get_screenshot()
            self.__status_timeout_decide()
            if self.__npc_dialog_bottom():
                continue
            if self.__npc_checkbox_top1(image):
                continue
            if self.__task_kill(image):
                continue
            if self.__final_enemy(image):
                continue
            if self.__final_escape(image):
                continue
            if self.__use_prop(image):
                continue
            if self.__task_is_fail(image):
                continue
            if self.__give_up_task(image):
                continue
            if self.__come_bank(image):
                continue
            if self.__is_task_finish(image):
                break
            # ---以下操作只能放到最后面且顺序不可颠倒，之上的操作顺序无所谓 - ------------------------
            self.__clean_environment()
            self.__try_receive_task()


   # =========================================================== 任务行为 ==================================================================

    def __status_timeout_decide( self ):
        """
        状态超时判断
        :return:
        """
        if self.status not in (11, 20, 21, 22):
            return True
        time_total = time.time() - self.status_tag_time
        if time_total > self.timeout:
            self.status = 10
            logger.info(f'帮会任务-战龙（{self.serial}）: 状态（{self.status}）超时变更！')
        return True

    def __npc_checkbox_top1( self, image ):
        if self.status in (10, 12) and self.match_frame.click_top_npc_dialogue(image):
            logger.info(f'帮会任务-战龙（{self.serial}）: npc多选框_top1按钮，当前状态{self.status}')
            if self.status == 10:
                self.status = 11
                self.status_tag_time = time.time()
            time_sleep(self.reply_wait)
            return True
        else:
            return False

    def __npc_dialog_bottom( self ):
        """
         npc对话框（底部）：满足状态要求就循环点击,每次完成中间首要睡眠一段时间
         return : true:匹配成功；False: 匹配失败
        """
        is_exe = False
        while self.status in (0, 11, 12) and self.match_frame.click_botton_npc_text_dialogue():
            logger.info(f'帮会任务-战龙（{self.serial}）: 点击 npc对话框（底部），状态{self.status}')
            if self.status == 11:
                self.status = 12
            random_sleep()
            is_exe = True
        return is_exe

    def __task_kill( self, image ):
        if self.status == 12 and self.match_zhan_long.is_task_kill_click(image):
            logger.info(f'帮会任务-战龙（{self.serial}）: 触发刺杀任务！')
            time.sleep(self.use_prop_wait)
            start_time = time.time()
            time_total = 0
            try_num = 0
            # 执行时间未超过2分钟，就一直释放技能 (暂时没找到太好的办法判断是否完成刺杀任务，文字识别不成功) ,20秒后没有头像校验3次？
            while (time_total<20 or self.match_zhan_long.is_kill_arm()) and try_num<3:
                if time_total>20 and not self.match_zhan_long.is_kill_arm() :
                    try_num = try_num+1
                    continue
                for index in (1,2,3,4,5):
                    self.match_main.use_skill(index)
                    time.sleep(0.5)
                self.match_main.press_drug_quick()
                time_total = time.time() - start_time
                # 检查人物死亡，选择原地复活
            return True
        else :
            return False

    def __final_enemy( self ,image):
        """最终战龙-劲敌"""
        if self.status == 12 and self.match_zhan_long.is_last_deat_click(image):
            time.sleep(self.use_prop_wait)
            time.sleep(self.switch_map)
            start_time = time.time()
            time_total = 0
            logger.info(f'帮会任务-战龙（{self.serial}）: 最终战龙-劲敌')
            # 双重校验判断是否释放技能：有副本标识 or 未超过10秒
            while self.match_zhan_long.is_out_map_tag() or time_total<10:
                for index in (1, 2, 3, 4, 5):
                    self.match_main.use_skill(index)
                    time.sleep(0.5)
                self.match_main.press_drug_quick()
                time_total = time.time() - start_time
            time_sleep(self.switch_map)
            self.match_zhan_long.click_first_task_list_area()
            return True
        else :
            return False

    def __final_escape( self ,image):
        """最终战龙-求生"""
        if self.status == 12 and self.match_zhan_long.is_last_run_click(image):
            logger.info(f'帮会任务-战龙（{self.serial}）: 最终战龙-求生')
            time.sleep(self.use_prop_wait)
            time.sleep(self.switch_map)
            self.match_zhan_long.run_positions_exe()
            return True
        else :
            return False

    def __use_prop(self, image):
        if self.status == 12 and self.match_zhan_long.use_prop(image):
            logger.info(f'帮会任务-战龙（{self.serial}）: 使用道具！')
            time.sleep(self.use_prop_wait)
            return True
        else:
            return False

    def __task_is_fail( self, image ):
        if self.status == 12 and self.match_zhan_long.is_out_map_tag(image):
            time.sleep(self.reply_wait)
            return True
        if self.status == 12 and self.match_zhan_long.is_task_fail_click(image):
            logger.info(f'帮会任务-战龙（{self.serial}）: 任务失败-点击弹出失败弹框')
            self.status = 20
            self.status_tag_time = time.time()
            return True
        else:
            return False

    def __give_up_task( self, image ):
        if self.status == 20 and self.match_zhan_long.give_up_task(image):
            logger.info(f'帮会任务-战龙（{self.serial}）: 任务失败-放弃任务')
            self.status = 21
            self.status_tag_time = time.time()
            return True
        else:
            return False

    def __come_bank( self, image ):
        if self.status == 21 and self.match_zhan_long.come_bank():
            logger.info(f'帮会任务-战龙（{self.serial}）: 任务失败-返回帮会')
            self.status = 12
            return True
        else:
            return False

    def __is_task_finish( self, image ):
        if self.match_zhan_long.is_task_finish_click(image):
            logger.info(f'帮会任务-战龙（{self.serial}）: 任务完成，退出任务自动操作！')
            time.sleep(self.reply_wait)
            # 防止没有取消完成弹框，在判断一次
            image = self.match_sm.get_screenshot()
            self.__is_task_finish(image)
            return True
        else:
            return False


    def __clean_environment( self ):
        """清理环境"""
        if self.status in (0, 10, 11, 12):
            # 取消：npc对话框（底部）
            self.__npc_dialog_bottom()
            image = self.match_zhan_long.get_screenshot()
            # 关闭：活动窗口
            self.match_action.close_active_window(image)
            # 关闭：购物窗口
            self.match_shopping.close_buy_windwo(image)
            # 关闭：地图
            self.match_main.close_map_page(image)
            # 打开任务列表
            self.match_main.open_task_list()

    def __try_receive_task( self ):
        if self.status == 12 and self.match_zhan_long.click_first_task_list_area_strict():
            time_sleep(self.reply_wait)
            return True
        logger.info(f'帮会任务-战龙（{self.serial}）: 战龙任务执行过程中丢失判断，重新激活任务成功，状态{self.status}')
        self.__activation()



def run_exe(serial,devices):
    app = TaskZlongRun(devices, serial, 7, 1)
    app.run()

if __name__ == "__main__":


    from qianv_tool.module.devices.devices import Devices

    multi_process = []
    devices = Devices()
    devices_info = devices.devices_info
    #
    for serial in devices_info:
        if serial=='emulator-5558':
            run_exe(serial,devices)

    # for serial in devices_info :
    #     print(devices_info[serial])
    #     process = multiprocessing.Process(target=run_exe, args=(serial,devices,))
    #     multi_process.append(process)
    #     process.start()
    # # join 方法可以让主线程等待所有子线程执行完毕后再结束。
    # for process in multi_process:
    #     process.join()