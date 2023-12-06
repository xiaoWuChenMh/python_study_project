#!/usr/bin/env python
# -*- coding: utf-8 -*-
#################################################################
#  运行时监控任务执行情况
#################################################################

import customtkinter as ctk
from qianv_tool.gui_new.devices.devices_info import DevidesInfo
from qianv_tool.gui_new.devices.task_queue import TaskQueue


class RunMonitorFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, image):
        super().__init__(master, corner_radius=0,fg_color="transparent")
        self.grid_rowconfigure((0,1,2), weight=1)

        execute_title = ctk.CTkLabel(self, text="执行中的任务",compound="left",font=ctk.CTkFont(size=13, weight="bold"))
        execute_title.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

        wait_title = ctk.CTkLabel(self, text="待执行的任务",compound="left",font=ctk.CTkFont(size=13, weight="bold"))
        wait_title.grid(row=1, column=0, padx=10, pady=20, sticky="nsew")

        complete_title = ctk.CTkLabel(self, text="执行完的任务",compound="left",font=ctk.CTkFont(size=13, weight="bold"))
        complete_title.grid(row=2, column=0, padx=10, pady=20, sticky="nsew")

    def task_queue(self):
        pass