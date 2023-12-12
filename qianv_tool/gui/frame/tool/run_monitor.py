#!/usr/bin/env python
# -*- coding: utf-8 -*-
#################################################################
#  运行时监控任务执行情况
#################################################################

import customtkinter as ctk
from qianv_tool.module.devices.devices_info import DevidesInfo


class RunMonitorFrame(ctk.CTkScrollableFrame):

    def __init__(self, master, image):
        super().__init__(master, corner_radius=0,fg_color="transparent")
        self.grid_rowconfigure((0,1,2,3,4,5), weight=1)
        self.grid_columnconfigure(0, weight=1)
        # 获取设备信息
        self.devices = DevidesInfo().get_info()
        # 还需要一个执行和停止按钮

        execute_title = ctk.CTkLabel(self, text="执行中的任务",compound="left",font=ctk.CTkFont(size=13, weight="bold"))
        execute_title.grid(row=0, column=0, padx=10, pady=(10,0), sticky="nsew")
        execute_task = self.task_queue("")
        execute_task.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")

        wait_title = ctk.CTkLabel(self, text="待执行的任务",compound="left",font=ctk.CTkFont(size=13, weight="bold"))
        wait_title.grid(row=2, column=0, padx=10, pady=(10,0), sticky="nsew")
        wait_task = self.task_queue("")
        wait_task.grid(row=3, column=0, padx=10, pady=0, sticky="nsew")

        complete_title = ctk.CTkLabel(self, text="执行完的任务",compound="left",font=ctk.CTkFont(size=13, weight="bold"))
        complete_title.grid(row=4, column=0, padx=10, pady=(10,0), sticky="nsew")
        complete_task = self.task_queue("")
        complete_task.grid(row=5, column=0, padx=10, pady=(0,20), sticky="nsew")

    def task_queue(self,task_info):
        """
        任务队列
        :param task_info:
        :return:
        """
        submitFrom = ctk.CTkFrame(self, corner_radius=0)
        submitFrom.grid_columnconfigure(0, weight=1)
        for i, device in enumerate(self.devices):
            text = '%s : 师门，战龙' %(device['name'])
            info = ctk.CTkLabel(submitFrom, text=text, compound="left")
            info.grid(row=i, column=0, padx=10, pady=(5,0), sticky="nsew")
        return submitFrom