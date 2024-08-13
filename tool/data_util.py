from datetime import datetime, timedelta
# 指定日期加上指定月份后的日期
def add_months(date_str, months=1):
    # 检查输入类型，如果是整数，则转换为字符串
    if isinstance(date_str, int):
        date_str = str(date_str)

    # 将字符串日期转换为datetime对象
    date_format = "%Y%m%d"
    current_date = datetime.strptime(date_str, date_format)
    
    # 计算增加月份后的年份和月份
    new_month = current_date.month + months
    year = current_date.year + (new_month - 1) // 12
    month = (new_month - 1) % 12 + 1
    
    # 尝试构建增加月份后的日期对象，保持日不变
    try:
        new_date = datetime(year, month, current_date.day)
    except ValueError:
        # 如果当前日在新的月份不存在（例如2月没有30号），则使用该月的最后一天
        # 设置月份的最后一天，需要先设置到下个月的第一天，然后回退一天
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)
        new_date = next_month - timedelta(days=1)

    # 将结果日期转换回字符串格式
    return new_date.strftime(date_format)


# 指定日期加上指定天数后的日期
def date_add(date_str, days):
    # 检查输入类型，如果是整数，则转换为字符串
    if isinstance(date_str, int):
        date_str = str(date_str)

    # 将字符串日期转换为datetime对象
    date_format = "%Y%m%d"
    current_date = datetime.strptime(date_str, date_format)
    
    # 增加指定的天数
    new_date = current_date + timedelta(days=days)
    
    # 将结果日期转换回字符串格式
    return int(new_date.strftime(date_format))


#日期格式化
def format_date(date_str,date_format="%Y%m%d",new_date_format="%Y-%m-%d"):
    # 检查输入类型，如果是整数，则转换为字符串
    if isinstance(date_str, int):
        date_str = str(date_str)
        
    # 解析日期字符串
    date_obj = datetime.strptime(date_str,date_format)
    
    # 重新格式化日期为所需格式
    formatted_date = date_obj.strftime(new_date_format)
    
    return formatted_date

# 示例使用
input_date = 20240701
# result_date = add_months(input_date,7)
result_date = date_add(input_date,24)
# result_date = format_date(input_date)
print("Next month date:", result_date)