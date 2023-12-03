#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################################################################
#  一条龙任务
###########################################################################################################################
from PyQt5.QtWidgets import QWidget,QLabel,QHBoxLayout,QVBoxLayout

class LongTask:

    def create( self ):
        # 创建一个容器
        option2_widget = QWidget()
        #将布局放入容器中
        option2_widget.setLayout(self.createLayout())
        return option2_widget

    def createLayout( self ):
        # 创建一个布局
        option2_layout = QVBoxLayout()
        option2_label = QLabel("一条龙...............t")
        # 将内容放入布局中
        option2_layout.addWidget(option2_label)
        return option2_layout