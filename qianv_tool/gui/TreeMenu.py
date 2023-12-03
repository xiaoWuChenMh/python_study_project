#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################################################################
#  右侧树形菜单
# 通过配置文件构建树形菜单,重要方法如下：
#   buildMenu ：构建符合pyQt5格式的菜单项目
#   indexItemMapping： 返回菜单和 堆叠页idex的映射关系
#  未来会加入的菜单项： 守财、福星、饰品、各个等级剧情（半自动）
###########################################################################################################################

import json
from PyQt5.QtWidgets import QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem,QFont


class TreeMenu(QTreeView):

    menu_path = '../config/menu.json'

    def __init__(self):
        super().__init__()
        self.read_config()
        self.model = QStandardItemModel()
        self.setModel(self.model)

        # 隐藏表头(这样就不会显示行号了）
        self.setHeaderHidden(True)
        # 构建菜单布局
        self.buildMenu()

        print("树形菜单初始化成功")


    def read_config( self ):
        """
         读取菜单配置文件
        :return: dict格式的配置信息
        """
        with open(self.menu_path, 'r',encoding='utf-8') as f:
            data = json.load(f)
        return data

    def indexItemMapping( self ):
        """
         返回菜单和 堆叠页idex的映射关系
         :return: dict映射关系
        """
        mapping = {}
        data = self.read_config()

        for key, array in data.items():
            for oneItem in array:
                # print("创建一级目录: %s" % (oneItem['item_name']))
                if 'index' in oneItem:
                    item_name = oneItem['item_name']
                    index = oneItem['index']
                    mapping[item_name] = index
                if 'two_item' in oneItem:
                    for twoItem in oneItem['two_item']:
                        if 'index' in twoItem:
                            item_name = twoItem['item_name']
                            index = twoItem['index']
                            mapping[item_name] = index
        return mapping

    def buildMenu( self ):
        """
         读取菜单配置信息并构建菜单
        """
        # 读取menu配置文件
        data = self.read_config()

        # 设置菜单项字体大小为20
        font = QFont()
        font.setPointSize(12)

        for key, array in data.items():
            for oneItem in array:
                # print("创建一级目录: %s" % (oneItem['item_name']))
                item_name = oneItem['item_name']
                one_item = QStandardItem(item_name)
                self.model.appendRow([one_item])
                one_item.setFont(font)
                if 'two_item' in oneItem:
                    for twoItem in oneItem['two_item']:
                        # print("     创建二级目录: %s" % (twoItem['item_name']))
                        two_item_name = twoItem['item_name']
                        two_item = QStandardItem(two_item_name)
                        one_item.appendRow([two_item])
                        two_item.setFont(font)
