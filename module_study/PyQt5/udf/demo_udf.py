#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# 程序名称:    udf_demo
# 功能描述:    udf示例
# 数据源表:
# 目标表名:
# 创建人名:    byronhu
# 创建日期:    2021/11/12
# 修改人名:
# 修改日期:
# 修改原因:
# 版本说明:    v1.0
# 公司名称:    tencent
"""

## 举例一：获取字段长度udf_test_length函数的定义
from base_udf import BaseUDF


class LengthTest(BaseUDF):
    """
    继承BaseUDF类，在init中初始化
    """

    def __init__(self):
        BaseUDF.__init__(self)

    def eval(self, data):
        """
        实现eval方法，方法的输入是一行数据，输出是处理后的数据
        """
        return len(data)


## UDAF函数需要配合group by使用，输入多行数据，输出一行处理后的数据，例如求和平均值函数：
from base_udf import BaseUDAF


class AvgTest(BaseUDAF):
    def __init__(self):
        self.buffer = []

    def initialize(self):
        '''
        创建聚合buffer
        :return:buffer
        '''
        buffer = [0.0, 0]
        return buffer

    def update(self, buffer, data):
        '''
        处理每行数据
        :return:buffer
        '''
        buffer[0] += data[0]
        buffer[1] += 1
        return buffer

    def merge(self):
        pass

    def eval(self, buffer):
        '''
        计算并求均值
        :return:average
        '''
        if (buffer[1] != 0):
            return buffer[0] / buffer[1]
        else:
            return 0.0
