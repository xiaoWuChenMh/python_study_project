#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# 程序名称:    concat_ws_set.py
# 功能描述:    将列col1的字段连接为一行用逗号练成一列并去重，如何列中是用逗号分隔的字符串也会将其split切换后在合并去重，参数col1是需要合并的列名为必选参数
# 数据源表:
# 目标表名:
# 创建人名:    v_hhuima
# 创建日期:     2023/11/24
# 修改人名:
# 修改日期:
# 修改原因:
# 版本说明:    v1.0
# 公司名称:    tencent
"""

## UDAF函数需要配合group by使用，输入多行数据，输出一行处理后的数据，例如求和平均值函数：
from base_udf import BaseUDAF


class ConcatSetSplit(BaseUDAF):
    def __init__(self):
        self.buffer = []

    def initialize(self):
        '''
        创建聚合buffer
        :return:buffer
        '''
        buffer = ['']
        return buffer

    def update(self, buffer, data):
        '''
        处理每行数据
        :return:buffer
        '''
        if data!=None and len(data) > 0:
            elemnet = data[0]
            collect_set = set('')
            collect_set.update(buffer[0].split(','))
            collect_set.update(elemnet.split(','))
            buffer[0] = ','.join(x for x in collect_set if x)
        return buffer

    def merge(self):
        pass

    def eval(self, buffer):
        '''
        计算并求均值
        :return:average
        '''
        return buffer[0]
