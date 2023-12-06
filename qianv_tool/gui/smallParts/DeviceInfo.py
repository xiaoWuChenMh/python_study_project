#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################################################################
#  设备信息展示框
###########################################################################################################################
from PyQt5.QtWidgets import QWidget,QLabel,QGridLayout


class DeviceInfo(QWidget):


    def __init__(self,deInfo):
        super().__init__()
        # 设备其他详情信息
        layout = QGridLayout()
        layout.addWidget(QLabel(" 应用信息: "), 0, 0)
        layout.addWidget(QLabel("应用信息: %s" % (deInfo['app'])), 0, 1)
        layout.addWidget(QLabel(" 屏幕尺寸: "), 1, 0)
        layout.addWidget(QLabel("应用信息: %s" % (deInfo['size'])), 1, 1)

        self.setLayout(layout)
