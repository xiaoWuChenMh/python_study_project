#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qianv_tool.module.devices.devices_info import DevidesInfo

class TaskQueue:

    # 执行队列 Map<设备,List<TaskInfo>>>
    execute_queue = {}
    # 待执行队列 Map<设备,List<TaskInfo>>
    wait_queue = {}
    # 已完成队列 Map<设备,List<TaskInfo>>
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

    def param_collecor(self,device,task,task_info):
        """
        参数采集器，用于采集各个页面中的参数，然后将数据放入待执行的队列中
        有：修改；没有尾部添加
        :param device:设备信息
        :param task:任务
        :param task_info:任务信息
        :return:
        """
        device_task = self.task_param[device]

        if device in self.complete_queue:
            # 是否在已完成队列，是就更新
            task_list = self.complete_queue[device]
            self.__try_update_tasks(task_list,task_info)
            pass
        elif  device in self.execute_queue:
            # 是否在执行中队列，是就更新
            task_list = self.execute_queue[device]
            self.__try_update_tasks(task_list,task_info)
            pass
        elif  device in self.wait_queue:
            # 是否在待执行队列，是就更新
            task_list = self.wait_queue[device]
            self.__try_update_tasks(task_list,task_info)
            pass
        else:
            # 都没有将其加入待执行队列的末尾！
            self.wait_queue[device] = []
            self.wait_queue[device].append(task_info)
            pass
    def __try_update_tasks( self,task_list, task_info):
        """
         尝试更新任务信息
        :param task_list: 设备对应的任务队列
        :param task_info: 新的任务信息
        :return:
        """
        for i,task in enumerate(task_list):
            if task.get_task_name() == task_info.get_task_name():
                task_list[i] = task_info
