#!/usr/bin/env python
# -*- coding: utf-8 -*-
#################################################################
#  常规任务
#    布局：1  2  3
#################################################################

import customtkinter as ctk
from qianv_tool.gui.menu.navigation_frame import NavigationFrame
from qianv_tool.gui.operate_frame.tool.run_monitor import RunMonitorFrame


class RunFrame(ctk.CTkFrame):
    def __init__(self, master,image):
        super().__init__(master,corner_radius=0, fg_color="transparent")

        # 1*2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0,1,2), weight=1)

        # 布局row=0,column=0 操作空（CTkScrollableFrame）
        self.run_monitor_frame = RunMonitorFrame(self, image)
        self.run_monitor_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)


        # 布局row=0,column=2 日志（CTkScrollableFrame）
        self.log_frame = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.log_frame.grid(row=0, column=2, sticky="nsew")

