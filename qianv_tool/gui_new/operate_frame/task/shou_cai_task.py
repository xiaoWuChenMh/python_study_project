#!/usr/bin/env python
# -*- coding: utf-8 -*-
#################################################################
#  家园-收菜-任务
#################################################################

import customtkinter as ctk
from qianv_tool.gui_new.devices.devices_info import DevidesInfo
from qianv_tool.gui_new.devices.task_queue import TaskQueue


class ShouCaiTask(ctk.CTkScrollableFrame):

    def __init__(self, master,image):
        super().__init__(master,corner_radius=0)
        self.grid_columnconfigure(0, weight=1)

        task_title = ctk.CTkLabel(self, text="待完成")
        task_title.grid(row=0, column=0, padx=10, pady=(20, 0), sticky="nsew")

