#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################################################################
#  读取文件功能测试
# @staticmethod 代表静态方法
###########################################################################################################################

import json
import os

class ReadFileTest :
    def __init__(self):
        print("读取文件功能测试")

    def readJson( self ,file_path):
        # current_dir = os.path.dirname(__file__)  # 获取当前脚本的目录
        # file_path = os.path.join(current_dir, '..', 'config',fileName)  # 构建相对路径
        with open(file_path, 'r',encoding='utf-8') as f:
            data = json.load(f)
        print(data, type(data))
        return data

    @staticmethod
    def main():
        """
        在这里编写你的主要逻辑
        """
        readFileTest = ReadFileTest()
        readFileTest.readJson("../config/menu.json")
# 主要的程序逻辑被放置在main方法内部。if __name__ == "__main__":这行代码用来确保main方法只有在该脚本被直接运行时才会被调用，而不会在该脚本被作为模块导入时执行。
if __name__ == "__main__":
    ReadFileTest.main()


