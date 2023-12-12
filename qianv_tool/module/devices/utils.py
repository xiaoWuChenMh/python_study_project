
##################################################################################
# sys_command ： 执行系统命令，如要执行cmd命令需将shell设置为Ture
# recv_all：将stream信息转为bytes
# remove_shell_warning: 从shell命令中移除 warnings 信息
#
#
##################################################################################
import re
import time
import socket
import random
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


print(command('dir'))