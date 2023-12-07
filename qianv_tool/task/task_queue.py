#!/usr/bin/env python
# -*- coding: utf-8 -*-

from queue import Queue
from qianv_tool.devices.devices_info import DevidesInfo


class TaskQueue:

    # 执行队列 Map<String,List<TaskInfo>>
    execute_queue = {}
    # 待执行队列 Map<String,List<TaskInfo>>
    wait_queue = {}
    # 已完成队列 Map<String,List<TaskInfo>>
    complete_queue = {}

    # 过了00点，如果执行队列和待执行队列都是空，那就清空已完成队列。

    def __init__(self):
       self.devices_init(DevidesInfo().get_info())

    def devices_init(self,devices):
        for device in devices:
            self.task_param[device]={}

    def set_execute_queue(self):
        """
        执行中的任务队列
        :return:
        """
        pass

    def get_execute_queue(self):
        """
        获取执行中的任务队列
        :return:
        """
        pass

    # 出队不能阻塞
    def set_wait_queue(self):
        """
        待执行的任务队列
        :return:
        """
        pass

    def get_wait_queue(self):
        """
        获取待执行的任务队列
        :return:
        """
        pass
    def set_complete_queue(self):
        """
        执行完毕的任务队列
        :return:
        """
        pass

    def get_complete_queue(self):
        """
        获取执行完毕的任务队列
        :return:
        """
        pass

    def param_collecor(self,device,task,key,value):
        """
        参数采集器，用于采集各个页面中的参数，然后将数据放入待执行的队列中
        有：修改；没有尾部添加
        :param device:设备信息
        :param task:任务
        :param key:
        :param value:
        :return:
        """
        device_task = self.task_param[device]
        task
        # 是否在已完成队列，是更新完
        # 是否在执行中队列，是就更新
        # 是否在待执行队列，是就更新
        # 都没有将其加入待执行队列的末尾！