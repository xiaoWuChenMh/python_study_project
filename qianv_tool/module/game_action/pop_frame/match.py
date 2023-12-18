
from qianv_tool.module.logger import logger
from qianv_tool.module.base.button_match import ButtonMatch
from qianv_tool.module.game_action.pop_frame.assets import *


class Match:

    def __init__( self, devices, serial, reply_wait=1):
        self.buttonMatch = ButtonMatch()
        self.devices: Devices = devices
        self.serial = serial
        # 窗口切换等待时间
        self.reply_wait = reply_wait

    def click_top_npc_dialogue( self ):
        """
         查找顶层的npc对话框，并点击
        """
        image = self.devices.device_screenshot(self.serial)
        is_dialogue = self.buttonMatch.image_match(image, POP_NPC_DIALOGUE, offset=(-6,0))
        if is_dialogue:
            delta = POP_NPC_DIALOGUE_SITE.area_size()
            delta = (-delta[0], -delta[1] + 7)
            target_button = self.buttonMatch.grid_button_image_match(image,POP_NPC_DIALOGUE,delta,(1, 6),offset=(-6,0),threshold=0.81)
            if target_button:
                self.devices.click(self.serial, target_button)
                return True
            else:
                return False
        return False

    def click_botton_npc_text_dialogue( self ):
        """
        点击底部的npc文字版对话框
        """
        image = self.devices.device_screenshot(self.serial)
        if self.buttonMatch.image_match(image, POP_NPC_TEXT_TAG, offset=(0,-4), threshold=0.81):
            self.devices.click(self.serial, POP_NPC_TEXT_TAG)
            return True
        else :
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
            print(app.click_top_npc_dialogue())
            # print(app.click_botton_npc_text_dialogue())


