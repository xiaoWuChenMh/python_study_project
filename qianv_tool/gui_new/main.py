#!/usr/bin/env python
# -*- coding: utf-8 -*-

import customtkinter as ctk
import os
import tkinter as tk
from qianv_tool.gui_new.load_Image import LoadImage
from qianv_tool.gui_new.menu.navigation_frame import NavigationFrame
from qianv_tool.gui_new.operate_frame.devices_frame import DevicesFrame


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("测试程序")
        self.geometry("1200x450")

        # set grid layout 1x2 网格是1*2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 1、加载具有浅色和深色模式图像的图像
        image = LoadImage(ctk)

        # 2、create home frame 创建home框架
        self.devices_frame =DevicesFrame(self,image)
        self.second_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.for_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")


        # 3、初始化导航条
        self.frames_menu_mapping =[
            {"name":"设备","frame": self.devices_frame,"button_image":image.home_image,"button":""},
            {"name":"运行","frame": self.second_frame,"button_image":image.chat_image,"button":""},
            {"name":"常规任务","frame": self.third_frame,"button_image":image.add_user_image,"button":""},
            {"name":"bannghui任务","frame": self.for_frame,"button":""}
        ]
        self.navigation_title = {"text":"  Image Example","image":image.logo_image}
        self.navigation = NavigationFrame(self,self.frames_menu_mapping,self.navigation_title)
        self.navigation.grid(row=0, column=0, sticky="nsew")




if __name__ == "__main__":
    app = App()
    app.mainloop()