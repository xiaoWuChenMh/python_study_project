#!/usr/bin/env python
# -*- coding: utf-8 -*-
#################################################################
#  一条龙任务
#    布局： 第一层[列：1；行：2]，第二层(0,1)[列：1；行：动态]
#################################################################

import customtkinter as ctk
from qianv_tool.module.devices.devices_info import DevidesInfo
import qianv_tool.config.ui_option_conf as OPTION


class LongTask(ctk.CTkScrollableFrame):

    def __init__(self, master,image,devices):
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

        # 任务执行总次数（row=1）: 参考用法：https://github.com/TomSchimansky/CustomTkinter/issues/2134
        execute_num_value = ctk.StringVar(value="45")
        execute_num_title = ctk.CTkLabel(submitFrom, text='任务执行总次数')
        execute_num_title.grid(row=1, column=0, padx=10, pady=(5,0), sticky="nsew")

        execute_num = ctk.CTkEntry(submitFrom,textvariable=execute_num_value)
        execute_num.grid(row=1, column=1, padx=20, pady=(5, 0), sticky="nsew")
        device['execute_num'] = execute_num
        execute_num_value.trace_add("write", lambda *args: self.execute_num_callback(device) )


        # 任务待领取位置（row=2）:
        position_title = ctk.CTkLabel(submitFrom, text='任务待领取位置')
        position_title.grid(row=2, column=0, padx=10, pady=(5,0), sticky="nsew")

        position = ctk.CTkComboBox(submitFrom, values=OPTION.TASK_POSITION,command=self.position_callback)
        position.grid(row=2, column=1, padx=20, pady=(5, 0), sticky="nsew")
        device['position'] = position


        # 操作反应等待（row=3）:
        reply_wait_value = ctk.StringVar(value="1")
        reply_wait_title = ctk.CTkLabel(submitFrom, text='操作反应等待(秒)')
        reply_wait_title.grid(row=3, column=0, padx=10, pady=(5,0), sticky="nsew")

        reply_wait = ctk.CTkEntry(submitFrom,textvariable=reply_wait_value)
        reply_wait.grid(row=3, column=1, padx=20, pady=(5, 0), sticky="nsew")
        device['reply_wait'] = reply_wait
        reply_wait_value.trace_add("write", lambda *args: self.reply_wait_callback(device) )

        # 切换地图等待(秒)（row=4）:
        switch_map_value = ctk.StringVar(value="5")
        switch_map_title = ctk.CTkLabel(submitFrom, text='切换地图等待(秒)')
        switch_map_title.grid(row=4, column=0, padx=10, pady=(5,0), sticky="nsew")

        switch_map = ctk.CTkEntry(submitFrom,textvariable=switch_map_value)
        switch_map.grid(row=4, column=1, padx=20, pady=(5, 0), sticky="nsew")
        device['switch_map'] = switch_map
        switch_map_value.trace_add("write", lambda *args: self.switch_map_callback(device) )


        # 副本挂机时间（row=5）:
        dungeon_min_time_value = ctk.StringVar(value="120")
        dungeon_min_time_title = ctk.CTkLabel(submitFrom, text='副本挂机时间(秒)')
        dungeon_min_time_title.grid(row=5, column=0, padx=10, pady=(5,0), sticky="nsew")

        dungeon_min_time = ctk.CTkEntry(submitFrom,textvariable=dungeon_min_time_value)
        dungeon_min_time.grid(row=5, column=1, padx=20, pady=(5, 0), sticky="nsew")
        device['dungeon_min_time'] = dungeon_min_time
        dungeon_min_time_value.trace_add("write", lambda *args: self.dungeon_min_time_callback(device) )

        return submitFrom


    def open_task(self,switch_var,device):
        """
        开启任务
        :param switch_var:
        :return:
        """
        # 启动：on; 关闭：off；
        print(f'任务启动开关状态：{switch_var.get()}')
        if switch_var.get() == "on":
            print("设备名称:", device['name'])
            print( self.submit_check(device))

    def submit_check( self,device ):
        result = {}
        execute_num = device['execute_num'].get()
        result['execute_num'] = 45 if execute_num == '' or int(execute_num) > 45 else int(execute_num)
        result['position'] = 0 if device['position'].get() == '' else int(device['position'].get())
        result['reply_wait'] = 1 if device['reply_wait'].get() == '' else int(device['reply_wait'].get())
        result['switch_map'] = 5 if device['switch_map'].get() == '' else int(device['switch_map'].get())
        result['dungeon_min_time'] = 120 if device['dungeon_min_time'].get() == '' else int(device['dungeon_min_time'].get())
        return  result


    def execute_num_callback(self,device):
        print("任务执行总次数:", device['execute_num'].get())
        # 判断是否开启，开启就更新device参数
        print(self.submit_check(device))
    def position_callback(self,choice):
        # 判断是否开启，开启就更新device参数
        print("任务待领取位置:", choice)
    def reply_wait_callback(self,device):
        # 判断是否开启，开启就更新device参数
        print("操作反应等待(秒):", device['reply_wait'].get())
    def switch_map_callback(self,device):
        # 判断是否开启，开启就更新device参数
        print("切换地图等待(秒):", device['switch_map'].get())
    def dungeon_min_time_callback(self,device):
        # 判断是否开启，开启就更新device参数
        print("副本挂机时间(秒):", device['dungeon_min_time'].get())


