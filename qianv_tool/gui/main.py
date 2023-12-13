#!/usr/bin/env python
# -*- coding: utf-8 -*-

import customtkinter as ctk
import os
import tkinter as tk
from qianv_tool.gui.load_Image import LoadImage
from qianv_tool.gui.menu.navigation_frame import NavigationFrame
from qianv_tool.gui.frame.devices_frame import DevicesFrame
from qianv_tool.gui.frame.run_frame import RunFrame
from qianv_tool.gui.frame.routine_frame import RoutineFrame
from qianv_tool.gui.frame.bang_hua_frame import BangHuaFrame
from qianv_tool.gui.frame.jia_yuan_frame import JiaYunFrame


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("测试程序")
        self.geometry("900x600+900+600")

        # set grid layout 1x2 网格是1*2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 1、加载具有浅色和深色模式图像的图像
        image = LoadImage(ctk)

        # 2、create home frame 创建home框架
        self.devices_frame =DevicesFrame(self,image)
        self.run_frame =RunFrame(self,image)
        self.routine_frame = RoutineFrame(self,image)
        self.bang_hui_frame = BangHuaFrame(self,image)
        self.jia_yun_frame = JiaYunFrame(self,image)



        # 3、初始化导航条
        self.frames_menu_mapping = [
            {"name":"设备","frame": self.devices_frame,"button_image":image.home_image,"button":""},
            {"name":"运行","frame": self.run_frame,"button_image":image.chat_image,"button":""},
            {"name":"常规任务","frame": self.routine_frame,"button_image":image.add_user_image,"button":""},
            {"name":"帮会任务","frame": self.bang_hui_frame,"button_image":image.add_user_image,"button":""},
            {"name":"家园任务","frame": self.jia_yun_frame,"button_image":image.add_user_image,"button":""}
        ]
        self.navigation_title = {"text":"  导航菜单","image":image.logo_image}
        self.navigation = NavigationFrame(self,self.frames_menu_mapping,self.navigation_title)
        self.navigation.grid(row=0, column=0, sticky="nsew")



if __name__ == "__main__":
    app = App()
    app.mainloop()