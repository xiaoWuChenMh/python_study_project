########################################################################################################################
#                                      自定义的Uiautomator连接管理器
# adb_binary ：获取adb二进制可执行文件地址
# adb_client: 获取adb的客户端
# adb_device ： 与某个设备建立连接后的AdbDevice
# adb_shell : 执行给定的adb shell 命令，想要输入adb shell命令 需要先通过“adb -s serial shell“ [serial：设备id比如emulator-5554]。
#
########################################################################################################################

import logging
import uiautomator2 as u2
from qianv_tool.module.logger import logger

class Uiautomator:

    def __init__(self):
       pass


    def install_uiautomator2(self):
        """
        Init uiautomator2 and remove minicap.
        """
        logger.info('Install uiautomator2')
        init = u2.init.Initer(self.adb, loglevel=logging.DEBUG)
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
        """卸载minicap：它在某些模拟器上无法工作或会发送压缩图像。 """
        logger.info('Removing minicap')
        self.adb_shell(["rm", "/data/local/tmp/minicap"])
        self.adb_shell(["rm", "/data/local/tmp/minicap.so"])
