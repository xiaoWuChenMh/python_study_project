import math
import matplotlib
matplotlib.use('TkAgg')  # 在导入 pyplot 之前设置后端
import matplotlib.pyplot as plt

def generate_circle_points(center=(100, 200), radius=30, start_point=(130, 230), num_points=30):
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

    # 每个点之间的角度间隔，顺时针生成点
    angle_increment = 2 * math.pi / num_points

    # 每个点之间的角度间隔，使用负值来逆时针生成点
    # angle_increment = -2 * math.pi / num_points


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

def show_circle(center,radius,circle_points):
    """
    根据给定信息绘制圆，并显示
    :param center: 圆心坐标
    :param radius: 圆的半径
    :param circle_points: 绕圆一周的一系列的点
    :return:
    """
    # 绘制圆形和点
    fig, ax = plt.subplots()
    circle = plt.Circle(center, radius, color='blue', fill=False)
    ax.add_artist(circle)

    # 绘制生成的点
    x_points = [point[0] for point in circle_points]
    y_points = [point[1] for point in circle_points]
    ax.plot(x_points, y_points, 'ro')  # 'ro' 表示红色的圆点

    # 设置图表的标题和坐标轴标签
    ax.set_title('Circle with Points')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    # 设置坐标轴的范围
    ax.set_xlim([center[0] - radius - 10, center[0] + radius + 10])
    ax.set_ylim([center[1] - radius - 10, center[1] + radius + 10])

    # 保持纵横比例
    ax.set_aspect('equal', 'box')

    # 显示图表
    plt.show()

# 圆心坐标
center = (794.2857142857142, 360.0)
# 圆的半径
radius = 154.28571428571428
# 起点
start_point = (640.0, 360.0)
# 生成点
circle_points = generate_circle_points(center=center, start_point=(640.0, 360.0),radius = radius)
# 绘制圆
show_circle(center,radius,circle_points)

