################################################################################################################
#                        设备操作
#
# find_emulator_devices：发现当前pc上的所有模拟器设备
# init_devices：初始化所有设备，即安装需要的应用
# pc_system_info：pc的系统信息
#
# 初始化过程： find_devices Then init_devices  then 是否能正确连接 （否：关闭u2服务 then 重启atx服务） then 再次测试 then 重试3次不行报错
################################################################################################################

import uiautomator2 as u2
import subprocess


from qianv_tool.module.logger import logger
from qianv_tool.module.devices.connection.connection import Connection
from qianv_tool.module.devices.utils import (sys_command)

class Devices(Connection):

    # 设备信息：{'设备ID': {'serial': '设备ID','state': '状态：offline-离线；device-在线'},'设备ID':....}
    devices_info = {}

    # 系统信息 {'system': '64bit', 'cpu': 'AMD64'}
    system_info = {}


    def __init__( self ):
        super().__init__()
        self.pc_system_info()
        self.find_emulator_devices()
        self.init_devices()

    def is_emulator(self,serial):
        return serial.startswith('emulator-') or serial.startswith('127.0.0.1:')

    def find_emulator_devices( self ):
        """
         发现模拟器设备
        :return:
        """
        for info in self.adb_client.list():
            serial = info.serial
            if self.is_emulator(serial):
                state = info.state
                self.devices_info[serial] = {'serial':serial,'state':state}
        return self


    def init_devices(self):
        """
        初始化设备，等同于执行 'python -m uiautomator2 init' 命令
        :return:
        """
        if len(self.devices_info) == 0:
            logger.warning('init device error: no valid device')
            return self
        for device in self.devices_info:
            serial = device['serial']
            try:
                if device['state'] != 'device':
                    self.install_uiautomator2(serial)
                    device['install_tag'] = '1'
                else:
                    device['install_tag'] = '0'
            except Exception as e:
                device['install_tag'] = '0'
                logger.warning('init device error, serial(%s) : %s' % (serial,e))
        return self



    def pc_system_info(self):
        """
        pc的系统系统：系统架构(system) 和 cpu类型（cpu）
        :return:
        """
        try:
            adb_command = 'python -c "import platform;print(platform.architecture()[0]);print(platform.machine())"'
            cmd_result = sys_command(adb_command,shell=True).split('\n')
            system = cmd_result[0].strip()
            cpu = cmd_result[1].strip()
            self.system_info['system'] = system
            self.system_info['cpu'] = cpu
            logger.info('cp system info: system(%s) cpu(%s)' % (system, cpu))
        except Exception as e:
            self.system_info['system'] = 'null'
            self.system_info['cpu'] = 'null'
            logger.info('Get cp system info Error: %s' % (e))
        return self

    # 设置设备标识 emulator-5554 、emulator-5556、 emulator-5558 、emulator-5560
    # 不一定管用
    def init_atx(self,device_id):
        # 执行 adb shell 命令
        logger.info('Exe adb shell (%s):  ---------------- start ---------------------' % (device_id))
        adb_shell_process = subprocess.Popen(['adb', '-s', device_id, 'shell'], stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = ('','')
        try:
            # 执行 chmod 命令
            chmod_command = "chmod 775 /data/local/tmp/atx-agent\n"
            adb_shell_process.stdin.write(chmod_command.encode('utf-8'))
            adb_shell_process.stdin.flush()

            # 执行 atx-agent 命令
            agent_command = "/data/local/tmp/atx-agent server -d\n"
            adb_shell_process.stdin.write(agent_command.encode('utf-8'))
            adb_shell_process.stdin.flush()

            # 退出 adb shell
            exit_command = "exit\n"
            adb_shell_process.stdin.write(exit_command.encode('utf-8'))
            adb_shell_process.stdin.flush()

            # 获取命令的返回内容和错误信息
            output, error = adb_shell_process.communicate()

            # 通过uiautomator2 和指定设备建立连接(执行较慢3~5米啊）
            u2_connect_info = u2.connect(device_id).info
            if 'currentPackageName' in u2_connect_info:
                device_info = self.devices_info[device_id]['connect_statu'] = '1'
                logger.info('connect device success (%s) : %s' % ( device_id, u2_connect_info ))
            else:
                device_info = self.devices_info[device_id]['connect_statu'] = '0'
                # 输出命令返回错误信息(正常执行后，error也有信息输出，所以输出前还需要检查是否成功连接，失败后再输出)
                logger.info('connect device Error Output (%s) : %s' % (device_id, error.decode('utf-8')) )
            logger.info('connect device Error Output (%s) : %s' % (device_id, error.decode('utf-8')))
            # 输出命令返回内容
            if len(output)>3 :
                logger.info('Command Output (%s): %s' % (device_id,output.decode('utf-8')))
        except Exception as e:
            print(e)
            logger.info('Exe adb shell (%s), init axt error!!!' % (device_id))
            device_info = self.devices_info[device_id]['connect_statu'] = '0'
        finally:
            # 关闭stdin、stdout和stderr
            adb_shell_process.stdin.close()
            adb_shell_process.stdout.close()
            adb_shell_process.stderr.close()
            # 等待进程结束
            adb_shell_process.wait()

            logger.info('Exe adb shell (%s):  ---------------- end ---------------------' % (device_id))
        return self


    def screenshot( self ):
        """
        截图
        :return:
        """
        pass

    def click( self ,button):
        """
        点击指定按钮
        :param button:
        :return:
        """
        pass

if __name__ == "__main__":
    __devices = Devices()
    # for key, value in __devices.devices_info.items():
    #     if value['statu'] == '1' :
    #         # 如何判断atx是否正常呢，调用u2.connect('emulator-5554')查看是否报错？
    #         __devices.init_atx(key)
    print(__devices.devices_info)
    print(__devices.system_info)


