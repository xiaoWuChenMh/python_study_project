#!/usr/bin/env python
# -*- coding: utf-8 -*-
#################################################################
#  帮会任务
#    布局：1  2  3
#################################################################

import customtkinter as ctk
from qianv_tool.gui_new.menu.navigation_frame import NavigationFrame


class BangHuiFrame(ctk.CTkFrame):
    def __init__(self, master,image):
        super().__init__(master,corner_radius=0, fg_color="transparent")

        # 1*3
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 布局row=0,column=1 操作空（CTkScrollableFrame）
        self.second_frame = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")

        # 布局row=0,column=0 是二级菜单（CTkFrame）
        self.frames_menu_mapping =[
            {"name":"战龙","frame": self.second_frame,"button":""},
            {"name":"帮花","frame": self.third_frame,"button":""}
        ]
        self.navigation_title = {"text":"帮会任务"}
        self.navigation = NavigationFrame(self,self.frames_menu_mapping,self.navigation_title,2)
        self.navigation.grid(row=0, column=0, sticky="nsew")


