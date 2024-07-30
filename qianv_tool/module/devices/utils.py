
##################################################################################
# sys_command ： 执行系统命令，如要执行cmd命令需将shell设置为Ture
# recv_all：将stream信息转为bytes
# remove_shell_warning: 从shell命令中移除 warnings 信息
#
#
##################################################################################
import cv2
import math
import time
import socket
import numpy as np
from adbutils import AdbTimeout
from qianv_tool.module.logger import logger

try:
    # adbutils 0.x
    from adbutils import _AdbStreamConnection as AdbConnection
except ImportError:
    # adbutils >= 1.0
    from adbutils import AdbConnection
    # Patch list2cmdline back to subprocess.list2cmdline
    # We expect `screencap | nc 192.168.0.1 20298` instead of `screencap '|' nc 192.168.80.1 20298`
    import adbutils
    import subprocess



def is_emulator(serial):
    """
    # 判断是否为emulator
    :param serial:
    :return:
    """
    return serial.startswith('emulator-') or serial.startswith('127.0.0.1:')

def retry_sleep(trial=None):
    """
     重试时，系统睡眠时间
    :param trial:
    :return:
    """
    if trial == 0:
        pass
    elif trial == 1:
        pass
    # Failed twice
    elif trial == 2:
        time.sleep(1)
    # Failed more
    else:
        time.sleep(3)



def sys_command(cmd, timeout=10,shell=False):
    """
    执行cmd命令
    Args:
        cmd (list): 要执行的命令，可以是一个字符串或一个包含命令及其参数的列表。
        timeout (int):超时时间
        shell:默认为False，不通过shell；如果想要执行cmd命令需要将其设置为True

    Returns:
        str:
    """
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=shell,text=True)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.terminate() #结束进程
        stdout, stderr = process.communicate()
        logger.warning(f'TimeoutExpired when calling {cmd}, stdout={stdout}, stderr={stderr}')
    finally:
        if process:
            process.terminate()
    return stdout


# ------------------------------- 错误处理 --------------------------------------------------------

def handle_adb_error(e):
    """
    Args:
        e (Exception):

    Returns:
        bool: If should retry
    """
    text = str(e)
    if 'not found' in text:
        # When you call `adb disconnect <serial>`
        # Or when adb server was killed (low possibility)
        # AdbError(device '127.0.0.1:59865' not found)
        logger.error(e)
        return True
    elif 'timeout' in text:
        # AdbTimeout(adb read timeout)
        logger.error(e)
        return True
    elif 'closed' in text:
        # AdbError(closed)
        # Usually after AdbTimeout(adb read timeout)
        # Disconnect and re-connect should fix this.
        logger.error(e)
        return True
    elif 'device offline' in text:
        # AdbError(device offline)
        # When a device that has been connected wirelessly is disconnected passively,
        # it does not disappear from the adb device list,
        # but will be displayed as offline.
        # In many cases, such as disconnection and recovery caused by network fluctuations,
        # or after VMOS reboot when running Alas on a phone,
        # the device is still available, but it needs to be disconnected and re-connected.
        logger.error(e)
        return True
    elif 'is offline' in text:
        # RuntimeError: USB device 127.0.0.1:7555 is offline
        # Raised by uiautomator2 when current adb service is killed by another version of adb service.
        logger.error(e)
        return True
    elif 'unknown host service' in text:
        # AdbError(unknown host service)
        # Another version of ADB service started, current ADB service has been killed.
        # Usually because user opened a Chinese emulator, which uses ADB from the Stone Age.
        logger.error(e)
        return True
    else:
        # AdbError()
        logger.exception(e)
        possible_reasons(
            'If you are using BlueStacks or LD player or WSA, please enable ADB in the settings of your emulator',
            'Emulator died, please restart emulator',
            'Serial incorrect, no such device exists or emulator is not running'
        )
        return False

def possible_reasons(*args):
    """
    Show possible reasons

        Possible reason #1: <reason_1>
        Possible reason #2: <reason_2>
    """
    for index, reason in enumerate(args):
        index += 1
        logger.critical(f'Possible reason #{index}: {reason}')


## -------------------------------- adb shell输出处理 -------------------------------

def recv_all(stream, chunk_size=4096, recv_interval=0.000) -> bytes:
    """
    将流信息转为Bytes
    Args:
        stream:
        chunk_size:
        recv_interval (float): Default to 0.000, use 0.001 if receiving as server

    Returns:
        bytes:

    Raises:
        AdbTimeout
    """
    if isinstance(stream, AdbConnection):
        stream = stream.conn
        stream.settimeout(10)
    else:
        stream.settimeout(10)

    try:
        fragments = []
        while 1:
            chunk = stream.recv(chunk_size)
            if chunk:
                fragments.append(chunk)
                # See https://stackoverflow.com/questions/23837827/python-server-program-has-high-cpu-usage/41749820#41749820
                time.sleep(recv_interval)
            else:
                break
        return remove_shell_warning(b''.join(fragments))
    except socket.timeout:
        raise AdbTimeout('adb read timeout')

def remove_shell_warning(s):
    """
     从shell命令中移除 warnings 信息

    Args:
        s (str, bytes):

    Returns:
        str, bytes:
    """
    # WARNING: linker: [vdso]: unused DT entry: type 0x70000001 arg 0x0\n\x89PNG\r\n\x1a\n\x00\x00\x00\rIH
    if isinstance(s, bytes):
        # b''b代表是一个以字节的形式存在的字符串
        if s.startswith(b'WARNING'):
            try:
                s = s.split(b'\n', maxsplit=1)[1]
            except IndexError:
                pass
        return s
        # return re.sub(b'^WARNING.+\n', b'', s)
    elif isinstance(s, str):
        if s.startswith('WARNING'):
            try:
                s = s.split('\n', maxsplit=1)[1]
            except IndexError:
                pass
    return s


## -------------------------------- 图像相关 -------------------------------

# 显示图像
def image_show(image,test=False):
    if(test):
        cv2.imshow('Image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


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

## ------------------------------------ 坐标处理 -----------------------------

def random_normal_distribution_int(a, b, n=3):
    """Generate a normal distribution int within the interval. Use the average value of several random numbers to
    simulate normal distribution.

    Args:
        a (int): The minimum of the interval.
        b (int): The maximum of the interval.
        n (int): The amount of numbers in simulation. Default to 3.

    Returns:
        int
    """
    if a < b:
        output = np.mean(np.random.randint(a, b, size=n))
        return int(output.round())
    else:
        return b

def random_rectangle_point(area, n=3):
    """Choose a random point in an area.

    Args:
        area: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).
        n (int): The amount of numbers in simulation. Default to 3.

    Returns:
        tuple(int): (x, y)
    """
    x = random_normal_distribution_int(area[0], area[2], n=n)
    y = random_normal_distribution_int(area[1], area[3], n=n)
    return x, y


def ensure_int(*args):
    """
    Convert all elements to int.
    Return the same structure as nested objects.

    Args:
        *args:

    Returns:
        list:
    """

    def to_int(item):
        try:
            return int(item)
        except TypeError:
            result = [to_int(i) for i in item]
            if len(result) == 1:
                result = result[0]
            return result

    return to_int(args)

def point2str(x, y, length=4):
    """
    Args:
        x (int, float):
        y (int, float):
        length (int): Align length.

    Returns:
        str: String with numbers right aligned, such as '( 100,  80)'.
    """
    return '(%s, %s)' % (str(int(x)).rjust(length), str(int(y)).rjust(length))


def generate_circle_points(center=(100, 200), radius=30, start_point=(130, 230), num_points=30 ):
        """
        根据给定的圆心和起始点生成一系列的绕圆一周的坐标点，最后会回到起始点
        这个函数首先计算起始点对应的角度，然后计算每个点之间的角度间隔。接着，它在循环中生成每个点的坐标，并将它们添加到列表中。
        最后，它将起始点添加到列表的末尾，以便闭合圆周
        :param center: 圆心坐标
        :param radius: 圆的半径
        :param start_point: 起始点
        :param num_points: 30
        :return:
        """
        # 将起始点转换为相对于圆心的坐标
        start_point_relative = (start_point[0] - center[0], start_point[1] - center[1])

        # 计算起始点相对于圆心的角度
        start_angle = math.atan2(start_point_relative[1], start_point_relative[0])

        # 每个点之间的角度间隔
        angle_increment = 2 * math.pi / num_points

        # 生成点
        points = []
        for i in range(num_points):
            angle = start_angle + angle_increment * i
            x_relative = radius * math.cos(angle)
            y_relative = radius * math.sin(angle)
            # 将相对于圆心的坐标转换回原始坐标系
            x = math.ceil(x_relative + center[0])
            y = math.ceil(y_relative + center[1])
            points.append((x, y))

        # 添加起始点以闭合循环
        points.append(start_point)

        return points

