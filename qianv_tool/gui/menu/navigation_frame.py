#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################################################################
#             一级导航菜单
# 使用直接创建一个新对象，参入如下参数即可：
#     master ：父容器
#     frames_menu_mapping ：菜单和frame的对应关系
#          [{"name":"菜单项显示的名称","frame": frame对象,"button_image":图标-tk.CTkImage对象[可选],"button":菜单按钮对象}]
#     navigation_title : 导航标题[可选]
#          {"text":"导航标题","image":图标-tk.CTkImage对象[可选]}
########################################################################################################################

import customtkinter as ctk

class NavigationFrame(ctk.CTkFrame):
    def __init__(self, master,frames_menu_mapping,navigation_title=None,level=1):
        super().__init__(master,corner_radius=0)
        # 初始化参数
        self.mappings = frames_menu_mapping
        title = navigation_title
        self.row_num = -1

        # 居中设置
        self.grid_rowconfigure(len(self.mappings)+1, weight=1)

        #导航标题
        if not title ==None:
            title_font_size = 15 if level==1 else 13
            navigation_frame_label = ctk.CTkLabel(self, text=title['text'],
                                                        image=title['image'] if "image" in title else None,
                                                        compound="left",
                                                        font=ctk.CTkFont(size=title_font_size, weight="bold")
                                                  )
            navigation_frame_label.grid(row=self.get_index(), column=0, padx=10, pady=20)

        # 导航菜单
        for i, value in enumerate(self.mappings):
            button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text=value['name'],
                                   fg_color="transparent",
                                   text_color=("gray10", "gray90"),
                                   hover_color=("gray70", "gray30"),
                                   image= value['button_image'] if "button_image" in value else None,
                                   anchor="w",
                                   command=lambda t=value['name']: self.select_frame(t)
                                   )
            button.grid(row=self.get_index(), column=0, sticky="ew")
            value['button'] = button

        # 显示外观
        if level==1 :
            self.create_exterior_selecor()

        # 选中默认的frame
        self.select_frame(self.mappings[0]['name'])

    def select_frame(self, name):
        """
        切换所选按钮的按钮颜色 and 右侧frame的展示和隐藏
        :param name: 选中的菜单名，也代表按钮和fram的名字
        :return:
        """
        for mapping in self.mappings:
            if mapping['name']==name:
                mapping['button'].configure(fg_color=("gray75", "gray25"))
                mapping['frame'].grid(row=0, column=1, sticky="nsew")
                # print("当前选中的对象：%s" % (name))
            else:
                mapping['button'].configure(fg_color="transparent")
                mapping['frame'].grid_forget()

    def create_exterior_selecor(self):
        """
        创建外观选择器
        """
        appearance_mode_menu = ctk.CTkOptionMenu(self, values=["Light", "Dark", "System"],command=self.change_appearance_mode_event)
        appearance_mode_menu.grid(row=self.get_index(), column=0, padx=10, pady=20, sticky="s")


    def change_appearance_mode_event(self, new_appearance_mode):
        """
        切换外观主题
        :param new_appearance_mode: 选中的模式
        :return:
        """
        ctk.set_appearance_mode(new_appearance_mode)

    def get_index(self):
        self.row_num = self.row_num + 1
        return self.row_num