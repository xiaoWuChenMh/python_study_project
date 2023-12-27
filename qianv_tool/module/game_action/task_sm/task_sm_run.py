
import time
import multiprocessing
from qianv_tool.module.logger import logger
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
        #状态标记时间
        self.status_tag_time = 0
        #特殊状态需要的超时判断时间（默认60秒）
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

    def run(self):
        """
        启动任务，会尝试3次
        """
        try_num = self.try_num
        while try_num>0:
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
        self.__click_npc_speak_text()
        self.match_action.close_active_window()
        if self.match_main.open_active_window():
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
            self.status = 4
            self.status_tag_time = time.time()
        else:
            self.status = 1

    def __execution(self):
        """
        执行师门逻辑
        :return:
        """
        while True:
            self.__use_prop()
            self.__player_store()
            self.__click_out_map()
            # ===== 必须这样排序，这是效果最好，且防止某个动作打开后续点击任务栏关闭了 start ！！！！！！ ============
            self.__click_npc_speak_text()
            self.__click_task_dialogue()
            self.__is_activate()
            self.__click_task_dialogue()
            self.__npc_store()
            self.__submit_equipment()
            self.__click_task_list()
            # ==== 必须这样排序，并放到最后 end ！！！！！！ ===============
            self.__status_timeout_decide()
            if self.match_sm.is_task_finish():
                logger.info(f'日常任务-师门（{self.serial}）: 任务完成，退出师门任务自动操作！')
                time.sleep(self.reply_wait)
                # 防止没有取消完成弹框，在判断一次
                self.match_sm.is_task_finish()
                break

    def __click_out_map( self ):
        """点击退出副本"""
        self.match_sm.out_map()
    def __is_activate( self ):
        """判断师门任务是否激活,因文字识别率低，导致会多次重走激活逻辑"""
        if  self.status == 1 and not self.match_sm.is_first_task_list_area_strict():
            if self.__activation():
                logger.info(f'日常任务-师门（{self.serial}）: 师门任务执行过程中丢失判断，重新激活任务成功，状态{self.status}')
            else:
                logger.info(f'日常任务-师门（{self.serial}）:  师门任务执行过程中丢失判断，重新激活任务失败，状态{self.status}')


    def __click_npc_speak_text(self):
        """点击底部npc的文案"""
        while self.status == 1 and self.match_frame.click_botton_npc_text_dialogue():
            logger.info(f'日常任务-师门（{self.serial}）: 点击npc对话的文字，状态{self.status}')

    def __use_prop(self):
        """使用道具"""
        if self.status == 1 and self.match_sm.use_prop():
            logger.info(f'日常任务-师门（{self.serial}）: 使用道具，状态{self.status}')
            time.sleep(self.use_prop_wait)

    def __click_task_list(self):
        """点击任务列表"""
        self.match_action.close_active_window()
        if self.status in (1, 3) and self.match_main.open_task_list():
            # if not self.match_action.action_button_click:
            logger.info(f'日常任务-师门（{self.serial}）: 点击任务栏，状态{self.status}')
            self.match_sm.click_first_task_list_area()
            time.sleep(self.reply_wait)

    def __npc_store(self):
        """npc商店购买商品"""
        if self.status in (1,3) and self.match_shopping.npc_store():
            logger.info(f'日常任务-师门（{self.serial}）: NPC商店，状态{self.status}')

    def __player_store(self):
        """玩家商店购买商品"""
        if self.status == 1 and self.match_shopping.is_fabao_search():
            time.sleep(self.reply_wait)
        if self.status == 1 and self.match_shopping.player_store():
            logger.info(f'日常任务-师门（{self.serial}）: 玩家商店，状态{self.status}')

    def __click_task_dialogue(self):
        """点击任务对话框"""
        if self.status in (1, 2, 3, 4) and self.match_frame.click_top_npc_dialogue():
            logger.info(f'日常任务-师门（{self.serial}）: 点击npc对话框，当前状态{self.status}')
            if self.status == 4:
                self.status = 1
            if self.status == 2:
                self.status = 3
                self.status_tag_time = time.time()
            logger.info(f'日常任务-师门（{self.serial}）: 点击npc对话框，执行状态判断后{self.status}')
            time.sleep(self.reply_wait)

    def __submit_equipment(self):
        """提交装备的相关操作"""
        if self.status == 1 and self.match_sm.is_submit_equipment():
            logger.info(f'日常任务-师门（{self.serial}）: 提交装备的相关操作，状态{self.status}')
            self.status = 2
            self.status_tag_time = time.time()
            time.sleep(self.reply_wait)
            self.match_sm.click_submit_equipment_buy_other()
            time.sleep(self.switch_map)
        if self.status == 3 and self.match_sm.submit_equipment_real():
            logger.info(f'日常任务-师门（{self.serial}）: 提交装备的相关操作，状态{self.status}')
            self.status = 1
        if self.status == 1 and self.match_sm.submit_equipment_confirm():
            logger.info(f'日常任务-师门（{self.serial}）: 提交装备的相关操作，状态{self.status}')
            pass


    def __status_timeout_decide(self):
        """
        状态超时判断
        :return:
        """
        if self.status not in (2,3,4):
            return True
        time_total = time.time()-self.status_tag_time
        if time_total>self.timeout:
            self.status = 1
            logger.info(f'日常任务-师门（{self.serial}）: 状态（{self.status}）超时变更！')
        return True


def run_exe(serial,devices):
    app = TaskSmRun(devices, serial, 1, 1)
    app.run()

if __name__ == "__main__":

    from qianv_tool.module.devices.devices import Devices

    multi_process = []
    devices = Devices()
    devices_info = devices.devices_info

    #
    # for serial in devices_info:
    #     if serial=='emulator-5556': # 5560
    #         run_exe(serial,devices)

    for serial in devices_info :
        print(devices_info[serial])
        # process = threading.Thread(target=run_exe, args=(serial,))
        process = multiprocessing.Process(target=run_exe, args=(serial,devices,))
        multi_process.append(process)
        process.start()
    # join 方法可以让主线程等待所有子线程执行完毕后再结束。
    for process in multi_process:
        process.join()