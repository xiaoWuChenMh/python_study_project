#!/usr/bin/env python
# -*- coding: utf-8 -*-
#################################################################
#  师门任务
#    布局： 第一层[列：1；行：2]，第二层(0,1)[列：1；行：动态]
#################################################################

import customtkinter as ctk
from qianv_tool.gui_new.devices.devices_info import DevidesInfo
from qianv_tool.gui_new.devices.task_queue import TaskQueue


class ShiMenTask(ctk.CTkScrollableFrame):

    def __init__(self, master,image):
        super().__init__(master,corner_radius=0)
        self.grid_columnconfigure(0, weight=1)

        # 获取设备信息
        self.devices = DevidesInfo().get_info()

        # 操作区域
        for i, device in enumerate(self.devices):
            submitFrom =self.createSubmitForm(self,device)
            submitFrom.grid(row=i, column=0, sticky="nsew")


    def createSubmitForm(self,operate,device):
        """
        基于设备动态的创建提交表单
        :param operate:
        :param device:
        :return:
        """

        # create Frame
        submitFrom = ctk.CTkFrame(operate, corner_radius=0, fg_color="transparent")
        submitFrom.grid_columnconfigure((0, 1), weight=1)


        # 设备名称
        device_name = '设备名称：%s' % (device['name'])
        task_title = ctk.CTkLabel(submitFrom, text=device_name)
        task_title.grid(row=0, column=0, padx=10, pady=(20,0), sticky="nsew")
        # 是否开启
        switch_var = ctk.StringVar(value="off")
        switch = ctk.CTkSwitch(submitFrom, text="启动", variable=switch_var, onvalue="on", offvalue="off",
                                  command = lambda t=switch_var,d=device: self.open_task(t,d)
                              )
        switch.grid(row=0, column=1, padx=20, pady=(20,0), sticky="nsew")

        # 提交装备颜色
        equip_color_title = ctk.CTkLabel(submitFrom, text='提交装备颜色')
        equip_color_title.grid(row=1, column=0, padx=10, pady=(5,0), sticky="nsew")

        equip_color = ctk.CTkComboBox(submitFrom, values=["蓝色及以下","不限制"],command=self.equip_color_callback)
        equip_color.grid(row=1, column=1, padx=20, pady=(5, 0), sticky="nsew")
        device['equip_color'] = equip_color

        # 提交装备孔数
        equip_hole_title = ctk.CTkLabel(submitFrom, text='提交装备孔数')
        equip_hole_title.grid(row=2, column=0, padx=10, pady=(5,0), sticky="nsew")

        equip_hole = ctk.CTkComboBox(submitFrom, values=["2孔及以下", "3孔及以下"],command=self.equip_hole_callback)
        equip_hole.grid(row=2, column=1, padx=20, pady=(5, 10), sticky="nsew")
        device['equip_hole'] = equip_hole
        return submitFrom


    def open_task(self,switch_var,device):
        """
        开启任务
        :param switch_var:
        :return:
        """
        print("switch toggled, current value:", switch_var.get())
        if switch_var.get() == "on":
            print("设备名称:", device['name'])
            print("提交装备颜色:", device['equip_color'].get())
            print("提交装备孔数:", device['equip_hole'].get())


    def equip_color_callback(self,choice):
        print("提交装备颜色:", choice)

    def equip_hole_callback(self, choice):
        print("提交装备孔数:", choice)
