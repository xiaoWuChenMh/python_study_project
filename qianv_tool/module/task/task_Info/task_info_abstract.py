#!/usr/bin/env python
# -*- coding: utf-8 -*-

class TaskInfo:
    # 任务名称，不同任务之间唯一的识别标识
    __task_name = ""

    # 任务状态,默认是关闭状态，True是启动状态
    __task_state = False

    def __init__(self,task_name):
       self.set_task_name(task_name)

    def get_task_name(self):
        return self.__task_name

    def set_task_name( self ,task_name ):
        self.__task_name = task_name

    def close_task_state( self ):
        """
        关闭任务
        :return:
        """
        self.__task_state = False

    def open_tasks_tate( self ):
        """
        启动任务
        :return:
        """
        self.__task_state = True

    def get_task_state( self ):
        """
         获取任务状态
        :return:
        """
        return self.__task_state