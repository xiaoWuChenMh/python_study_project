#!/usr/bin/env python
# -*- coding: utf-8 -*-
#################################################################
#  战龙任务
#################################################################

import customtkinter as ctk


class BangHuaTask(ctk.CTkScrollableFrame):

    def __init__(self, master,image,devices):
        super().__init__(master,corner_radius=0)
        self.grid_columnconfigure(0, weight=1)

        task_title = ctk.CTkLabel(self, text="待完成")
        task_title.grid(row=0, column=0, padx=10, pady=(20, 0), sticky="nsew")
