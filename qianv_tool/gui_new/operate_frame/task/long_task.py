#!/usr/bin/env python
# -*- coding: utf-8 -*-
#################################################################
#  一条龙任务
#    布局： 第一层[列：1；行：2]，第二层(0,1)[列：1；行：动态]
#################################################################

import customtkinter as ctk
from qianv_tool.gui_new.devices.devices_info import DevidesInfo
from qianv_tool.gui_new.devices.task_queue import TaskQueue


class LongTaskFrame(ctk.CTkScrollableFrame):

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

        # 执行次数:
        execute_num_value = ctk.StringVar(value="40")
        execute_num_title = ctk.CTkLabel(submitFrom, text='执行次数')
        execute_num_title.grid(row=1, column=0, padx=10, pady=(5,0), sticky="nsew")

        execute_num = ctk.CTkEntry(submitFrom,textvariable=execute_num_value)
        execute_num.grid(row=1, column=1, padx=20, pady=(5, 0), sticky="nsew")
        device['execute_num'] = execute_num
        execute_num_value.trace_add("write", lambda *args: self.execute_num_callback(device) )
        # 他人申请队长
        apply_leader_title = ctk.CTkLabel(submitFrom, text='他人申请队长')
        apply_leader_title.grid(row=2, column=0, padx=10, pady=(5,0), sticky="nsew")

        apply_leader = ctk.CTkComboBox(submitFrom, values=["不允许", "允许"],command=self.apply_leader_callback)
        apply_leader.grid(row=2, column=1, padx=20, pady=(5, 0), sticky="nsew")
        device['apply_leader'] = apply_leader

        # 当前不是队长
        is_leader_title = ctk.CTkLabel(submitFrom, text='当前不是队长')
        is_leader_title.grid(row=3, column=0, padx=10, pady=(5,0), sticky="nsew")

        is_leader = ctk.CTkComboBox(submitFrom, values=["跳过任务", "申请队长"],command=self.is_leader_callback)
        is_leader.grid(row=3, column=1, padx=20, pady=(5, 10), sticky="nsew")
        device['is_leader'] = is_leader
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
            # 不能大于40，大于40就修正为40，修改值： execute_num.configure(textvariable=ctk.StringVar(value="22"))
            print("执行次数:", device['execute_num'].get())
            print("他人申请队长:", device['apply_leader'].get())
            print("当前不是队长:", device['is_leader'].get())


    def apply_leader_callback(self,choice):
        print("他人申请队长:", choice)

    def is_leader_callback(self, choice):
        print("当前不是队长:", choice)

    def execute_num_callback(self,device):
        print("执行次数:", device['execute_num'].get())