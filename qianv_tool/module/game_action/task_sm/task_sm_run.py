
import time
import multiprocessing
from qianv_tool.module.logger import logger
from qianv_tool.module.game_action.util import (random_sleep,time_sleep)
from qianv_tool.module.game_action.task_sm.match import Match as MatchSm
from qianv_tool.module.game_action.mian_window.match import Match as MatchMain
from qianv_tool.module.game_action.pop_frame.match import Match as MatchFrame
from qianv_tool.module.game_action.shopping.match import Match as MatchShopping
from qianv_tool.module.game_action.action_window.match import Match as MatchAction


class TaskSmRun:


    def __init__( self, devices, serial, position, reply_wait=2,switch_map=3,use_prop_wait=5):
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
        self.match_shopping = MatchShopping(devices,serial,reply_wait)
        self.match_main = MatchMain(devices,serial,reply_wait)
        self.match_sm = MatchSm(devices,serial,reply_wait)
        self.match_action = MatchAction(devices,serial,reply_wait)
        self.match_frame = MatchFrame(devices,serial,reply_wait)
        # 让人物移动一下
        # devices.swipe(serial, 600, 300, 700, 500)

  # =================================================================================

    def run(self):
        """
        启动任务，会尝试3次
        """
        try_num = self.try_num
        while try_num>0:
            self.__clean_environment()
            if self.__activation():
                logger.info(f'日常任务-师门（{self.serial}）:激活成功,开始执行任务逻辑')
                self.__execution()
                break
            else:
                try_num  = try_num-1
                logger.info(f'日常任务-师门（{self.serial}）:激活失败,剩余尝试次数{try_num}。')
        if try_num==0:
            logger.info(f'日常任务-师门（{self.serial}）：激活失败且超过尝试次数，退出任务！')
            return False
        else:
            return True


    def __activation(self):
        """
        激活任务
        """
        if self.status in (0,10,11) and self.match_main.open_active_window():
            time.sleep(self.reply_wait)
            self.serial
            if self.position == 0 and self.match_action.find_task_receive('师门'):
                self.position = self.match_action.buttonMatch.grid_word_index
                self.__activation_status()
                return True
            if self.position > 0 and self.match_action.find_task_position(self.position, '师门'):
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
            self.status = 11

    def __execution(self):
        """
        执行师门逻辑: 不要轻易改动排序效果，且防止某个动作打开后续点击任务栏关闭了(比如npc对话框)
        :return:
        """
        while True:
            image = self.match_sm.get_screenshot()
            self.__status_timeout_decide()
            if self.__npc_dialog_bottom():
                continue
            if self.__npc_checkbox_top1(image):
                continue
            if self.__use_task_prop(image):
                continue
            if self.__player_store_search(image):
                continue
            if self.__player_store_buy(image):
                continue
            if self.__npc_store_buy(image):
                continue
            if self.__in_dungeon_into(image):
                continue
            if self.__submit_equipment_start(image):
                continue
            if self.__submit_equipment_end(image):
                continue
            if self.__is_task_finish(image):
                break
            # ---以下操作只能放到最后面且顺序不可颠倒，之上的操作顺序无所谓 - ------------------------
            self.__clean_environment()
            self.__is_activate()
            self.__click_task_list_status()

 # =========================================================== 任务行为 ==================================================================

    def __status_timeout_decide(self):
        """
        状态超时判断
        :return:
        """
        if self.status not in (10,20,21,22):
            return True
        time_total = time.time()-self.status_tag_time
        if time_total>self.timeout:
            self.status = 11
            logger.info(f'日常任务-师门（{self.serial}）: 状态（{self.status}）超时变更！')
        return True

    def __npc_dialog_bottom( self ):
        """
         npc对话框（底部）：满足状态要求就循环点击,每次完成中间首要睡眠一段时间
         return : true:匹配成功；False: 匹配失败
        """
        is_exe = False
        while self.status in (10, 11) and self.match_frame.click_botton_npc_text_dialogue():
            logger.info(f'日常任务-师门（{self.serial}）: 点击 npc对话框（底部），状态{self.status}')
            self.status = 11 if self.status == 10 else self.status
            random_sleep()
            is_exe = True
        return is_exe

    def __npc_checkbox_top1( self, image ):
        if self.status in (11, 20) and self.match_frame.click_top_npc_dialogue(image):
            logger.info(f'日常任务-师门（{self.serial}）: npc多选框_top1按钮，当前状态{self.status}')
            if self.status == 20:
                self.status = 21
                self.status_tag_time = time.time()
            time_sleep(self.use_prop_wait)
            return True
        else:
            return False

    def __use_task_prop( self, image ):
        if self.status == 11 and self.match_sm.use_prop(image):
            logger.info(f'日常任务-师门（{self.serial}）: 使用任务道具，状态{self.status}')
            time_sleep(self.use_prop_wait)
            self.__safe_click_task_list()
            return True
        else:
            return False

    def __player_store_search( self, image ):
        if self.status == 11 and self.match_shopping.is_fabao_search(image):
            logger.info(f'日常任务-师门（{self.serial}）: 玩家商店-搜索法宝，状态{self.status}')
            return True
        else:
            return False

    def __player_store_buy( self, image ):
        if self.status == 11 and self.match_shopping.player_store(image):
            logger.info(f'日常任务-师门（{self.serial}）: 玩家商店-购买物品，状态{self.status}')
            self.__safe_click_task_list()
            return True
        else:
            return False

    def __npc_store_buy( self, image ):
        if self.status in (11, 21) and self.match_shopping.npc_store(image):
            logger.info(f'日常任务-师门（{self.serial}）: NPC商店-购买物品，状态{self.status}')
            if self.status == 21:
                self.status = 22
                self.status_tag_time = time.time()
            self.__safe_click_task_list()
            return True
        else:
            return False

    def __in_dungeon_into( self, image ):
        """副本内操作"""
        if self.status == 11 and self.match_sm.is_out_map_tag(image):
            logger.info(f'日常任务-师门（{self.serial}）: 副本内：释放技能，状态{self.status}')
            for index in (1, 2, 3, 4, 5):
                self.match_main.use_skill(index)
                random_sleep()
            while self.match_sm.is_out_map_tag():
                for index in (1, 2, 3, 4, 5):
                    self.match_main.use_skill(index)
                    random_sleep()
            return True
        else:
            return False

    def __submit_equipment_start( self, image ):
        if self.status == 11 and self.match_sm.click_submit_equipment(image):
            logger.info(f'日常任务-师门（{self.serial}）: 提交装备-从npc商店购买物品，状态{self.status}')
            time_sleep(self.reply_wait)
            self.match_sm.click_submit_equipment_buy_other()
            self.status = 20
            self.status_tag_time = time.time()
            time.sleep(self.switch_map)
            return True
        else:
            return False

    def __submit_equipment_end( self, image ):
        if self.status == 22 and self.match_sm.submit_equipment_real(image):
            logger.info(f'日常任务-师门（{self.serial}）: 提交装备-上交物品，状态{self.status}')
            self.status = 11

    def __is_task_finish( self, image ):
        if self.match_sm.is_task_finish(image):
            logger.info(f'日常任务-师门（{self.serial}）: 任务完成，退出师门任务自动操作！')
            time.sleep(self.reply_wait)
            # 防止没有取消完成弹框，在判断一次
            image = self.match_sm.get_screenshot()
            self.__is_task_finish(image)
            return True
        else:
            return False

    def __clean_environment( self ):
        """清理环境"""
        if self.status in (0, 10, 11):
            # 取消：npc对话框（底部）
            self.__npc_dialog_bottom()
            image = self.match_sm.get_screenshot()
            # 关闭：师门进阶通知
            self.match_sm.click_advanced_notice(image)
            # 关闭：确认按钮：改为副本退出按钮的判断吧！！！！
            self.match_sm.click_notice_confirm(image)
            # 关闭：活动窗口
            self.match_action.close_active_window(image)
            # 关闭：购物窗口
            self.match_shopping.close_buy_windwo(image)
            # 关闭：地图
            self.match_main.close_map_page(image)



    def __is_activate( self):
        """判断师门任务是否激活,因文字识别率低，导致会多次重走激活逻辑"""
        if  self.status in (10,11) and not self.match_sm.is_first_task_list_area_strict():
            if self.__activation():
                logger.info(f'日常任务-师门（{self.serial}）: 师门任务执行过程中丢失判断，重新激活任务成功，状态{self.status}')
            else:
                logger.info(f'日常任务-师门（{self.serial}）:  师门任务执行过程中丢失判断，重新激活任务失败，状态{self.status}')


    def __click_task_list_status(self):
        """点击任务列表"""
        if self.status in (11, 22):
            self.__safe_click_task_list()

    def __safe_click_task_list( self ):
        if self.match_main.open_task_list():
            logger.info(f'日常任务-师门（{self.serial}）: 点击任务栏，状态{self.status}')
            self.match_sm.click_first_task_list_area()
            time.sleep(self.reply_wait)


def run_exe(serial,devices):
    app = TaskSmRun(devices, serial, 1, 2)
    app.run()

if __name__ == "__main__":

    from qianv_tool.module.devices.devices import Devices

    multi_process = []
    devices = Devices()
    devices_info = devices.devices_info

    # 指定某人执行任务
    for serial in devices_info:
        if serial=='emulator-5562': # 5560
            run_exe(serial,devices)

    # for serial in devices_info :
    #     print(devices_info[serial])
    #     try:
    #         process = multiprocessing.Process(target=run_exe, args=(serial,devices,))
    #         multi_process.append(process)
    #         process.start()
    #     except Exception as e:
    #         print(e)
    # # join 方法可以让主线程等待所有子线程执行完毕后再结束。
    # for process in multi_process:
    #     process.join()