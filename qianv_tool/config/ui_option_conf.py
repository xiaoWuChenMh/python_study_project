#!/usr/bin/env python
# -*- coding: utf-8 -*-
#################################################################
#  ui选项的配置项目，比如：一条龙里的‘当前不是队长’这一选项的值
#################################################################

# 任务领取位置
TASK_POSITION  = ['0','1','2','3','4','5','6','7','8']

# 他人申请队长
APPLY_LEADER_OPTION = ["不允许", "允许"]

# 当前不是队长
IS_LEADER_TITLE_OPTION = ["跳过任务", "申请队长"]

# 装备颜色
EQUIP_COLOR = ["蓝色及以下","不限制"]

# 装备孔数
EQUIP_HOLE = ["蓝色及以下","不限制"]

def get_option_code(option,option_name):
    """
    根据给定的选项名获取对应编号
    :param option: 选项列表
    :param option_name: 选项名称
    :return:选项编号
    """
    for i, k in enumerate(option):
        if option_name == k:
            return i
        else:
            pass
    return None

def get_option_name(option,option_code):
    """
    根据给定的值，获取选项名
    :param option:选项列表
    :param option_code:选项编号
    :return: 选项名称
    """
    if len(option)>option_code:
        return option[option_code]
    else:
        return None
