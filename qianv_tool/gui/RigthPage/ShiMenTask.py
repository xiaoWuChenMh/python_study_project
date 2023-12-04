#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################################################################
#  师门任务
###########################################################################################################################

from PyQt5.QtWidgets import QWidget,QLabel,QHBoxLayout,QVBoxLayout

class ShiMenTask(QWidget):

    def __init__(self):
        super().__init__()
        self.setLayout(self.layoutInit())

    def layoutInit(self):
        # 创建一个布局
        option2_layout = QVBoxLayout()
        option2_label = QLabel("师门...............t")
        # 将内容放入布局中
        option2_layout.addWidget(option2_label)
        return option2_layout