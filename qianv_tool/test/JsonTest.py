#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################################################################
#  json内容操作测试
###########################################################################################################################

import json
import os
from qianv_tool.test.readFileTest import ReadFileTest


class JsonTest :
    def __init__(self):
        print("json内容操作测试")

    def traverse_nested_dict(self, nested_dict ):
        for key, value in nested_dict.items():
            if isinstance(value, dict):
                self.traverse_nested_dict(value)  # 递归遍历子字典
            else:
                print(f"Key: {key}, Value: {value}")  # 处理最内层的键值对

    def menuBuild( self,data):
        for key, array in data.items():
            for oneItem in array:
                print("创建一级目录: %s" % (oneItem['item_name']))
                if 'two_item' in oneItem:
                    for twoItem in oneItem['two_item']:
                        print("     创建二级目录: %s" % (twoItem['item_name']))

    # 循环测试
    def circulateTest(self):
        # 读取json文件
        readFileTest = ReadFileTest()
        jsonData = readFileTest.readJson("../config/menu.json")
        # 循环遍历内容
        self.traverse_nested_dict(jsonData)

    # menu测试
    def menuBuildTest(self):
        # 读取json文件
        readFileTest = ReadFileTest()
        jsonData = readFileTest.readJson("../config/menu.json")
        # 循环遍历内容
        self.menuBuild(jsonData)

    @staticmethod
    def main():
        """
        在这里编写你的主要逻辑
        """
        JsonTest().menuBuildTest()

if __name__ == "__main__":
    JsonTest.main()

