import uiautomator2 as u2
import numpy as np
import cv2

# 链接设备
a = u2.connect('emulator-5562')
print(a.info)
a.screenshot('image/师门_是否确认退出副本.jpg')
# for x in range(100):
#     a.screenshot(f'image/师门_进入后地点_{x}.jpg')



#
# devices = ['emulator-5554','emulator-5556','emulator-5558','emulator-5560''emulator-5562']
# for de in devices:
#    try:
#        a = u2.connect(de)
#        print(a.info)
#    except Exception as e :
#        print(e)
#
