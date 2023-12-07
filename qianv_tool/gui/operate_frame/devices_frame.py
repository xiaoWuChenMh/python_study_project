#!/usr/bin/env python
# -*- coding: utf-8 -*-

import customtkinter as ctk

class DevicesFrame(ctk.CTkFrame):
    def __init__(self, master,image):
        super().__init__(master,corner_radius=0, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)

        # 文本说明
        self.home_frame_large_image_label = ctk.CTkLabel(self, text="", image=image.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)
        # 按钮1
        self.home_frame_button_1 = ctk.CTkButton(self, text="", image=image.image_icon_image)
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        # 按钮2
        self.home_frame_button_2 = ctk.CTkButton(self, text="CTkButton", image=image.image_icon_image,
                                                 compound="right")
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        # 按钮3
        self.home_frame_button_3 = ctk.CTkButton(self, text="CTkButton", image=image.image_icon_image,
                                                 compound="top")
        self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        # 按钮4
        self.home_frame_button_4 = ctk.CTkButton(self, text="CTkButton", image=image.image_icon_image,
                                                 compound="bottom", anchor="w")
        self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)
