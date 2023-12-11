cmd = [333333,'aaaaaa']
# 检查是否为字符串，如果不是执行期内逻辑
if not isinstance(cmd, str):
    # 使用map函数将cmd列表中的元素转换为字符串，并将结果转换为列表
    cmd = list(map(str, cmd))
print(cmd)