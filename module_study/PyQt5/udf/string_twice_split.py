#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# 程序名称:    string_twice_split
# 功能描述:    执行两次split后去制定的值，然后用逗号切换拼接成一条记录
# 例子：
#    数据：a,1,zzz;b,2,vvv
#    udf: string_twice_split(str,';',',',1)
#    输出：1,2
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

class StringTwiceSplit(BaseUDF):
    """
    继承BaseUDF类，在init中初始化
    """

    def __init__(self):
        BaseUDF.__init__(self)

    def eval(self, data, regex1, regex2, index):
        """
        实现eval方法，方法的输入是一行数据，输出是处理后的数据
        """
        result = []
        if data==None or len(data)==0:
            return ""
        for outer_elemnet in data.split(regex1):
            inside = outer_elemnet.split(regex2)
            if len(inside)>index:
                result.append(inside[index])
        return ','.join(result)