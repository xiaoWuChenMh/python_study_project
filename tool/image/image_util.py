

def divide_image_ratio(image, rows=1,columns=1):
    """将等比切换图片
    image: 图片
    rows：行数，对应长
    columns：列数，对应宽
    """
    width, height = image.size
    tile_width = width // columns
    tile_height = height // rows

    # 创建一个列表来存储切割后的图片
    divided_images = []

    for i in range(rows):
        for j in range(columns):
            # 计算每个小图片的坐标和尺寸
            box = (j * tile_width, i * tile_height, (j + 1) * tile_width, (i + 1) * tile_height)
            # crop(left, top, right, bottom) 左上角到右下角
            divided_image = image.crop(box)
            divided_images.append(divided_image)

    return divided_images

def save_divided_images(divided_images, base_name, index=0):
    """保存切割后的图片"""
    for i, img in enumerate(divided_images, start=1):
        img.save(f"{base_name}_num_{index}_part_{i}.png")