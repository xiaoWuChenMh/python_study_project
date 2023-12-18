################################################################################################################
#                                              按钮匹配
#
################################################################################################################

import copy
from qianv_tool.module.base.timer import Timer
from qianv_tool.module.base.button import ButtonGrid


class ButtonMatch:

    """
    module.base
    """
    COLOR_SIMILAR_THRESHOLD = 10
    BUTTON_OFFSET = 30
    WAIT_BEFORE_SAVING_SCREEN_SHOT = 1
    BUTTON_MATCH_SIMILARITY = 0.85

    def __init__(self):
        self.interval_timer = {}

    def __interval(self,button,interval):
        """启动定时"""
        if interval:
            if button.name in self.interval_timer:
                if self.interval_timer[button.name].limit != interval:
                    self.interval_timer[button.name] = Timer(interval)
            else:
                self.interval_timer[button.name] = Timer(interval)
            if not self.interval_timer[button.name].reached():
                return True
        return False

    def image_match(self, image, button, offset=0, interval=0, threshold=None):
        """
        匹配图片本身: appear(MAP_PREPARATION, offset=(20, 20)
        Args:
            image : 截图
            button (Button, Template, HierarchyButton, str):
            offset (bool, int):
            interval (int, float): 两个活动事件之间的间隔。
            threshold (int, float): 如果使用偏移量，则为0到1，越大意味着越相似，如果不使用偏移量，则为 0 到 255，越小表示越相似

        Returns:
            bool:
            ```
        """
        threshold = self.BUTTON_MATCH_SIMILARITY if threshold is None else threshold
        if self.__interval(button,interval):
            return False
        if isinstance(offset, bool):
            offset = self.BUTTON_OFFSET
        appear = button.match(image, offset=offset,threshold=threshold)
        if appear and interval:
            self.interval_timer[button.name].reset()
        return appear


    def color_match(self, image, button, offset=0, interval=0, threshold=None):
        """
        匹配图片颜色
        Args:
            image : 截图
            button (Button, Template, HierarchyButton, str):
            interval (int, float): 两个活动事件之间的间隔。
            threshold (int, float): 如果使用偏移量，则为0到1，越大意味着越相似，如果不使用偏移量，则为 0 到 255，越小表示越相似

        Returns:
            bool:
            ```
        """
        threshold = self.COLOR_SIMILAR_THRESHOLD if threshold is None else threshold
        if self.__interval(button,interval):
            return False
        if isinstance(offset, bool):
            offset = self.BUTTON_OFFSET
        appear = button.appear_on(image,threshold=threshold)
        if appear and interval:
            self.interval_timer[button.name].reset()
        return appear


    def word_match(self, image, button, text=None, offset=0, interval=0, model=1):
        """
        文字匹配（模糊匹配
        :param image: 源图
        :param button: 匹配的按钮对象
        :param text: 待匹配的文本
        :param offset(int, tuple): Detection area offset
        :param interval (int, float): 两个活动事件之间的间隔。
        :param model(int): 匹配模式 1-模糊；2-严格
        :return:
        """
        if self.__interval(button,interval):
            return False
        if isinstance(offset, bool):
            offset = self.BUTTON_OFFSET
        if text != None:
            button.text=text
        appear = button.word(image,offset,model)
        if appear and interval:
            self.interval_timer[button.name].reset()
        return appear

    def grid_button_word_match(self, image, origin_button, delta, grid_shape, text='', offset=0):
        """
         网格按钮中的文字匹配
        :param image: 源图
        :param origin_button: 起点按钮
        :param delta: 移动的距离（x,y）
        :param grid_shape: 网格大小(行，列)
        :param text: 待匹配的文本
        :param offset(int, tuple): Detection area offset
        :return: 匹配到返回button,否则 None
        """
        button_grip = ButtonGrid(origin_button=origin_button, delta=delta, grid_shape=grid_shape, text=text)
        for button in button_grip.buttons():
            if  self.word_match(image,button,text,offset=offset):
                return button
        return None

    def grid_button_image_match(self, image, origin_button, delta, grid_shape, offset=0, threshold=None):
        """
         网格按钮中的颜色匹配
        :param image: 源图
        :param origin_button: 起点按钮
        :param delta: 移动的距离（x,y）
        :param grid_shape: 网格大小(行，列)
        :param offset(int, tuple): Detection area offset
        :param threshold (int, float): 如果使用偏移量，则为0到1，越大意味着越相似，如果不使用偏移量，则为 0 到 255，越小表示越相似
        :return: 匹配到返回button,否则 None
        """
        result_button = None
        button_grip = ButtonGrid(origin_button=origin_button, delta=delta, grid_shape=grid_shape)
        for button in button_grip.buttons():
            if not self.image_match(image,button,offset=offset,threshold=threshold):
                break
            else:
                result_button = button
        return result_button



