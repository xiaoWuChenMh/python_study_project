
# 代码执行过程中用到的配置
class ExecuteConfig:

    """
     任务标识符号
    """
    # 一条龙任务的标识
    TASK_TAG__LONG = "long_task_tag"
    # 师门任务的标识
    TASK_TAG__SHI_MEN = "shi_men_task_tag"

    """
     图片资源转按钮模块对象
    """
    # 图片资源转换为按钮模块对象后存储的位置
    MODULE_FOLDER = './module/game_action'
    # 按钮模块对象的文件命名
    BUTTON_FILE = 'assets.py'
    # 资源文件夹
    ASSETS_FOLDER = './assets'
    # 有效的服务，默认是game
    VALID_SERVER = ['game']
    # 游戏中图片资源的父目录,按钮模块对象属性中的标识也是这个,默认是game 和 VALID_SERVER和对应
    ASSETS_GAME_FOLDER = 'game'