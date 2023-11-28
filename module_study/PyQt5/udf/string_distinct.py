#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# 程序名称:    string_distinct
# 数据源表:
# 目标表名:
# 创建人名:    v_hhuima
# 创建日期:    2023/11/24
# 修改人名:
# 修改日期:
# 修改原因:
# 版本说明:    v1.0
# 公司名称:    tencent
"""

from base_udf import BaseUDF

class StringDistinct(BaseUDF):
    """
    继承BaseUDF类，在init中初始化
    """

    def __init__(self):
        BaseUDF.__init__(self)

    def eval(self, data, regex):
        """
        实现eval方法，方法的输入是一行数据，输出是处理后的数据
        """
        result = set()
        if data==None or len(data)==0:
            return ""
        result.update(data.split(','))
        return ','.join(x for x in result if x)