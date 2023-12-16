################################################################################################################
#                                              运行
#
# 初始化：初始化devices
################################################################################################################

import threading
from qianv_tool.gui.app import App
from qianv_tool.module.devices.devices import Devices


class TaskThread(threading.Thread):
    def __init__(self,serial,device_info):
        super().__init__()
        self._stop_event = threading.Event()
        self.serial = serial

    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            # 在这里编写线程的逻辑
            print("线程正在执行...")


class Run:

    def __init__(self):

        # 初始化设备信息
        self.devices = Devices()

        #载入执行线程
        self.load_exe_thread(self.devices.info())

        # 启动 gui页面
        App(self.devices).mainloop()


    def load_exe_thread(self,info):
        for serial in info:
            device_info = info[serial]
            thread = TaskThread(serial,device_info)
            info['thread'] = thread



if __name__ == "__main__":
    run =  Run()
    run.start_device()