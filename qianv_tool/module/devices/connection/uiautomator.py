########################################################################################################################
#                                    自定义的Uiautomator连接管理器（基于uiautomator2）
#
# u2_device： 通过uiautomator建立和设备的连接（u2.connect(设备ID)）。
# get_u2： 安全的获取uiautomator连接，即连接可复用
# install_uiautomator2 ：将守护程序（u2、atx等）安装到设备，等同于‘python -m uiautomator2 init’
# u2_adb_shell : u2下执行 adb shell 命令
# screenshot： 截图，并做一些前置操作（颜色、去噪）
# click_uiautomator2 ：根据给定的坐标执行点击行为
#
########################################################################################################################


import re
import cv2

import numpy as np
import logging
import threading
from typing import Dict
import uiautomator2 as u2
from qianv_tool.module.logger import logger
from qianv_tool.module.devices.connection.adb import Adb
from qianv_tool.module.devices.exception import ImageTruncated
from qianv_tool.module.devices.utils import (remove_shell_warning,image_size,image_show)


class Uiautomator(Adb):

    image_test = False

    # 创建一个锁对象
    lock = threading.Lock()

    # 缓存u2连接
    u2_devices : Dict[str, u2.Device] = {}

    def __init__(self, image_test = False):
        super().__init__()
        self.image_test = image_test

    def u2_device(self,serial) -> u2.Device:
        """
         通过uiautomator建立和设备的连接
        :param serial:
        :return:
        """
        if self.is_over_http(serial):
            # Using uiautomator2_http
            device = u2.connect(serial)
        else:
            # Normal uiautomator2
            if serial.startswith('emulator-') or serial.startswith('127.0.0.1:'):
                device = u2.connect_usb(serial)
            else:
                device = u2.connect(serial)

        # Stay alive
        device.set_new_command_timeout(604800)

        logger.attr('u2.Device', f'Device(atx_agent_url={device._get_atx_agent_url()})')
        self.u2_devices[serial] = device
        return device

    def get_u2(self,serial) ->u2.Device:
        """
         安全的获取uiautomator连接
        :param serial:
        :return:
        """
        if serial not in self.u2_devices:
            self.lock.acquire()
            self.u2_device(serial)
            self.lock.release()
        # 验证连接是否可用
        print(self.u2_devices[serial].info)
        # for _ in range(3):
        #     try:
        #
        #         break
        #     except Exception as e:
        #         print(e)
        #         self.lock.acquire()
        #         self.u2_device(serial)
        #         self.lock.release()

        return self.u2_devices[serial]




    def is_over_http(self,serial):
        """
          验证 设备ID是否是一个http地址
        :param serial:
        :return:
        """
        return bool(re.match(r"^https?://",serial))

    def install_uiautomator2(self,serial):
        """
        安装 uiautomator2、atx 并移除 minicap,同在对每个设备执行  'python -m uiautomator2 init' 命令
        """
        logger.info('Install uiautomator2')
        init = u2.init.Initer(self.adb_device(serial), loglevel=logging.DEBUG)
        # MuMu X has no ro.product.cpu.abi, pick abi from ro.product.cpu.abilist 【init.abi：设备的 CPU 架构】
        if init.abi not in ['x86_64', 'x86', 'arm64-v8a', 'armeabi-v7a', 'armeabi']:
            init.abi = init.abis[0]
        # uiautomator默认监控的就是7912，这是显示的在声明下
        init.set_atx_agent_addr('127.0.0.1:7912')
        try:
            init.install()
        except ConnectionError:
            u2.init.GITHUB_BASEURL = 'http://tool.appetizer.io/openatx'
            init.install()
        self.uninstall_minicap()

    def uninstall_minicap(self):
        """卸载minicap：它在某些模拟器上无法工作或会发送压缩图像。 """
        logger.info('Removing minicap')
        self.adb_shell(["rm", "/data/local/tmp/minicap"])
        self.adb_shell(["rm", "/data/local/tmp/minicap.so"])

    def u2_adb_shell(self, cmd, serial, stream=False, recvall=True, timeout=10, rstrip=True):
        """
        Equivalent to http://127.0.0.1:7912/shell?command={command}
        u2下执行 adb shell 命令

        Args:
            cmd (list, str):
            stream (bool): Return stream instead of string output (Default: False)
            recvall (bool): Receive all data when stream=True (Default: True)
            timeout (int): (Default: 10)
            rstrip (bool): Strip the last empty line (Default: True)

        Returns:
            str if stream=False
            bytes if stream=True
        """
        if not isinstance(cmd, str):
            cmd = list(map(str, cmd))

        if stream:
            result = self.get_u2(serial).shell(cmd, stream=stream, timeout=timeout)
            # Already received all, so `recvall` is ignored
            result = remove_shell_warning(result.content)
            # bytes
            return result
        else:
            result = self.get_u2(serial).shell(cmd, stream=stream, timeout=timeout).output
            if rstrip:
                result = result.rstrip()
            result = remove_shell_warning(result)
            # str
            return result

    def uiautomator_stop( self,serial ):
        """
        通过adb shell 停止设备上的uiautomator和uiautomatorTest服务
        :param serial:
        :return:
        """
        package_name = 'com.github.uiautomator'
        package_name_test = 'com.github.uiautomator.test'
        self.adb_shell(['am', 'force-stop', package_name],serial)
        self.adb_shell(['am', 'force-stop', package_name_test],serial)

    def atx_restart(self, serial):
        """
        重新启动指定设备下的 atxAgent 服务,也会启动uiautomator服务，但首先需要先关闭uiautomator服务。
        :param serial: 设备ID
        """
        logger.info('Restart ATX')
        atx_agent_path = '/data/local/tmp/atx-agent'
        self.adb_shell(['chmod', '775', atx_agent_path], serial)
        self.adb_shell([atx_agent_path, 'server', '--stop'], serial)
        # '--nouia'
        self.adb_shell([atx_agent_path, 'server', '-d', '--addr', '127.0.0.1:7912'], serial)

    def click_uiautomator2(self,serial, x, y):
        """
        点击功能
        """
        self.get_u2(serial).click(x, y)


    def swipe_uiautomator2( self,serial, sx, sy, ex, ey):
        """
        滑动
        起始坐标：sx, sy
        目标坐标： ex, ey
        """
        self.get_u2(serial).swipe(sx, sy, ex, ey)

    def screenshot(self,serial):
        """
         截图，并做一些前置操作（颜色、去噪）
        :param serial: 设备ID
        :return: 处理后的截图
        """

        device = self.get_u2(serial)

        # 调用设备的截图功能截图，并发送到当前赋值给image变量
        image = device.screenshot(format='raw')

        # 这行代码将输入的"image"数据读入一个类型为np.uint8的NumPy数组中。
        image = np.frombuffer(image, np.uint8)
        self.__image_check(image,'Empty image after reading from buffer')

        # 这里使用了OpenCV的imdecode函数来对图像数据进行解码(转换为图像格式)。标志cv2.IMREAD_COLOR表示应该以彩色方式加载图像
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        self.__image_check(image, 'Empty image after cv2.imdecode')

        # 这行代码使用OpenCV的cvtColor函数将图像的颜色空间从BGR转换为RGB。
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.__image_check(image, 'Empty image after cv2.cvtColor')

        # 可选：对图片去噪
        cv2.fastNlMeansDenoising(image, image, h=17, templateWindowSize=1, searchWindowSize=2)
        self.__image_check(image, 'Empty image after cv2.fastNlMeansDenoising')

        # 图片校验，非1280*720的会给出错误信息
        width, height = image_size(image)
        if width != 1280 or height != 720:
            logger.warning(f'screenshot image size: {width},{height}')

        return image


    def central_coordinate(self,serial):
        """
         获取屏幕中央点位
        :param serial:
        :return:
        """
        # 获取模拟器屏幕的尺寸
        screen_width, screen_height = self.get_u2(serial).window_size()
        # 计算中心点的坐标
        center_x = screen_width // 2
        center_y = screen_height // 2
        return (center_x,center_y)


    def __image_check(self,image,error_message):
        if image is None:
            raise ImageTruncated(error_message)
        else:
            image_show(image,self.image_test)

if __name__ == "__main__":
    connection = Uiautomator()
    connection.install_uiautomator2('emulator-5554')