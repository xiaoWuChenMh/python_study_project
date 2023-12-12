########################################################################################################################
#                                      连接管理器
#
#  ConnectionAttr -> Connection(ConnectionAttr)  -->  Uiautomator2(Connection)  -->Screenshot(Adb, WSA, DroidCast, AScreenCap, Scrcpy)  --> .....Device-->  AzurLaneAutoScript
# 其中的config 是 AzurLaneConfig
#  发现设备，初始化atx环境、启动atx环境（先关闭u2、atx后在启动atx)，校验环境是否正常，
########################################################################################################################
import os
import adbutils
import uiautomator2 as u2
from adbutils import AdbClient, AdbDevice
from qianv_tool.module.devices.adb import Adb

class Connection(Adb):


    def __init__(self):
        pass


    def stop_uiautomator( self,serial ):
        """
        通过adb shell 停止设备上的uiautomator和uiautomatorTest服务
        :param serial:
        :return:
        """
        package_name = 'com.github.uiautomator'
        package_name_test = 'com.github.uiautomator.test'
        self.adb_shell(['am', 'force-stop', package_name],serial)
        self.adb_shell(['am', 'force-stop', package_name_test],serial)



if __name__ == "__main__":
    connection = Connection()
    # print(connection.adb_binary())
    print(connection.adb_client())
    connection.Test()