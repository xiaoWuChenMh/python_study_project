################################################################################################################
#                                              按钮匹配
#
################################################################################################################


from qianv_tool.module.base.timer import Timer
from qianv_tool.module.base.button import ButtonGrid


class ButtonMatch:

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
        threshold = self.config.BUTTON_MATCH_SIMILARITY if threshold is None else threshold
        if self.__interval(button,interval):
            return False
        if isinstance(offset, bool):
            offset = self.config.BUTTON_OFFSET
        appear = button.match(image, offset=offset,threshold=threshold)
        if appear and interval:
            self.interval_timer[button.name].reset()
        return appear


    def color_match(self, image, button, interval=0, threshold=None):
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
        threshold = self.config.COLOR_SIMILAR_THRESHOLD if threshold is None else threshold
        if self.__interval(button,interval):
            return False
        appear = button.appear_on(image,threshold=threshold)
        if appear and interval:
            self.interval_timer[button.name].reset()
        return appear


    def word_match(self, image, button, offset=0, interval=0, model=1):
        """
        文字匹配（模糊匹配
        :param image: 源图
        :param button: 匹配的按钮对象
        :param offset(int, tuple): Detection area offset
        :param interval (int, float): 两个活动事件之间的间隔。
        :param model(int): 匹配模式 1-模糊；2-严格
        :return:
        """
        if self.__interval(button,interval):
            return False
        if isinstance(offset, bool):
            offset = self.config.BUTTON_OFFSET
        appear = button.word(image,offset,model)
        if appear and interval:
            self.interval_timer[button.name].reset()
        return appear

    def grid_button_word_match(self, image, origin_button, site_button, grid_shape, text):
        """
         网格按钮中的文字匹配
        :param image: 源图
        :param origin_button: 起点按钮
        :param site_button: 点位按钮，起点按钮在点位按钮的左上角，通过该图计算delta
        :param delta: 移动的距离（x,y）
        :param grid_shape: 网格大小(行，列)
        :param text: 待匹配的文本
        :return: 匹配到返回button,否则 None
        """
        delta = site_button.area_size()
        button_grip = ButtonGrid(origin_button=origin_button, delta=delta, grid_shape=grid_shape, text=text)
        for button in button_grip:
            if self.word_match(image,button):
                return button
        return None

    def grid_button_color_match(self, image, origin_button, site_button, grid_shape):
        """
         网格按钮中的颜色匹配
        :param image: 源图
        :param origin_button: 起点按钮
        :param site_button: 点位按钮，起点按钮在点位按钮的左上角，通过该图计算delta
        :param delta: 移动的距离（x,y）
        :param grid_shape: 网格大小(行，列)
        :return: 匹配到返回button,否则 None
        """
        result_button = None
        delta = site_button.area_size()
        button_grip = ButtonGrid(origin_button=origin_button, delta=delta, grid_shape=grid_shape)
        for button in button_grip:
            if not self.color_match(image,button):
                break
            else:
                result_button = button
        return result_button



