import os

from paddleocr import PaddleOCR

import imageio
import numpy as np
from tqdm.contrib.concurrent import process_map

from qianv_tool.module.logger import logger
from qianv_tool.module.base.utils import get_bbox, get_color, image_size, load_image
from qianv_tool.config.exe_config  import ExecuteConfig as ButtonExt

ButtonExt.IMPORT_EXP = """
from qianv_tool.module.base.button import Button
from qianv_tool.module.base.template import Template

# This file was automatically generated by dev_tools/button_extract.py.
# Don't modify it manually.
"""
ButtonExt.IMPORT_EXP = ButtonExt.IMPORT_EXP.strip().split('\n') + ['']

ocr = PaddleOCR(use_angle_cls=True, lang="ch")

class ImageExtractor:
    def __init__(self, module, file):
        """
        Args:
            module(str): 图片资源所在的父级文件名
            file(str): 图片资源的名字，xxx.png or xxx.gif
        """
        self.module = module
        # 文件名 和 后缀
        self.name, self.ext = os.path.splitext(file)
        # 初始化 按钮模块对象的属性
        self.area, self.color, self.button, self.file, self.text = {}, {}, {}, {}, {}
        # 加载 图片资源，并获取模块对象的真实属性
        self.load(ButtonExt.ASSETS_GAME_FOLDER)
        # need to run only once to download and load model into memory


    def get_file(self, genre='', server=ButtonExt.ASSETS_GAME_FOLDER):
        """
        获取图片资源的文件地址
        :param genre:
        :param server:
        :return:
        """
        for ext in ['.png', '.gif']:
            file = f'{self.name}.{genre}{ext}' if genre else f'{self.name}{ext}'
            file = os.path.join(ButtonExt.ASSETS_FOLDER, server, self.module, file).replace('\\', '/')
            if os.path.exists(file):
                return file

        ext = '.png'
        file = f'{self.name}.{genre}{ext}' if genre else f'{self.name}{ext}'
        file = os.path.join(ButtonExt.ASSETS_FOLDER, server, self.module, file).replace('\\', '/')
        return file

    def extract(self, file):
        """
         从图片资源中提取按钮模块对象的属性
        :param file:
        :return:
        """
        if os.path.splitext(file)[1] == '.gif':
            # In a gif Button, use the first image.
            bbox = None
            mean = None
            # 遍历使用 imageio.mimread(file) 读取的 GIF 的每一帧图像：
            # 详解：imageio.mimread 可以将 GIF 文件或类似的动态图像文件读取为一个包含各帧图像数据的列表，让你可以对每一帧进行处理或者将其作为视频进行播放
            for image in imageio.mimread(file):
                # 检查每一帧的维度，如果它是一个三维数组（代表彩色图像），则将其切片为只包含前三个通道的图像数据。如果它是一个二维数组（代表灰度图像），则不作任何处理。
                # 作用：确保所有帧的图像数据都是彩色图像，并消除了可能存在的透明度通道或其他额外通道的情况。
                image = image[:, :, :3] if len(image.shape) == 3 else image
                new_bbox, new_mean = self._extract(image, file)
                if bbox is None:
                    bbox = new_bbox
                elif bbox != new_bbox:
                    logger.warning(f'{file} has multiple different bbox, this will cause unexpected behaviour')
                if mean is None:
                    mean = new_mean
            return bbox, mean,''
        else:
            image = load_image(file)
            text = self.get_word(image)
            bbox, mean = self._extract(image, file)
            return bbox, mean, text

    def get_word(self,image):
        text = ""
        result = ocr.ocr(image, cls=True)
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                text = text+line[1][0]
        return text

    @staticmethod
    def _extract(image, file):
        size = image_size(image)
        if size != (1280, 720):
            logger.warning(f'{file} has wrong resolution: {size}')
        # 获取识别区域的坐标：
        bbox = get_bbox(image)
        # 获取颜色RGB
        mean = get_color(image=image, area=bbox)
        mean = tuple(np.rint(mean).astype(int))
        return bbox, mean

    def load(self, server=ButtonExt.ASSETS_GAME_FOLDER):
        file = self.get_file(server=server)
        if os.path.exists(file):
            area, color, text = self.extract(file)
            # 默认按钮点击区域 和 按钮识别区域相同
            button = area
            # 判断是否需要修正识别区域
            override = self.get_file('AREA', server=server)
            if os.path.exists(override):
                area, _, _ = self.extract(override)
            # 判断是否需要修正颜色
            override = self.get_file('COLOR', server=server)
            if os.path.exists(override):
                _, color, _ = self.extract(override)
            # 判断是否需要修正按钮点击区域
            override = self.get_file('BUTTON', server=server)
            if os.path.exists(override):
                button, _, _ = self.extract(override)
            # ----------- 获取:最终的坐标和颜色值 -----------------
            # 按钮识别的区域
            self.area[server] = area
            # 按钮的颜色
            self.color[server] = color
            # 按钮出现后的点击区域
            self.button[server] = button
            # 图片资源的相对位置
            self.file[server] = file
            # 图片上的文字
            self.text[server] = text
        else:
            logger.attr(server, f'{self.name} not found, use server assets')
            self.area[server] = self.area[ButtonExt.ASSETS_GAME_FOLDER]
            self.color[server] = self.color[ButtonExt.ASSETS_GAME_FOLDER]
            self.button[server] = self.button[ButtonExt.ASSETS_GAME_FOLDER]
            self.file[server] = self.file[ButtonExt.ASSETS_GAME_FOLDER]
            self.text[server]= self.file[ButtonExt.ASSETS_GAME_FOLDER]



    @property
    def expression(self):
        return '%s = Button(area=%s,text=%s, color=%s, button=%s, file=%s)' % (
            self.name, self.area, self.text, self.color, self.button, self.file)


class TemplateExtractor(ImageExtractor):

    @staticmethod
    def extract(file):
        image = load_image(file)
        bbox = get_bbox(image)
        mean = get_color(image=image, area=bbox)
        mean = tuple(np.rint(mean).astype(int))
        return bbox, mean

    @property
    def expression(self):
        return '%s = Template(file=%s)' % (
            self.name, self.file)
        # return '%s = Template(area=%s, color=%s, button=%s, file=\'%s\')' % (
        #     self.name, self.area, self.color, self.button,
        #     self.config.ButtonExt.ASSETS_FOLDER + '/' + self.module + '/' + self.name + '.png')


# class OcrExtractor(ImageExtractor):
#     @property
#     def expression(self):
#         return '%s = OcrArea(area=%s, color=%s, button=%s, file=\'%s\')' % (
#             self.name, self.area, self.color, self.button,
#             self.config.ButtonExt.ASSETS_FOLDER + '/' + self.module + '/' + self.name + '.png')


class ModuleExtractor:
    def __init__(self, name):
        # name：图片资源所在的父级文件名
        self.name = name
        # 获取图片资源的全路径
        self.folder = os.path.join(ButtonExt.ASSETS_FOLDER, ButtonExt.ASSETS_GAME_FOLDER, name)

    @staticmethod
    def split(file):
        name, ext = os.path.splitext(file)
        name, sub = os.path.splitext(name)
        return name, sub, ext

    def is_base_image(self, file):
        _, sub, _ = self.split(file)
        return sub == ''

    @property
    def expression(self):
        exp = []
        for file in os.listdir(self.folder):
            # 图片资源的文件路径，全部是数字就跳过
            if file[0].isdigit():
                continue
            # 图片资源的文件路径已（TEMPLATE_）开头，需要特殊处理
            if file.startswith('TEMPLATE_'):
                exp.append(TemplateExtractor(module=self.name, file=file).expression)
                continue
            # if file.startswith('OCR_'):
            #     exp.append(OcrExtractor(module=self.name, file=file, config=self.config).expression)
            #     continue
            # 图片资源是一个Button
            if self.is_base_image(file):
                # 获取模块对象的属性，并通过expression函数，转化为恰当的格式。
                exp.append(ImageExtractor(module=self.name, file=file).expression)
                continue

        logger.info('Module: %s(%s)' % (self.name, len(exp)))
        exp = ButtonExt.IMPORT_EXP + exp
        return exp

    def write(self):
        # 拼接动作解析文件全路径
        folder = os.path.join(ButtonExt.MODULE_FOLDER, self.name)
        # 该路径不存在就创建
        if not os.path.exists(folder):
            os.mkdir(folder)
        # 将动作解析内容写入文件assets.py 中
        with open(os.path.join(folder, ButtonExt.BUTTON_FILE), 'w', newline='',encoding='utf-8') as f:
            # 获取按钮模块对象的内容（expression） 并 写入文件assets.py中
            for text in self.expression:
                f.write(text + '\n')


def worker(module):
    me = ModuleExtractor(name=module)
    me.write()


class AssetExtractor:
    """
    Extract Asset to asset.py.
    All the filename of assets should be in uppercase.

    Asset name starts with digit will be ignore.
        E.g. 2020XXXX.png.
    Asset name starts with 'TEMPLATE_' will treat as template.
        E.g. TEMPLATE_AMBUSH_EVADE_SUCCESS.png
             > TEMPLATE_AMBUSH_EVADE_SUCCESS = Template(file='./assets/handler/TEMPLATE_AMBUSH_EVADE_SUCCESS.png')
    Asset name starts other will treat as button.
        E.g. GET_MISSION.png
             > Button(area=(553, 482, 727, 539), color=(93, 142, 203), button=(553, 482, 727, 539), name='GET_MISSION')
    Asset name like XXX.AREA.png, XXX.COLOR.png, XXX.BUTTON.png, will overwrite the attribute of XXX.png.
        E.g. BATTLE_STATUS_S.BUTTON.png overwrites the attribute 'button' of BATTLE_STATUS_S
    Asset name starts with 'OCR_' will be treat as button.
        E.g. OCR_EXERCISE_TIMES.png.
    """

    def __init__(self):
        logger.info('Assets extract')
        # 1、定位到资源文件下的game目录(assets/game)；2、同时遍历判断该目录下的‘存在’是不是文件夹，如果是就放入到容器（modules）中
        modules = [m for m in os.listdir(ButtonExt.ASSETS_FOLDER + '/' + ButtonExt.ASSETS_GAME_FOLDER)
                   if os.path.isdir(os.path.join(ButtonExt.ASSETS_FOLDER + '/' + ButtonExt.ASSETS_GAME_FOLDER, m))]
        # 启动一个进程，并执行指定的函数（worker）；modules：作为函数输入的可迭代对象。
        #  process_map会将这个迭代对象中的每个元素作为参数传递给指定的函数，并在多个进程中并行执行这个函数。
        process_map(worker, modules)


if __name__ == '__main__':
    ae = AssetExtractor()
