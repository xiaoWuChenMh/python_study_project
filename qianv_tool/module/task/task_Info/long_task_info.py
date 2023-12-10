#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qianv_tool.module.task.task_Info.task_info_abstract import TaskInfo
import qianv_tool.config.ui_option_conf as OPTION
from qianv_tool.config.exe_config  import ExecuteConfig as TaskTagConfig

class LongTaskInfo(TaskInfo):

    # 执行次数
    __execute_num = 40

    # 他人申请队长
    __apply_leader = 9

    # 当前不是队长
    __is_leader = 0

    def __init__(self):
        super().__init__(TaskTagConfig.TASK_TAG__LONG)

    def set_execute_num( self, execute_num ):
        """
        设置 执行次数
        :param execute_num: 执行次数
        """
        self.__execute_num = execute_num

    def get_execute_num( self ):
        """
        获取 执行次数
        """
        return self.__execute_num

    def set_apply_leader(self,option_name):
        """
        设置 他人申请队长的选项值
        :param option_name: 选项名称
        """
        self.__apply_leader = OPTION.get_option_code(OPTION.APPLY_LEADER_OPTION,option_name)

    def get_apply_leader(self):
        """
        获取 他人申请队长的选项值
        """
        return self.__apply_leader

    def set_is_leader( self, option_name ):
        """
        设置 当前不是队长
        :param option_name: 选项名称
        """
        self.__apply_leader = OPTION.get_option_code(OPTION.IS_LEADER_TITLE_OPTION,option_name)

    def get_is_leader( self ):
        """
        获取 当前不是队长
        """
        return self.__apply_leader


