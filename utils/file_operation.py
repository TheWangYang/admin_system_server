import shutil
import os
import random
import time
import stat


# 判断文件路径是否存在的方法
def ensure_dir_exists(file_dir):
    return os.path.exists(file_dir)


# 设置复制文件，并重新命名的方法
def copy_file(file_dir, save_dir, new_file_name):
    # 确定路径存在
    if ensure_dir_exists(file_dir) and ensure_dir_exists(save_dir):
        path_dir = os.listdir(file_dir)
        # 随便得到一张图片
        sample_pictures = random.sample(path_dir, 1)  # 随机从现存的图像文件夹中选取1张图片
        for old_name in sample_pictures:
            shutil.copy(file_dir + old_name, save_dir + new_file_name)
        # 返回新的图片位置
        return save_dir + new_file_name, str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    else:
        return "error"


# 设置的根据路径删除文件的函数
def delete_file(file_path):
    try:
        if ensure_dir_exists(file_path):
            os.chmod(file_path, 0o777)
            os.remove(file_path)
            return "success"
        else:
            return "failed"
    except Exception as e:
        print("delete_file inner error : ", e)
        print(f'error file:{e.__traceback__.tb_frame.f_globals["__file__"]}')
        print(f"error line:{e.__traceback__.tb_lineno}")
        return "error"
