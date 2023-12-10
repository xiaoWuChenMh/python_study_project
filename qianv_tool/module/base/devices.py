#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################################################
#                        设备操作
#  设备信息说明：
#      devices_info = {'设备ID': {'statu': '状态：0-异常；1-正常', 'product': '命令返回信息', 'model': '命令返回信息', 'device': '命令返回信息', 'transport_id': '命令返回信息'},'设备ID':....}
#      system_info =  {'system': '64bit', 'cpu': 'AMD64'}
################################################################################################################

import uiautomator2 as u2
import subprocess
from qianv_tool.module.logger import logger

class Devices:

    devices_info = {}

    system_info = {}

    def __init__( self ):
        pass

    def cmdExe( self, command ):
        """
         执行cmd命令
        :param command: 待执行的命令
        :return:
        """
        # 执行命令
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        # 获取输出结果
        output = result.stdout.strip()
        # 返回输出结果
        return output

    def find_devices( self ):
        """
         发现设备
        :return:
        """
        adb_command = 'adb devices -l'
        cmd_result =  self.cmdExe(adb_command).split('\n')
        for dv in cmd_result[1:] :
            device_info = {}
            try:
                if 'offline ' in dv:
                    results = dv.split(' offline ')
                    device_id = results[0].strip()
                    logger.info('find device error: %s' % (device_id))
                    device_info['statu'] = '0'
                    self.devices_info[device_id] = {}
                else:
                    results = dv.split(' device ')
                    device_id = results[0].strip()
                    logger.info('find device success: %s' % (device_id) )
                    device_info['statu'] = '1'
                    others_info = results[1].strip().split(' ')
                    for info in others_info:
                        key = info.split(':')[0].strip()
                        value = info.split(':')[1].strip()
                        device_info[key] = value
                    self.devices_info[device_id] = device_info
            except Exception:
                pass
        return self


    def install_atx(self):
        """
         在设备中安装atx等app
         命令返回值 # 'Successfully init AdbDevice(serial=emulator-5554) \nSuccessfully init AdbDevice(serial=emulator-5556) \n\x1b[0m'
        :return:
        """
        try:
            adb_command = 'python -m uiautomator2 init'
            cmd_result = self.cmdExe(adb_command).split('\n')
            for dv in cmd_result:
                if 'Successfully' in dv:
                    device_id = dv.split('serial=')[1][0:-1]
                    device_info = self.devices_info[device_id]
                    device_info['install_tag'] = '1'
        except Exception:
            pass

    def check_processor(self):
        """
        检查处理器架构：系统架构(system) 和 cpu类型（cpu）
        :return:
        """
        try:
            adb_command = 'python -c "import platform;print(platform.architecture()[0]);print(platform.machine())"'
            cmd_result = self.cmdExe(adb_command).split('\n')
            self.system_info['system'] = cmd_result[0].strip()
            self.system_info['cpu'] = cmd_result[1].strip()
        except Exception:
            self.system_info['system'] = 'null'
            self.system_info['cpu'] = 'null'
        return self

    # 设置设备标识 emulator-5554 、emulator-5556、 emulator-5558 、emulator-5560
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
            # 输出命令返回内容
            if len(output)>3 :
                logger.info('Command Output (%s): %s' % (device_id,output.decode('utf-8')))
        except KeyError:
            print("r")
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




if __name__ == "__main__":
    __devices = Devices()
    __devices.find_devices()
    # __devices.install_atx()
    __devices.check_processor()
    for key, value in __devices.devices_info.items():
        if value['statu'] == '1' :
            # 如何判断atx是否正常呢，调用u2.connect('emulator-5554')查看是否报错？
            __devices.init_atx(key)
    print(__devices.devices_info)
    print(__devices.system_info)


