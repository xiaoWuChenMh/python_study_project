#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################################################
#             tab页卡初始化
# 使用直接创建一个新对象，参入如下参数即可：
#     master ：父容器
#     tabConfig ：tab配置信息
#          [{"name":"名称","tab": tab对象}]
############################################################################

import customtkinter as ctk

class TabView(ctk.CTkTabview):

    def __init__(self, master,tabConfig, **kwargs):
        super().__init__(master, **kwargs)
        self.tabConfig = tabConfig

        for tab in self.tabConfig:
            name = tab['name']
            tab_object = self.add(name)
            tab_object.grid_columnconfigure(0, weight=1)
            tab_object.grid_rowconfigure(0, weight=1)
            tab['tab'] = tab_object

    def getTab(self,index):
        return self.tabConfig[index]['tab']
