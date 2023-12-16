#!/usr/bin/env python
# -*- coding: utf-8 -*-
#################################################################
#  家园任务
#    布局：1  2  3
#################################################################

import customtkinter as ctk
from qianv_tool.gui.menu.tab_view import TabView
from qianv_tool.gui.frame.task.shou_cai_task import ShouCaiTask

class JiaYunFrame(ctk.CTkFrame):
    def __init__(self, master,image):
        super().__init__(master,corner_radius=0, fg_color="transparent")
        # 居中配置
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # tab配置
        self.tabConfig =[
            {"name":" 收菜 ","tab": None},
        ]

        tabVidew = TabView(self,self.tabConfig)
        tabVidew.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew")
        a = tabVidew.getTab(0)

        # 初始化各个tab页的内容
        self.shou_cai_task_frame = ShouCaiTask(tabVidew.getTab(0),image,self.devices)
        self.shou_cai_task_frame.grid(row=0, column=0,sticky="nsew")