import pytesseract
from PIL import Image

# 指定tesseract的安装路径，如果tesseract在系统PATH中则不需要
# pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'  # 适用于Windows

# 打开图片文件
image_path = 'C:/Users/'  # 图片路径
image = Image.open(image_path)

# 使用tesseract进行文字识别
text = pytesseract.image_to_string(image, lang='chi_sim+eng')  # 对于中文和英文混合的文档
text = text.replace('Takram','').replace('EN','').replace('CN','').replace('|','C')

# 打印识别的文字
print(text)