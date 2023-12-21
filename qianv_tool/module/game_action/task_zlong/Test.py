import math


def generate_circle_points(radius, start_point, num_points):
    # 计算起始点对应的角度
    start_angle = math.atan2(start_point[1], start_point[0])

    # 每个点之间的角度间隔
    angle_increment = 2 * math.pi / num_points

    # 生成点
    points = []
    for i in range(num_points):
        angle = start_angle + angle_increment * i
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points.append((x, y))

    # 添加起始点以闭合循环
    points.append(start_point)

    return points


# 圆的半径
radius = 30
# 起始点
start_point = (-25, 25)
# 生成的点数
num_points = 30

# 生成点
circle_points = generate_circle_points(radius, start_point, num_points)

# 打印点
for point in circle_points:
    print(point)

# 好的，你想要的是一个算法，它能够在圆周上输出30个等间隔的点，起始点是(-25, 25)，然后绕圆一周后回到起点。我们可以使用三角函数来计算这些点的坐标。
#
# 首先，我们需要知道圆的半径是30，所以我们可以使用圆的参数方程来计算圆周上任意一点的坐标：
#
# 复制
# x = r * cos(theta)
# y = r * sin(theta)
# 其中，r 是圆的半径，theta 是从圆的正x轴开始测量的角度（以弧度为单位）。我们可以从起始点对应的角度开始，然后计算出其他29个点的坐标。起始点(-25, 25)对应的角度可以通过反三角函数 atan2(y, x) 来计算。
#
# 下面是一个Python函数，它实现了上述算法：