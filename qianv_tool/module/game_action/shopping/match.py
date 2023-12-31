
import time
from qianv_tool.module.logger import logger
from qianv_tool.module.base.button_match import ButtonMatch
from qianv_tool.module.game_action.shopping.assets import *


class Match:

    def __init__( self, devices, serial, reply_wait=1):
        self.buttonMatch = ButtonMatch()
        self.devices: Devices = devices
        self.serial = serial
        # 响应等待时间
        self.reply_wait = reply_wait


    def npc_store( self , input_image=None):
        """npc 商店购买物品 [ok]"""
        image = self.devices.device_screenshot(self.serial) if input_image is None else input_image
        result = False
        if self.buttonMatch.image_match(image, SHOPPING_NPC, offset=(-5,-6), interval=0.5,threshold=0.83):
            self.devices.click(self.serial, SHOPPING_NPC)
            time.sleep(self.reply_wait)
            result = True
        if result and self.buttonMatch.image_match(image, SHOPPING_NPC_CLOSE, offset=(0,-3), interval=0.5,threshold=0.83):
            self.devices.click(self.serial, SHOPPING_NPC_CLOSE)
            time.sleep(self.reply_wait)
            result = True
        else:
            result = False
        return result

    def player_store( self, input_image=None):
        """玩家 商店购买物品 [ok]"""
        image = self.devices.device_screenshot(self.serial) if input_image is None else input_image
        result = False
        if self.buttonMatch.image_match(image, SHOPPING_PLAYER, offset=(-5,-6), interval=0.5):
            # 点击购买
            self.devices.click(self.serial, SHOPPING_PLAYER)
            time.sleep(self.reply_wait)
            result = True
            image = self.devices.device_screenshot(self.serial)
        if result and self.buttonMatch.image_match(image, SHOPPING_PLAYER_CONFIRM, offset=(-5,-6), interval=0.5,threshold=0.83):
            # 确认购买商品
            self.devices.click(self.serial, SHOPPING_PLAYER_CONFIRM)
            time.sleep(self.reply_wait)
            result = True
            image = self.devices.device_screenshot(self.serial)
        if result and self.buttonMatch.image_match(image, SHOPPING_PLAYER_CLOSE, offset=(0,-6), interval=0.5,threshold=0.81):
            # 关闭商店
            self.devices.click(self.serial, SHOPPING_PLAYER_CLOSE)
            time.sleep(self.reply_wait)
            result = True
        else:
            result = False
        return result
    def close_buy_windwo( self ,input_image=None):
        """
         关闭购买窗口
        """
        image = self.devices.device_screenshot(self.serial) if input_image is None else input_image
        if self.buttonMatch.image_match(image, SHOPPING_PLAYER_CLOSE, offset=(0,-6), interval=0.5,threshold=0.81):
            self.devices.click(self.serial, SHOPPING_PLAYER_CLOSE)
            image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image, SHOPPING_NPC_CLOSE, offset=(0,-3), interval=0.5,threshold=0.83):
            self.devices.click(self.serial, SHOPPING_NPC_CLOSE)

    def is_fabao_search( self , input_image=None):
        """ 是否 法宝搜索页面，是就点击搜索"""
        image = self.devices.device_screenshot(self.serial) if input_image is None else input_image
        if self.buttonMatch.image_match(image, SHOPPING_FABAO_SEARCH, offset=(0,0)):
            self.devices.click(self.serial, SHOPPING_FABAO_SEARCH)
            time.sleep(self.reply_wait)
            return True
        return False

if __name__ == "__main__":

    from qianv_tool.module.devices.devices import Devices

    devices = Devices()
    devices_info = devices.devices_info
    for serial in devices_info:
        if serial=='emulator-5554':
            print(devices_info[serial])
            app = Match(devices, serial)
            # print(app.is_map('金陵'))
            print(app.npc_store())


