
import os
import glob
import shutil

class ImageTool:
    def __init__( self):
        pass

    def change_image_extension(self, folder_path, old_ext, new_ext ):
        """
        修改指定文件夹下图片的后缀名
        """
        # 获取指定文件夹下的所有图片文件
        image_files = glob.glob(os.path.join(folder_path, f'*.{old_ext}'))

        for file in image_files:
            # 构造新的文件名
            new_file = os.path.splitext(file)[0] + '.' + new_ext
            # 重命名并保存文件
            shutil.move(file, new_file)

    def parent_directory( self ):
        """
         获取当前文件的父目录
        """
        current_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.dirname(current_dir)

    def change_game_source( self ):
        """
        修改assets/game_source文件下图片的后缀名
        """
        parent_dir = self.parent_directory()
        image_path = os.path.join(parent_dir, "assets/game_source")
        self.change_image_extension(image_path, 'png', 'jpg')

if __name__ == "__main__":
    app = ImageTool()
    app.change_game_source()

