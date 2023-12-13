################################################################################################################
#                        设备操作
#
# find_emulator_devices：发现当前pc上的所有模拟器设备
# init_devices：初始化所有设备，即安装需要的应用
# pc_system_info：pc的系统信息
#
# 初始化过程： find_devices Then init_devices  Then 是否能正确连接 （否：关闭u2服务 then 重启atx服务） then 再次测试 then 重试3次不行报错
################################################################################################################

import uiautomator2 as u2
import subprocess

import time
from functools import wraps
from json.decoder import JSONDecodeError
from adbutils.errors import AdbError
from qianv_tool.module.logger import logger

from qianv_tool.module.devices.connection.connection import Connection
from qianv_tool.module.devices.utils import (sys_command,possible_reasons,handle_adb_error,is_emulator)
from qianv_tool.module.devices.exception import RequestHumanTakeover
from qianv_tool.module.devices.exception import ImageTruncated

# 默认和设备连接失败重试次数
RETRY_TRIES = 5






# 和设备发生连接错误时进行重试的逻辑
def retry(func):

    # 重试时的睡眠时间
    def retry_sleep( self, trial=None ):
        if trial == 0:
            pass
        elif trial == 1:
            pass
        # Failed twice
        elif trial == 2:
            time.sleep(1)
        # Failed more
        else:
            time.sleep(3)
    def get_serial(args):
        for v in args:
            if is_emulator(v):
                return v
        return None

    @wraps(func)
    def retry_wrapper(self, *args, **kwargs):
        """
        Args:
            self (Uiautomator2):
        """
        serial = get_serial(args)
        init = None
        for _ in range(RETRY_TRIES):
            try:
                if callable(init):
                    retry_sleep(_)
                    init()
                return func(self, *args, **kwargs)
            # Can't handle
            except RequestHumanTakeover:
                break
            # When adb server was killed
            except ConnectionResetError as e:
                logger.error(e)
                def init():
                    self.device_restart()
            # In `device.set_new_command_timeout(604800)`
            # json.decoder.JSONDecodeError: Expecting value: line 1 column 2 (char 1)
            except JSONDecodeError as e:
                logger.error(e)
                def init():
                    # 需要获取所有设备ID
                    self.init_devices()
            except ValueError as e:
                logger.error(e)
                def init():
                    # 需要获取所有设备ID
                    self.restart_device_service(serial)
            # AdbError
            except AdbError as e:
                if handle_adb_error(e):
                    def init():
                        self.device_restart()
                else:
                    break
            # RuntimeError: USB device 127.0.0.1:5555 is offline
            except RuntimeError as e:
                if handle_adb_error(e):
                    def init():
                        self.device_restart()
                else:
                    break
            # In `assert c.read string(4) == _OKAY`
            # ADB on emulator not enabled
            except AssertionError as e:
                logger.exception(e)
                possible_reasons(
                    'If you are using BlueStacks or LD player or WSA, '
                    'please enable ADB in the settings of your emulator'
                )
                break
            # ImageTruncated
            except ImageTruncated as e:
                logger.error(e)
                def init():
                    pass
            # Unknown
            except Exception as e:
                logger.exception(e)
                def init():
                    pass

        logger.critical(f'Retry {func.__name__}() failed')
        raise 8

    return retry_wrapper


class Devices(Connection):

    # 设备列表：{'设备ID': {'serial': '设备ID','state': '状态：offline-离线；device-在线'},'设备ID':....}
    devices_info = {}

    # 系统信息 {'system': '64bit', 'cpu': 'AMD64'}
    system_info = {}


    def __init__( self ):
        super().__init__()
        self.pc_system_info()
        self.find_devices()
        # self.init_devices()

    def find_devices( self ):
        """
         发设备
        :return:
        """
        self.devices_info = {}
        for info in self.adb_client.list():
            serial = info.serial
            state = info.state
            if state == 'offline':
                logger.warning(f'Device {serial} is offline, disconnect it before connecting')
            elif state == 'unauthorized':
                logger.error(f'Device {serial} is unauthorized, please accept ADB debugging on your device')
            elif state == 'device':
                pass
            else:
                logger.warning(f'Device {serial} is is having a unknown status: {state}')
            self.devices_info[serial] = {'serial':serial,'state':state}
        return self

    def device_restart(self,serial=None):
        """
            Reboot adb client
        """
        if serial == None :
            logger.info('Restart device for all device')
            self.adb_restart()
            self.find_devices()
        else:
            logger.info(f'Restart device for {serial}')
            self.adb_disconnect(serial)
            self.adb_client.connect(serial)
            self.find_devices()

    def init_devices(self):
        """
        初始化设备，等同于执行 'python -m uiautomator2 init' 命令
        :return:
        """
        if len(self.devices_info) == 0:
            logger.warning('init device error: no valid device')
            return self
        for serial in self.devices_info:
            device = self.devices_info[serial]
            try:
                if device['state'] == 'device':
                    self.install_uiautomator2(serial)
                    logger.info(f'init device install uiautomator2: serial({serial}) ' )
            except Exception as e:
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

    @retry
    def device_info_print( self,serial ):
        """
        尝试使用retry,在u2服务没有启动的时候，第一次执行失败，然后通过报错+回调函数调用重启服务后，再次执行该段代码成功
        :param serial:
        :return:
        """

        a = self.u2_device(serial)
        print(a.info)

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
    for serial in __devices.devices_info:
        __devices.device_info_print(serial)





