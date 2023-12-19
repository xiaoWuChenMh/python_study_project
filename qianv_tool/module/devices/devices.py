################################################################################################################
#                        设备操作
#
# find_emulator_devices：发现当前pc上的所有模拟器设备
# init_devices：初始化所有设备，即安装需要的应用
# pc_system_info：pc的系统信息
#
# 初始化过程： find_devices Then init_devices  Then 是否能正确连接 （否：关闭u2服务 then 重启atx服务） then 再次测试 then 重试3次不行报错
################################################################################################################

import time
import copy
from functools import wraps
from json.decoder import JSONDecodeError
from adbutils.errors import AdbError
from qianv_tool.module.devices.connection.connection import Connection
from qianv_tool.module.devices.utils import *
from qianv_tool.module.devices.exception import RequestHumanTakeover
from qianv_tool.module.devices.exception import ImageTruncated



# 和设备发生连接错误时进行重试的逻辑
def retry(func):

    # 默认和设备连接失败重试次数
    RETRY_TRIES = 5

    # 获取设备信息
    def get_serial(args):
        for v in args:
            if is_emulator(v):
                return v
            # 其他类型：无，当前仅支持模拟器
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
            # AdbError
            except BaseException as e:
                if handle_adb_error(e):
                    def init():
                        self.get_u2(serial)
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


    def info(self):
        return self.devices_info

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


    def find_devices( self ):
        """
         发现设备
        :return:
        """
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
            if serial in self.devices_info:
                device = self.devices_info[serial]
                device['serial'] = serial
                device['state'] = state
            else:
                self.devices_info[serial] = {'serial':serial,'state':state}
        return self


    @retry
    def device_info_print( self,serial ):
        """
        尝试使用retry,在u2服务没有启动的时候，第一次执行失败，然后通过报错+回调函数调用重启服务后，再次执行该段代码成功
        :param serial:
        :return:
        """

        self.get_u2(serial)

    @retry
    def device_screenshot(self, serial):
        """
        截图
        :return:
        """
        return self.screenshot(serial)

    @retry
    def click( self,serial,button,offset=None):
        """
        点击指定按钮
        TODO 加一个随机睡眠n秒，来对冲多次点击相隔实现将近的问题。
        :param serial:设备id
        :param button:带点击的按钮
        :param offset:点击按钮是否有位移
        :return:
        """
        x, y = random_rectangle_point(button.button)
        x, y = ensure_int(x, y)
        if isinstance(offset, tuple) and len(offset) == 2:
            x  = x+offset[0]
            y  = y+offset[1]
        logger.info(
            'Click %s @ %s' % (point2str(x, y), button)
        )
        self.click_uiautomator2(serial,x,y)

    @retry
    def swipe( self,serial, sx, sy, ex, ey):
        """
        滑动
        direction: 手指右滑方向，4选1 "left", "right", "up", "down"
        scale: 滑动距离，默认0.2即屏幕宽度的20%
        """
        self.swipe_uiautomator2(serial, sx, sy, ex, ey)

    @retry
    def central_site_click(self, serial, offset=None):
        """
        点击屏幕位置，支持偏移
        :param serial:
        :param offset:
        :return:
        """
        x,y = self.central_coordinate(serial)
        if isinstance(offset, tuple) and len(offset) == 2:
            x = x+offset[0]
            y = y+offset[1]
        self.click_uiautomator2(serial, x, y)


if __name__ == "__main__":
    __devices = Devices()

    print(__devices.devices_info)
    print(__devices.system_info)
    for serial in __devices.devices_info:
        __devices.device_info_print(serial)





