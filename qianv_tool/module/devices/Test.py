import subprocess

# 使用capture_output=True执行命令
process_capture = subprocess.Popen('echo Hello, World!', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
output_capture, error_capture = process_capture.communicate()
print(output_capture)  # 输出：Hello, World!
print(error_capture)  # 输出：空字符串

# 使用capture_output=False执行命令
process_no_capture = subprocess.Popen('echo Hello, World!', shell=True, text=True)
output_capture1, error_capture1 = process_no_capture.communicate()  # 不捕获输出

print(output_capture1)  # 输出：None
print(error_capture1)  # 输出：None

# 获取子进程的输出
output_no_capture = process_no_capture.stdout.read().decode()
print(output_no_capture)  # 输出：Hello, World!