import subprocess
import uiautomator2
# 环境初始化

def cmdExe(command):
    # 执行命令
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    # 获取输出结果
    output = result.stdout.strip()
    # 返回输出结果
    return output

# 以下命令都需要管理员身份运行pyCharm，才能在pyCharm中执行改代码！！！

# ADB命令：发现设备
adb_command = 'adb devices -l'

# 设备安装 atx-agent
init_uiautomator_command = 'python -m uiautomator2 init'

print(cmdExe(adb_command))
# print(cmdExe(init_uiautomator_command))

