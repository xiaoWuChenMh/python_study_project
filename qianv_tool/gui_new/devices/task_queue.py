#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qianv_tool.gui_new.devices.devices_info import DevidesInfo

class TaskQueue:

    task_param = {}

    def __init__(self):
       self.devices_init(DevidesInfo().get_info())

    def devices_init(self,devices):
        for device in devices:
            self.task_param[device]={}

    def param_collecor(self,device,task,key,value):
        """
        参数采集器，用于采集各个页面中的参数
        :param device:设备信息
        :param task:任务
        :param key:
        :param value:
        :return:
        """
        device_task = self.task_param[device]
        task
        pass