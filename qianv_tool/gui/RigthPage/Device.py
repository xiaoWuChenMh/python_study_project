#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################################################################
#  设备信息
###########################################################################################################################
from PyQt5.QtWidgets import QWidget,QLabel,QHBoxLayout,QVBoxLayout,QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from qianv_tool.gui.smallParts.DeviceInfo import DeviceInfo

class Device(QWidget):

    deviceInfo = [
        {
            "name":"DevieL00D5",
            "app":"ADZCDwwesasss",
            "size":"1270*568"
        },
        {
            "name":"DevieF00D5",
            "app":"ADZCD_PlayFram",
            "size": "1270*568"
        }
    ]

    def __init__(self):
        super().__init__()
        self.setLayout(self.layoutInit())




    def layoutInit(self):
        # 主窗口线性水平布局
        mainLayout = QHBoxLayout()
        # 左右垂直布局
        leftLayout = QVBoxLayout()
        rightLayout = QVBoxLayout()

        mainLayout.addLayout(leftLayout, 6)
        mainLayout.addLayout(rightLayout, 4)

        self.leftLayoutInit(leftLayout)
        return mainLayout
# =====================  左侧布局  ==================================

    def leftLayoutInit(self,leftLayout):
        self.title(leftLayout)
        self.devicesInfo(leftLayout)

    def title(self,leftLayout):
        """
        创建标题，并左对齐
        :param leftLayout: 父容器
        :return: None
        """
        oneLine = QVBoxLayout()
        font = QFont()
        font.setPointSize(8)
        title = QLabel("设备信息")
        title.setFont(font)
        title.setAlignment(Qt.AlignLeft)
        oneLine.addWidget(title)
        leftLayout.addLayout(oneLine,1)

    def devicesInfo(self,leftLayout):
        # 创建一个QScrollArea小部件
        scroll_area = QScrollArea(self)
        # 设置滚动区域的布局
        deviceInfoWidget = QWidget()
        devicesLayout = QVBoxLayout(deviceInfoWidget)
        scroll_area.setWidget(deviceInfoWidget)
        # 设备名称
        title = QLabel("设备名称: %s" )
        title.setAlignment(Qt.AlignLeft)
        devicesLayout.addWidget(title)

        # 设置垂直滚动条
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # 将滚动区域添加到布局中
        devicesArea = QVBoxLayout()
        devicesArea.addWidget(scroll_area)
        leftLayout.addLayout(devicesArea, 9)





