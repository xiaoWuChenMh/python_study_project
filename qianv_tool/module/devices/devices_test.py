
import time
import multiprocessing
from qianv_tool.module.logger import logger


class StartDevices:


    def __init__( self, devices, serial):
        # 设备管理对象
        self.devices: Devices = devices
        # 设备ID
        self.serial = serial


    def run(self):
        image = self.devices.device_screenshot(self.serial)
        print(f"{self.serial} :截图成功")



def run_exe(serial,devices):
    app = StartDevices(devices, serial)
    app.run()

if __name__ == "__main__":

    from qianv_tool.module.devices.devices import Devices
    multi_process = []
    devices = Devices()
    devices_info = devices.devices_info

    for serial in devices_info :
        print(devices_info[serial])
        process = multiprocessing.Process(target=run_exe, args=(serial,devices,))
        multi_process.append(process)
        process.start()
    # join 方法可以让主线程等待所有子线程执行完毕后再结束。
    for process in multi_process:
        process.join()