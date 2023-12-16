
import numpy as np
from qianv_tool.module.base.button import Button
from qianv_tool.module.base.button import ButtonGrid


origin_button = Button(area={'game': (128, 136, 240, 192)},text={'game': '队伍'}, color={'game': (95, 131, 171)}, button={'game': (128, 136, 240, 192)}, file={'game': './assets/game/mian_window/TEAM_NO_SELECT.png'})
exchange_bottom_navbar = ButtonGrid(origin_button=origin_button, delta=(208, 0), grid_shape=(2, 1), text='自然人')

b = exchange_bottom_navbar.buttons()
print("dddddd")