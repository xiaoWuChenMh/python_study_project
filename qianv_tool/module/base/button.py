import os
import imageio
from PIL import ImageDraw
from paddleocr import PaddleOCR
from qianv_tool.module.base.utils import *
from qianv_tool.module.base.resource import Resource
from qianv_tool.module.base.decorator import cached_property
from qianv_tool.config.exe_config  import ExecuteConfig as ButtonExt
from qianv_tool.module.logger import logger




# 图片匹配：match ，对目标图片进行剪裁，然后和button对象进行对比,前提是需要先调用ensure_template（）
# 图片中的颜色匹配：appear_on


# 定义为全局变量，只需要下载一次 ,默认使用的模型：ocr_version=PP-OCRv4
# use_angle_cls=True ：使用方向分类器识别180度旋转文字
# use_gpu=False ：不使用GPU
# lang="ch" ：识别中文
word_ocr = PaddleOCR(use_angle_cls=True, lang="ch",use_gpu=False)

class Button(Resource):
    def __init__(self, area, text, color, button, initial_area=None, file=None, name=None):
        """Initialize a Button instance.

        Args:
            area (dict[tuple], tuple): Area that the button would appear on the image.
                          (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y)
            color (dict[tuple], tuple): Color we expect the area would be.
                           (r, g, b)
            button (dict[tuple], tuple): Area to be click if button appears on the image.
                            (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y)
                            If tuple is empty, this object can be use as a checker.
        Examples:
            BATTLE_PREPARATION = Button(
                area=(1562, 908, 1864, 1003),
                color=(231, 181, 90),
                button=(1562, 908, 1864, 1003)
            )
        """
        self.raw_area = area
        self.raw_color = color
        self.raw_button = button
        self.raw_file = file
        self.raw_name = name
        self.raw_initial_area = initial_area  if initial_area else area
        self.raw_text = text

        self._button_offset = None
        self._match_init = False
        self._match_binary_init = False
        self._match_luma_init = False
        self.image = None
        self.image_binary = None
        self.image_luma = None

        # 图像测试开关
        self.image_test = False

        if self.file:
            self.resource_add(key=self.file)

    cached = ['area', 'color', '_button', 'file', 'name', 'is_gif']

   ## ---------------------- 【认证】获取模块对象的各个属性的值 start --------------------------
    @cached_property
    def area(self):
        return self.parse_property(self.raw_area)

    @cached_property
    def initial_area(self):
        return self.parse_property(self.raw_initial_area)

    @cached_property
    def text(self):
        return self.parse_property(self.raw_text)

    @cached_property
    def color(self):
        return self.parse_property(self.raw_color)

    @cached_property
    def _button(self):
        return self.parse_property(self.raw_button)

    @cached_property
    def file(self):
        return self.parse_property(self.raw_file)

    @cached_property
    def name(self):
        if self.raw_name:
            return self.raw_name
        elif self.file:
            return os.path.splitext(os.path.split(self.file)[1])[0]
        else:
            return 'BUTTON'
    ## ---------------------- 【认证】获取模块对象的各个属性的值 end --------------------------

    ## ---------------------- 【认证】 一些通用方法 start --------------------------
    @cached_property
    def is_gif(self):
        if self.file:
            return os.path.splitext(self.file)[1] == '.gif'
        else:
            return False

    def __str__(self):
        return self.name

    __repr__ = __str__

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(self.name)

    def __bool__(self):
        return True

    def area_size(self):
        x1, y1, x2, y2 = map(int, map(round,self.area))
        shape_x = x2-x1
        shape_y = y2-y1
        return shape_x,shape_y

    def button_size(self):
        x1, y1, x2, y2 = map(int, map(round,self.button))
        shape_x = x2-x1
        shape_y = y2-y1
        return shape_x,shape_y

    def area_origin(self):
        x1, y1, x2, y2 = map(int, map(round,self.area))
        return x1,y1
    def button_origin(self):
        x1, y1, x2, y2 = map(int, map(round,self.button))
        return x1,y1
    ## ---------------------- 【认证】 一些通用方法 end --------------------------

    @property
    def button(self):
        if self._button_offset is None:
            return self._button
        else:
            return self._button_offset

    def appear_on(self, image, threshold=10):
        """Check if the button appears on the image.
          检查按钮是否出现在图像上，通过颜色检查
        Args:
            image (np.ndarray): Screenshot.
            threshold (int): Default to 10.

        Returns:
            bool: True if button appears on screenshot.
        """
        temp = crop(image, self.button, copy=False)
        image_show(temp, self.image_test)
        return color_similar(
            color1=get_color(image, self.button),
            color2=self.color,
            threshold=threshold
        )

    def load_color(self, image):
        """Load color from the specific area of the given image.
        This method is irreversible, this would be only use in some special occasion.

        Args:
            image: Another screenshot.

        Returns:
            tuple: Color (r, g, b).
        """
        self.__dict__['color'] = get_color(image, self.area)
        self.image = crop(image, self.area)
        self.__dict__['is_gif'] = False
        return self.color

    def load_offset(self, button):
        """
        Load offset from another button.

        Args:
            button (Button):
        """
        offset = np.subtract(button.button, button._button)[:2]
        self._button_offset = area_offset(self._button, offset=offset)

    def clear_offset(self):
        self._button_offset = None

    def ensure_template(self):
        """
        Load asset image.
        If needs to call self.match, call this first.
        加载资源图像,如果需要调用self.match，请先调用它。
        """
        if not self._match_init:
            if self.is_gif:
                self.image = []
                for image in imageio.mimread(self.file):
                    image = image[:, :, :3].copy() if len(image.shape) == 3 else image
                    image = crop(image, self.initial_area)
                    self.image.append(image)
            else:
                self.image = load_image(self.file, self.initial_area)
            self._match_init = True

    def ensure_binary_template(self):
        """
        Load asset image.
        If needs to call self.match, call this first.
        """
        if not self._match_binary_init:
            if self.is_gif:
                self.image_binary = []
                for image in self.image:
                    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    _, image_binary = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                    self.image_binary.append(image_binary)
            else:
                image_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                _, self.image_binary = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            self._match_binary_init = True

    def ensure_luma_template(self):
        if not self._match_luma_init:
            if self.is_gif:
                self.image_luma = []
                for image in self.image:
                    luma = rgb2luma(image)
                    self.image_luma.append(luma)
            else:
                self.image_luma = rgb2luma(self.image)
            self._match_luma_init = True

    def resource_release(self):
        super().resource_release()
        self.image = None
        self.image_binary = None
        self.image_luma = None
        self._match_init = False
        self._match_binary_init = False
        self._match_luma_init = False


    def word(self, image, text, offset=30, model=1):
        """

        :param image: 源图
        :param offset(int, tuple): Detection area offset.
        :param model(int): 匹配模式 1-模糊；2-严格
        :return:
        """
        if text == None:
            text = [self.text]
        elif isinstance(text, str):
            text = [text]
        else:
            text = np.array(text)
        if isinstance(offset, tuple):
            if len(offset) == 2:
                offset = np.array((-offset[0], -offset[1], offset[0], offset[1]))
            else:
                offset = np.array(offset)
        else:
            offset = np.array((-3, -offset, 3, offset))
        # 对图片进行剪切
        image = crop(image, offset + self.area, copy=False)
        image_show(image,self.image_test)
        # 文字识别源图 ，加参数试一试：det=False
        orc_reuslt = word_ocr.ocr(image, cls=False, bin=True)
        image_word = ''
        try:
            for idx in range(len(orc_reuslt)):
                res = orc_reuslt[idx]
                for line in res:
                    image_word = image_word + line[1][0]
        except Exception:
            return False
        # 进行匹配
        if model==1 :
            for vl in text:
                if vl in image_word:
                    return True
        elif model==2 :
            for vl in text:
                if vl == image_word:
                    return True
        else:
            return False


    def match(self, image, offset=30, threshold=0.85):
        """Detects button by template matching. To Some button, its location may not be static.
           通过模板匹配检测按钮。 对于某些按钮，其位置可能不是静态的。
        Args:
            image: Screenshot.
            offset (int, tuple): Detection area offset.  offset=(6,5,-6,-5) ==  offset=(-6,-5)
            threshold (float): 0-1. Similarity.

        Returns:
            bool.
        """
        self.ensure_template()

        if isinstance(offset, tuple):
            if len(offset) == 2:
                offset = np.array((-offset[0], -offset[1], offset[0], offset[1]))
            else:
                offset = np.array(offset)
        else:
            offset = np.array((-3, -offset, 3, offset))
        # 对图片进行剪切
        image = crop(image, offset + self.area, copy=False)
        if self.is_gif:
            for template in self.image:
                res = cv2.matchTemplate(template, image, cv2.TM_CCOEFF_NORMED)
                _, similarity, _, point = cv2.minMaxLoc(res)
                self._button_offset = area_offset(self._button, offset[:2] + np.array(point))
                if similarity > threshold:
                    return True
            return False
        else:
            # ---------- 找到self.image中与image最相似的位置，并返回相似度以及位置信息------------
            # - 使用了TM_CCOEFF_NORMED算法 对两个图片进行匹配，结果存储到res
            res = cv2.matchTemplate(self.image, image, cv2.TM_CCOEFF_NORMED)
            # 找到了res中的最大值和最小值，并返回它们的位置（point），以及最大值（similarity）。其中similarity的值范围在-1到1之间，代表的含义如下：
                # 如果相似度为1，表示找到了一个完全匹配的区域。
                # 相似度接近1表示找到了一个非常相似的区域。
                # 相似度为0表示模板与图像的匹配程度较低。
                # 负值表示模板的匹配程度比较差。
            _, similarity, _, point = cv2.minMaxLoc(res)
            self._button_offset = area_offset(self._button, offset[:2] + np.array(point))
            # image_show(self.image, self.image_test)
            image_show(image, self.image_test,similarity)
            return similarity > threshold

    def match_binary(self, image, offset=30, threshold=0.85):
        """Detects button by template matching. To Some button, its location may not be static.
           This method will apply template matching under binarization.
           通过模板匹配检测按钮。 对于某些按钮，其位置可能不是静态的。 该方法将在二值化下应用模板匹配

        Args:
            image: Screenshot.
            offset (int, tuple): Detection area offset. offset=(6,5,-6,-5) ==  offset=(-6,-5)
            threshold (float): 0-1. Similarity.

        Returns:
            bool.
        """
        self.ensure_template()
        self.ensure_binary_template()

        if isinstance(offset, tuple):
            if len(offset) == 2:
                offset = np.array((-offset[0], -offset[1], offset[0], offset[1]))
            else:
                offset = np.array(offset)
        else:
            offset = np.array((-3, -offset, 3, offset))
        image = crop(image, offset + self.area, copy=False)

        if self.is_gif:
            for template in self.image_binary:
                # graying
                image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                # binarization
                _, image_binary = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                # template matching
                res = cv2.matchTemplate(template, image_binary, cv2.TM_CCOEFF_NORMED)
                _, similarity, _, point = cv2.minMaxLoc(res)
                self._button_offset = area_offset(self._button, offset[:2] + np.array(point))
                if similarity > threshold:
                    return True
            return False
        else:
            # graying
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # binarization
            _, image_binary = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            # template matching
            res = cv2.matchTemplate(self.image_binary, image_binary, cv2.TM_CCOEFF_NORMED)
            _, similarity, _, point = cv2.minMaxLoc(res)
            self._button_offset = area_offset(self._button, offset[:2] + np.array(point))
            return similarity > threshold

    def match_luma(self, image, offset=30, threshold=0.85):
        """
        Detects button by template matching under Y channel (Luminance)
        通过Y通道（亮度）下的模板匹配来检测按钮

        Args:
            image: Screenshot.
            offset (int, tuple): Detection area offset.
            threshold (float): 0-1. Similarity.

        Returns:
            bool.
        """
        self.ensure_template()
        self.ensure_luma_template()

        if isinstance(offset, tuple):
            if len(offset) == 2:
                offset = np.array((-offset[0], -offset[1], offset[0], offset[1]))
            else:
                offset = np.array(offset)
        else:
            offset = np.array((-3, -offset, 3, offset))
        image = crop(image, offset + self.area, copy=False)
        image_show(image,self.image_test)

        if self.is_gif:
            image_luma = rgb2luma(image)
            for template in self.image_luma:
                res = cv2.matchTemplate(template, image_luma, cv2.TM_CCOEFF_NORMED)
                _, similarity, _, point = cv2.minMaxLoc(res)
                self._button_offset = area_offset(self._button, offset[:2] + np.array(point))
                if similarity > threshold:
                    return True
        else:
            image_luma = rgb2luma(image)
            res = cv2.matchTemplate(self.image_luma, image_luma, cv2.TM_CCOEFF_NORMED)
            _, similarity, _, point = cv2.minMaxLoc(res)
            self._button_offset = area_offset(self._button, offset[:2] + np.array(point))
            return similarity > threshold

    def match_appear_on(self, image, threshold=30):
        """
        Args:
            image: Screenshot.
            threshold: Default to 10.

        Returns:
            bool:
        """
        diff = np.subtract(self.button, self._button)[:2]
        area = area_offset(self.area, offset=diff)
        return color_similar(color1=get_color(image, area), color2=self.color, threshold=threshold)

    def crop(self, area, image=None, name=None):
        """
        Get a new button by relative coordinates.

        Args:
            area (tuple):
            image (np.ndarray): Screenshot. If provided, load color and image from it.
            name (str):

        Returns:
            Button:
        """
        if name is None:
            name = self.name
        new_area = area_offset(area, offset=self.area[:2])
        new_button = area_offset(area, offset=self.button[:2])
        button = Button(area=new_area, color=self.color, button=new_button, file=self.file, name=name)
        if image is not None:
            button.load_color(image)
        return button

    def move(self, vector, image=None, name=None):
        """
        Move button.

        Args:
            vector (tuple):
            image (np.ndarray): Screenshot. If provided, load color and image from it.
            name (str):

        Returns:
            Button:
        """
        if name is None:
            name = self.name
        new_area = area_offset(self.area, offset=vector)
        new_button = area_offset(self.button, offset=vector)
        button = Button(area=new_area, color=self.color, button=new_button, file=self.file, name=name)
        if image is not None:
            button.load_color(image)
        return button

    def split_server(self):
        """
        Split into 4 server specific buttons.

        Returns:
            dict[str, Button]:
        """
        out = {}
        for s in ButtonExt.VALID_SERVER:
            out[s] = Button(
                area=self.parse_property(self.raw_area, s),
                color=self.parse_property(self.raw_color, s),
                button=self.parse_property(self.raw_button, s),
                file=self.parse_property(self.raw_file, s),
                name=self.name
            )
        return out


class ButtonGrid:
    def __init__(self, origin_button, delta, grid_shape, text=None):
        """

        :param origin_button: 起点按钮
        :param delta: 按钮移动距离(x,y);x=origin_button左上角x- 下一个目标左上角x;y=origin_button左上角y - 下一个目标左上角y
        :param grid_shape: 网格大小（列，行）
        :param text: 按钮的文本内容
        """
        # 起点按钮的坐上角坐标
        self.area_origin = np.array(origin_button.area_origin())
        self.button_origin = np.array(origin_button.button_origin())
        self.delta = np.array(delta)
        self.grid_shape = np.array(grid_shape)

        # 起点按钮的基础数据
        self._text = "" if text==None else text
        self._name = origin_button.name
        self._color = origin_button.color
        self._file = origin_button.file
        self._initial_area = origin_button.initial_area
        self.area_shape = origin_button.area_size()
        self.button_shape = origin_button.button_size()

    def __getitem__(self, item):
        # item ：网格位置
        area_base = np.round(np.array(item) * self.delta + self.area_origin).astype(int)
        button_base = np.round(np.array(item) * self.delta + self.button_origin).astype(int)
        area = tuple(np.append(area_base, area_base + self.area_shape))
        button = tuple(np.append(button_base, button_base + self.button_shape))
        return Button(area=area, text=self._text, color=self._color, button=button,initial_area=self._initial_area,file=self._file, name='%s_%s_%s' % (self._name, item[0], item[1]))

    def generate(self):
        for y in range(self.grid_shape[1]):
            for x in range(self.grid_shape[0]):
                yield x, y, self[x, y]

    # 将网格展平为 list
    def buttons(self):
        return list([button for _, _, button in self.generate()])


    def gen_mask(self):
        """
        Generate a mask image to display this ButtonGrid object for debugging.

        Returns:
            PIL.Image.Image: Area in white, background in black.
        """
        image = Image.new("RGB", (1280, 720), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        for button in self.buttons:
            draw.rectangle((button.area[:2], button.button[2:]), fill=(255, 255, 255), outline=None)
        return image

    def show_mask(self):
        self.gen_mask().show()

    def save_mask(self):
        """
        Save mask to {name}.png
        """
        self.gen_mask().save(f'{self._name}.png')

