#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################################################################
#                                      自定义的adb连接管理器
#
########################################################################################################################
import os
import adbutils
import subprocess
from adbutils import AdbClient, AdbDevice
from qianv_tool.module.devices.utils import (recv_all,remove_shell_warning)

class Adb:
    # adb的二进制执行文件的地址（toolkit下是项目内安装的，那如何安装呢？
    adb_binary_list = [
        './bin/adb/adb.exe',
        './toolkit/Lib/site-packages/adbutils/binaries/adb.exe',
        '/usr/bin/adb'
    ]
    adb_path = ""

    def __init__(self):
        # 修改adb的路径
        adbutils.adb_path = lambda: self.adb_binary
        self.adb_path = self.adb_binary()

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
        获取AdbClient连接：它用于建立与本地计算机或远程计算机上运行的ADB服务器的连接。它提供了与连接的Android设备交互、发送ADB命令、安装和卸载应用程序以及管理设备的功能。
          (有什么用，这个host和端口是否能连接模拟器，如果是多个模拟器呢）
        :return:
        """
        host = '127.0.0.1' # IP地址 127.0.0.1 代表本地主机
        port = 5037 # 所有 adb 客户端均使用端口 5037 与 adb 服务器通信。发出命令时，通过携带设备id，来分辨是发给哪一个设备的

        # 尝试从环境变量中获取 adb的端口号
        env = os.environ.get('ANDROID_ADB_SERVER_PORT', None)
        if env is not None:
            try:
                port = int(env)
            except ValueError:
                print(f'logger.warnin Invalid environ variable ANDROID_ADB_SERVER_PORT={port}, using default port')

        print('logger.attrAdbClient', f'AdbClient({host}, {port})')
        return AdbClient(host, port)


    def adb(self,serial) -> AdbDevice:
        """
        获取AdbDevice服务，通过AdbClient建立连接后的单个Android设备。它允许您直接在设备上执行各种ADB命令，如拉/推送文件、安装/卸载应用程序、运行shell命令等。
        :return:
        """
        return AdbDevice(self.adb_client(),serial)

   # 来源：connection.py =》Connection(ConnectionAttr)
    def adb_shell(self, cmd, serial,stream=False, recvall=True, timeout=10, rstrip=True):
        """
        Equivalent to `adb -s <serial> shell <*cmd>`

        Args:
            cmd (list, str):
            stream (bool): 返回流而不是字符串输出（默认值：False）
            recvall (bool): 当流=True时接收所有数据（默认值：True）
            timeout (int): 超时时间(默认值：10)
            rstrip (bool): 是否去掉最后一行的空格 (默认值: True)

        Returns:
            str if stream=False
            bytes if stream=True and recvall=True
            socket if stream=True and recvall=False
        """
        # 检查是否为字符串，如果不是执行期内逻辑
        if not isinstance(cmd, str):
            # 使用map函数将cmd列表中的元素转换为字符串，并将结果转换为列表
            cmd = list(map(str, cmd))

        if stream:
            result = self.adb(serial).shell(cmd, stream=stream, timeout=timeout, rstrip=rstrip)
            if recvall:
                # bytes
                return recv_all(result)
            else:
                # socket
                return result
        else:
            result = self.adb(serial).shell(cmd, stream=stream, timeout=timeout, rstrip=rstrip)
            result = remove_shell_warning(result)
            # str
            return result

    # 来源：connection.py =》Connection(ConnectionAttr)
    def adb_command(self, cmd, timeout=10,serial=None):
        """
        在子流程中执行ADB命令，
        通常在拉或推大文件时使用。

        Args:
            cmd (list): 命令列表
            timeout (int):超时时间

        Returns:
            str:
        """
        cmd = list(map(str, cmd))
        if serial != None:
            cmd = [self.adb_path, '-s', serial] + cmd
        else:
            cmd = [self.adb_path] + cmd

        print(f'info: Execute: {cmd}')

        # Use shell=True to disable console window when using GUI.
        # Although, there's still a window when you stop running in GUI, which cause by gooey.
        # To disable it, edit gooey/gui/util/taskkill.py

        # No gooey anymore, just shell=False
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=False)
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            print(f'warning: TimeoutExpired when calling {cmd}, stdout={stdout}, stderr={stderr}')
        return stdout

    # ---------------------------------------------------- command 常用命令 -----------------------------------

    def restart_atx(self,serial):
        """
         重新启动指定设备下的 atxAgent 服务，首先关闭，然后启动
        """
        print('info:Restart ATX')
        atx_agent_path = '/data/local/tmp/atx-agent'
        self.adb_shell(['chmod','775',atx_agent_path],serial)
        self.adb_shell([atx_agent_path, 'server', '--stop'],serial)
        # 以非UI自动化模式下启动 atx-agent 服务器，并且指定服务器监听的地址为 127.0.0.1，端口号为 7912 ，
            # -d 是以后台方式运行
            # --nouia: 告诉 ATX 代理不需要与用户界面进行交互，因此它不会启动用户界面相关的服务，测试发现使用它后，u2就无法启动了
        # self.adb_shell([atx_agent_path, 'server', '--nouia', '-d', '--addr', '127.0.0.1:7912'],serial)
        # 有时还是会出现错误：无法提供服务非 am instrument启动
        self.adb_shell([atx_agent_path, 'server', '-d'],serial)
    def stop_uiautomator( self,serial ):
        package_name = 'com.github.uiautomator'
        package_name_test = 'com.github.uiautomator.test'
        self.adb_shell(['am', 'force-stop', package_name],serial)
        self.adb_shell(['am', 'force-stop', package_name_test],serial)

if __name__ == "__main__":
    adb = Adb()
    # print(connection.adb_binary())

    # 获取全部devices: connection.py --> adb_connect.list_device ,通过参考：adb_reconnect
    print(adb.adb_command(['devices','-l']))

    # 先停止uiautomator,然后启动atx会将atx和uiautomator都启动起来
    print(adb.stop_uiautomator('emulator-5554'))
    print(adb.restart_atx('emulator-5554'))

    # 初始化uiautomator2 ？
    # init = u2.init.Initer(adb.adb('emulator-5554'))
    # init.install()
    # print( init.abi)

    # u2.init.Initer(adb.adb('emulator-5554'))


# Connection.install_uiautomator2