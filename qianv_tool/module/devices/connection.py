#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################################################################
#                                      设备连接属性
#
#  ConnectionAttr -> Connection(ConnectionAttr)  -->  Uiautomator2(Connection)  -->Screenshot(Adb, WSA, DroidCast, AScreenCap, Scrcpy)  --> .....Device-->  AzurLaneAutoScript
# 其中的config 是 AzurLaneConfig
########################################################################################################################
import os
import adbutils
import uiautomator2 as u2
from adbutils import AdbClient, AdbDevice

class Connection:
    # adb的二进制执行文件的地址（toolkit下是项目内安装的，那如何安装呢？
    adb_binary_list = [
        './bin/adb/adb.exe',
        './toolkit/Lib/site-packages/adbutils/binaries/adb.exe',
        '/usr/bin/adb'
    ]

    def __init__(self):
        # Init adb client
        # 修改adb的路径
        adbutils.adb_path = lambda: self.adb_binary

    def adb_binary(self):
        """
        获取adb二进制可执行文件地址
        :return:
        """
        # 默认的文件路径下是否存在adb.exe文件
        for file in self.adb_binary_list:
            if os.path.exists(file):
                return os.path.abspath(file)

        # 尝试获取python虚拟环境下的adb.exe文件
        import sys
        file = os.path.join(sys.executable, '../Lib/site-packages/adbutils/binaries/adb.exe')
        file = os.path.abspath(file).replace('\\', '/')
        if os.path.exists(file):
            return file

        # 获取 用户系统变量（PATH）中配置的adb
        file = 'adb'
        return file

    def adb_client(self) -> AdbClient:
        """
        尝试获取adb客户端(有什么用，这个host和端口是否能连接模拟器，如果是多个模拟器呢）
        :return:
        """
        host = '127.0.0.1'
        port = 5037

        # 尝试从环境变量中获取 adb的端口号
        env = os.environ.get('ANDROID_ADB_SERVER_PORT', None)
        if env is not None:
            try:
                port = int(env)
            except ValueError:
                print(f'logger.warnin Invalid environ variable ANDROID_ADB_SERVER_PORT={port}, using default port')

        print('logger.attrAdbClient', f'AdbClient({host}, {port})')
        return AdbClient(host, port)

    def adb(self) -> AdbDevice:
        return AdbDevice(self.adb_client, self.serial)

    def Test( self ):
        color = (100,20,10)
        print(sum(color))


if __name__ == "__main__":
    connection = Connection()
    # print(connection.adb_binary())
    print(connection.adb_client())
    connection.Test()