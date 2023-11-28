import subprocess


def cmdExe(command):
    # 执行命令
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    # 获取输出结果
    output = result.stdout.strip()
    # 返回输出结果
    return output

# dir命令
dir_command = 'dir'

print(cmdExe(dir_command))