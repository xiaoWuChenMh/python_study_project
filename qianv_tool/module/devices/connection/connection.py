########################################################################################################################
#                                      连接管理器
#
# restart_device_service ： 重启设备服务(uiautomator、atxAgent)
# device_restart ： Reboot adb client
#
########################################################################################################################

from qianv_tool.module.logger import logger
from qianv_tool.module.devices.connection.uiautomator import Uiautomator

class Connection(Uiautomator):

    def __init__(self):
        super().__init__()


    def restart_device_service(self, serial):
        """
         重启设备服务(uiautomator、atxAgent)
        :param serial:
        :return:
        """
        self.uiautomator_stop(serial)
        self.atx_restart(serial)

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



if __name__ == "__main__":
    connection = Connection()
    connection.stop_uiautomator('emulator-5554')
    connection.restart_atx('emulator-5554')