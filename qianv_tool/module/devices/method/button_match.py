################################################################################################################
#                                              按钮匹配
#
################################################################################################################


from qianv_tool.module.base.timer import Timer


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



    def dialog_top_button(self, image, below_button, step, interval=0, threshold=None):
        """
        上移动查找对话框的顶部按钮
        :param image: 截图
        :param below_button: 底部按钮
        :param step: 移动的步长 （below_button.area_size()[1]+frame_button.area_size()[1]）
        :param interval: 两个活动事件之间的间隔。
        :param threshold:
        :return:
        """
        threshold = self.config.COLOR_SIMILAR_THRESHOLD if threshold is None else threshold
        if self.__interval(below_button,interval):
            return False
        appear = below_button.match(image,offset=0, threshold=threshold)
        top_appear = appear
        with appear:
            top_appear = appear
            appear = below_button.match(image,offset=(0,step), threshold=threshold)
        if top_appear and interval:
            self.interval_timer[below_button.name].reset()
        return top_appear


    ## 左和下移动区域

    def word_match(self,image,left_top_button, step=(0,0), offset=0):
        """
        文字匹配
        """
        image_word = ''
        if self.__interval(button,interval):
            return False
        if isinstance(offset, bool):
            offset = self.config.BUTTON_OFFSET
        appear = button.word(image,offset)
        if appear and interval:
            self.interval_timer[button.name].reset()
        return appear
