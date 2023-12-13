#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PIL import Image

class LoadImage:

    logo_image = None
    large_test_image = None
    image_icon_image = None
    home_image = None
    chat_image = None
    add_user_image = None
    bg_image = None

    def __init__(self,tk):
        # 图像地址
        current_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.dirname(current_dir)
        image_path = os.path.join(parent_dir, "assets/image")

        # 创建Image对象
        self.logo_image = tk.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = tk.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(300, 80))
        self.image_icon_image = tk.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = tk.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = tk.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = tk.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
