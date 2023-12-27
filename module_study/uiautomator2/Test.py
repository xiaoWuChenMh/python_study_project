import uiautomator2 as u2
import numpy as np
import cv2

# 链接设备
# a = u2.connect('emulator-5556')
# print(a.info)
# a.screenshot('image/跑商_兰若寺_钱在来1.jpg')


#
devices = ['emulator-5554','emulator-5556','emulator-5558','emulator-5560']
for de in devices:
   try:
       a = u2.connect(de)
       print(a.info)
   except Exception as e :
       print(e)

