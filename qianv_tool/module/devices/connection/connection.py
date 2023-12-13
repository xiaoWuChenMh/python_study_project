########################################################################################################################
#                                      连接管理器
#
# stop_uiautomator ： 停止设备上的uiautomator和uiautomatorTest服务
#
#  ConnectionAttr -> Connection(ConnectionAttr)  -->  Uiautomator2(Connection)  -->Screenshot(Adb, WSA, DroidCast, AScreenCap, Scrcpy)  --> .....Device-->  AzurLaneAutoScript
# 其中的config 是 AzurLaneConfig
#  发现设备，初始化atx环境、启动atx环境（先关闭u2、atx后在启动atx)，校验环境是否正常，
########################################################################################################################
import os
import adbutils
import uiautomator2 as u2
from adbutils import AdbClient, AdbDevice
from qianv_tool.module.logger import logger
from qianv_tool.module.devices.connection.uiautomator import Uiautomator

class Connection(Uiautomator):

    def __init__(self):
        super().__init__()

    def __atx_restart(self, serial):
       """
       重新启动指定设备下的 atxAgent 服务，首先关闭，然后启动 [需要先执行u2的停止任务]
       :param serial: 设备ID
       """
       logger.info('Restart ATX')
       atx_agent_path = '/data/local/tmp/atx-agent'
       self.adb_shell(['chmod', '775', atx_agent_path], serial)
       self.adb_shell([atx_agent_path, 'server', '--stop'], serial)
       # '--nouia'
       self.adb_shell([atx_agent_path, 'server', '-d', '--addr', '127.0.0.1:7912'], serial)

    def restart_device_service(self, serial):
        """
         重启设备服务(uiautomator、atxAgent)
        :param serial:
        :return:
        """
        self.uiautomator_stop(serial)
        self.__atx_restart(serial)





if __name__ == "__main__":
    connection = Connection()
    connection.stop_uiautomator('emulator-5554')
    connection.restart_atx('emulator-5554')