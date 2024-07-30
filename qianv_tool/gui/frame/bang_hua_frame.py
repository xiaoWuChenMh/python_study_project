#!/usr/bin/env python
# -*- coding: utf-8 -*-
#################################################################
#  帮会任务
#    布局：1  2  3
#################################################################

import customtkinter as ctk
from qianv_tool.gui.menu.tab_view import TabView
from qianv_tool.gui.frame.task.zhan_long_task import ZhanLongTask
from qianv_tool.gui.frame.task.bang_hua_task import BangHuaTask

class BangHuaFrame(ctk.CTkFrame):
    def __init__(self, master,image,devices):
        super().__init__(master,corner_radius=0, fg_color="transparent")
        self.devices = devices
        # 居中配置
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # tab配置
        self.tabConfig =[
            {"name":" 战龙 ","tab": None},
            {"name":" 帮花 ","tab": None}
        ]

        tabVidew = TabView(self,self.tabConfig)
        tabVidew.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew")
        a = tabVidew.getTab(0)

        # 初始化各个tab页的内容
        self.zhan_long_task_frame = ZhanLongTask(tabVidew.getTab(0),image, self.devices)
        self.zhan_long_task_frame.grid(row=0, column=0,sticky="nsew")
        self.bang_hua_task_frame = BangHuaTask(tabVidew.getTab(1),image, self.devices)
        self.bang_hua_task_frame.grid(row=0, column=0,sticky="nsew")


