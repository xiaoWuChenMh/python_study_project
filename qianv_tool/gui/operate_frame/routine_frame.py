#!/usr/bin/env python
# -*- coding: utf-8 -*-
#################################################################
#  常规任务
#    布局：1  2  3
#################################################################

import customtkinter as ctk
from qianv_tool.gui.menu.tab_view import TabView
from qianv_tool.gui.operate_frame.task.long_task import LongTask
from qianv_tool.gui.operate_frame.task.shi_men_task import ShiMenTask

class RoutineFrame(ctk.CTkFrame):
    def __init__(self, master,image):
        super().__init__(master,corner_radius=0, fg_color="transparent")
        # 居中配置
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # tab配置
        self.tabConfig =[
            {"name":" 一条 ","tab": None},
            {"name":" 师门 ","tab": None}
        ]

        tabVidew = TabView(self,self.tabConfig)
        tabVidew.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew")
        a = tabVidew.getTab(0)

        # 初始化各个tab页的内容
        self.long_task_frame = LongTask(tabVidew.getTab(0),image)
        self.long_task_frame.grid(row=0, column=0,sticky="nsew")
        self.shi_men_task_frame = ShiMenTask(tabVidew.getTab(1),image)
        self.shi_men_task_frame.grid(row=0, column=0,sticky="nsew")

