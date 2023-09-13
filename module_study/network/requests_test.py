#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################################################################
#                                             requests 模块
# 介绍： requests 模块是可以模仿浏览器发送请求获取响应 requests 模块在python2,与python3中通用 requests模块能够自动帮助我们解压网页内容。
# 安装： 通用（pip install requests），只在python3中安装（pip3 install requests）
###########################################################################################################################


import requests

# url字典库
url = 'http://www.baidu.com'

## =========================== 常用函数使用说明  ==========================

# response = requests.get(url)
# print("获取响应的 html 内容:"+response.text)
# print("获取响应的 html 内容(bytes 类型),通过decode编码为字符串:"+response.content.decode('utf-8'))
# print("获取响应的 状态码:"+str(response.status_code))
# print("获取请求头:"+str(response.request.headers))
# print("获取响应头:"+str(response.headers))
# print("获取响应的  RequestsCookieJar 对象:"+str(response.cookies))



## 自定义请求头

## 发送 GET 请求

## 发送 POST 请求


## 使用代理服务器


## 发送请求携带 Cookies

## 常用异常处理

## =========================== 下载图片地址 ==========================

# url = "https://img2.baidu.com/it/u=917382917,4109985544&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=500"
# # 发送请求获取响应
# response = requests.get(url)
# # 保存图片,以二进制写入模式('wb')打开一个名为image.png的文件，with语句是一种上下文管理器，它可以确保在代码块执行完毕后正确关闭文件，无论是否发生异常。
# with open('image.jpeg','wb') as f:
#   f.write(response.content)
