
import time
from qianv_tool.module.logger import logger
from qianv_tool.module.game_action.task_sm.match import Match as MatchSm
from qianv_tool.module.game_action.task_long.match import Match as MatchLong
from qianv_tool.module.game_action.pop_frame.match import Match as MatchFrame
from qianv_tool.module.game_action.shopping.match import Match as MatchShopping
from qianv_tool.module.game_action.action_window.match import Match as MatchAction


class TaskSmRun:

    def __init__( self, devices, serial, reply_wait,position ):
        # 设备管理对象
        self.devices: Devices = devices
        # 设备ID
        self.serial = serial
        # 响应等待时间
        self.reply_wait = reply_wait
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
        self.match_long = MatchLong(devices,serial,reply_wait)
        self.match_sm = MatchSm(devices,serial,reply_wait)
        self.match_shopping = MatchShopping(devices,serial,reply_wait)
        self.match_action = MatchAction(devices,serial,reply_wait)
        self.match_frame = MatchFrame(devices,serial,reply_wait)

    def run(self):
        """
        启动任务，会尝试3次
        """
        try_num = self.try_num
        while try_num>0:
            if self.__activation():
                logger.info(f'日常任务-师门:激活成功,开始执行任务逻辑')
                self.__execution()
                break
            else:
                try_num  = try_num-1
                logger.info(f'日常任务-师门:激活失败,剩余尝试次数{try_num}。')

        if try_num==0:
            logger.info(f'日常任务-师门：激活失败且超过尝试次数，退出任务！')
            return False
        else:
            return True


    def __activation(self):
        """
        激活任务
        """
        if self.match_long.click_first_task_list_area_strict():
            self.status = 1
            return True
        if self.position==0 and self.match_action.find_task_receive('龙'):
            self.status = 0
            return True
        else:
            return self.match_action.find_task_position(self.position)

    def __execution(self):
        """
        执行师门逻辑
        :return:
        """
        activate_again_try = 0
        while True:
            if self.status in (0, 1) and self.match_frame.click_botton_npc_text_dialogue():
                logger.info(f'日常任务-师门:click npc speak tex;')
                if self.status == 0:
                    self.status == 1
                    logger.info(f'日常任务-师门:status change 1;')
            if self.status == 1 and self.match_sm.use_prop():
                logger.info(f'日常任务-师门:use prop;')
            if self.status == 1 and self.match_sm.click_first_task_list_area_strict():
                activate_again_try = 0
                logger.info(f'日常任务-师门:click task list;Clear activate threshold again')
            if self.status in (1, 2) and  self.match_frame.click_top_npc_dialogue():
                logger.info(f'日常任务-师门:click top npc dialogue;')
                if self.status == 2:
                    self.status = 3
                    self.status_tag_time = time.time()
                    logger.info(f'日常任务-师门:status change 3;')
            if self.status == 1 and self.match_shopping.npc_store():
                logger.info(f'日常任务-师门:npc store;')
            if self.status == 1 and self.match_shopping.is_fabao_search():
                logger.info(f'日常任务-师门:player store search;')
            if self.status == 1 and self.match_shopping.player_store():
                logger.info(f'日常任务-师门:player store;')
            # 提交装备 -略
            activate_again_try=self.__activate_again(activate_again_try)
            self.__status_timeout_decide()
            if self.match_sm.is_task_finish():
                logger.info(f'日常任务-师门: Execution completed, exit！')
                break

    def __activate_again(self,activate_again_try):
        if activate_again_try>=self.activate_threshold_again:
            if self.__activation():
                logger.info(f'日常任务-师门: Activate task again success！！！')
                return 0
            else:
                logger.info(f'日常任务-师门: Activate task again fail！！！')
                return activate_again_try
        if not self.match_sm.is_first_task_list_area_strict():
            logger.info(f'日常任务-师门: Reactivation task threshold increased！！')
            return activate_again_try+1




    def __status_timeout_decide(self):
        """
        状态超时判断
        :return:
        """
        if self.status not in (2,3):
            return True
        time_total = time.time()-self.status_tag_time
        if self.status == 2 and time_total>self.timeout:
            self.status = 1
        if self.status == 3 and time_total>self.timeout:
            self.status = 1
        return True




if __name__ == "__main__":

    from qianv_tool.module.devices.devices import Devices

    devices = Devices()
    devices_info = devices.devices_info
    for serial in devices_info:
        app = TaskSmRun(devices, serial, 1, 0)
        app.run()

