#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qianv_tool.module.task.task_Info.task_info_abstract import TaskInfo
import qianv_tool.config.ui_option_conf as OPTION
import qianv_tool.config.constant as CONSTANT

class ShiMenTaskInfo(TaskInfo):

    # 提交装备颜色
    __equip_color = 9

    # 提交装备孔数
    __equip_hole = 0

    def __init__( self ):
        super().__init__(CONSTANT.LONG_TASK_NAME)

    def set_equip_color( self, option_name ):
        """
        设置 提交装备颜色
        :param option_name: 选项名称
        """
        self.__equip_color = OPTION.get_option_code(OPTION.EQUIP_COLOR, option_name)

    def get_equip_color( self ):
        """
        获取 提交装备颜色
        """
        return self.__equip_color

    def set_equip_hole( self, option_name ):
        """
        设置 提交装备孔数
        :param option_name: 选项名称
        """
        self.__equip_hole = OPTION.get_option_code(OPTION.EQUIP_HOLE, option_name)

    def get_equip_hole( self ):
        """
        获取 提交装备孔数
        """
        return self.__equip_hole


