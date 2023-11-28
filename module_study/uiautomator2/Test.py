import uiautomator2 as u2

# 链接设备
a = u2.connect('emulator-5554')
d = u2.connect('emulator-5556')
# 输出设备信息
print(a.info)
print(d.info)

# 截图
a.screenshot('image/home.jpg')

