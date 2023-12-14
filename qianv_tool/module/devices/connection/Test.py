from typing import Dict
import threading
import uiautomator2 as u2

# 创建一个锁对象
lock = threading.Lock()

# 缓存u2连接
u2_devices: Dict[str, u2.Device] = {}


def get_u2( serial) -> str:
    """
     安全的获取uiautomator连接
    :param serial:
    :return:
    """
    for _ in range(3):
        try:
            # 验证连接是否可用
            u2_devices[serial]
            break
        except Exception:
            lock.acquire()
            u2_device(serial)
            lock.release()
    return u2_devices[serial]



def u2_device(serial) -> str:
    u2_devices[serial] = serial
    return serial


print(get_u2('11111'))
print(get_u2('11111'))
print(get_u2('22222'))