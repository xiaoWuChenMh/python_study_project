import uiautomator2 as u2
import numpy as np
import cv2
# 链接设备
# a = u2.connect('emulator-5554')
# print(a.info)
d = u2.connect('emulator-5556')
print(d.info)
# c = u2.connect('emulator-5558')
# print(c.info)
# d = u2.connect('emulator-5560')
# print(d.info)
# 输出设备信息



# 截图
# a.screenshot('image/他人申请队长.png')
# d.screenshot('image/home2.png')
# c.screenshot('image/home3.png')
# d.screenshot('image/继续登录.png')

def get_device() -> u2.Device:
    # if self.is_over_http:
    #     # Using uiautomator2_http
    #     device = u2.connect(self.serial)
    # else:
    #     # Normal uiautomator2
    #     if self.serial.startswith('emulator-') or self.serial.startswith('127.0.0.1:'):
    #         device = u2.connect_usb(self.serial)
    #     else:
    #         device = u2.connect(self.serial)
    #
    # # Stay alive
    # device.set_new_command_timeout(604800)
    #
    # logger.attr('u2.Device', f'Device(atx_agent_url={device._get_atx_agent_url()})')
    device = u2.connect('emulator-5554')
    return device

# 截图并对图片进行前期处理
def screenshot_uiautomator2():
    device = get_device()
    image = device.screenshot(format='raw')
    # 这行代码将输入的"image"数据读入一个类型为np.uint8的NumPy数组中。
    image = np.frombuffer(image, np.uint8)
    # 这个条件语句确保如果从缓冲区中读取的图像数据为空，就会引发一个"ImageTruncated"异常。
    if image is None:
        raise ImageTruncated('Empty image after reading from buffer')
    else:
        image_show(image)
    # 这里使用了OpenCV的imdecode函数来对图像数据进行解码。标志cv2.IMREAD_COLOR表示应该以彩色方式加载图像
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    #  如果解码后的图像为空，此条件语句会引发一个"ImageTruncated"异常。
    if image is None:
        raise ImageTruncated('Empty image after cv2.imdecode')
    else:
        image_show(image)
    # 这行代码使用OpenCV的cvtColor函数将图像的颜色空间从BGR转换为RGB。
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # 类似于之前的检查，此条件语句确保如果颜色转换后图像为空，会引发一个"ImageTruncated"异常。
    if image is None:
        raise ImageTruncated('Empty image after cv2.cvtColor')
    else:
        image_show(image)
    # 可选： 对 mage进行去噪处理。函数的参数包括输入图像、输出图像、以及一些去噪的参数
      # h: 决定过滤器强度。较大的值可以更好地去除噪声，但也可能删除图像细节
      # templateWindowSize : 用于计算像素权重的邻域大小。较大的值将考虑更广泛的邻域。
        # 更大的像素范围，意味着计算每个像素的权重中将该点像素周围更多的像素纳入算法的计算范围，会得到更多细节，使噪声的影响减小，保留了更多的图像细节和结构信息。
      # searchWindowSize ：  用于查找相似像素的邻域大小。较大的值将考虑更广泛的邻域以寻找相似的像素
    cv2.fastNlMeansDenoising(image, image, h=17, templateWindowSize=1, searchWindowSize=2)
    image_show(image)
    # 如果所有操作都成功，就会返回修改后的图像。
    return image

# 显示图像
def image_show(image):
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()





class ImageTruncated(Exception):
    pass

# 获取图像大小：用于检查屏幕（图像）的大小，其尺寸必须为1280x720。
def image_size(image):
    """
    Args:
        image (np.ndarray):

    Returns:
        int, int: width, height
    """
    shape = image.shape
    return shape[1], shape[0]

# screenshot_uiautomator2()