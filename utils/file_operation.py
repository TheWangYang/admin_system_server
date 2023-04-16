import shutil
import os
import time
import cv2
import numpy as np
from .constant import TEMP_IMAGES
from .constant import PROJECT_PATH


# 判断文件路径是否存在的方法
def ensure_dir_exists(file_dir):
    return os.path.exists(file_dir)


# 设置复制文件，并重新命名的方法
def copy_file(file_dir, save_dir, new_file_name):
    # 确定路径存在
    if ensure_dir_exists(file_dir) and ensure_dir_exists(save_dir):
        # 得到目录下的所有文件和文件夹
        images_name_list = os.listdir(file_dir)
        # 对图片路径进行排序(参考拍摄日期)
        images_name_list.sort(key=lambda x: int(x[6:-4]))
        # images_name_list_test = [images_name_list[1]]
        # 设置保存图片对象的list数组
        images_list = []
        # 保存当前图片的patches到tmp的save_dir+new_file_name文件夹下面
        patches_tmp_name = new_file_name[:-4]
        print("new_file_name: {}".format(new_file_name))
        print("patches_tmp_name: {}".format(patches_tmp_name))
        # 创建对应的文件夹
        tmp_path = PROJECT_PATH + TEMP_IMAGES + patches_tmp_name + "/"
        if not os.path.exists(tmp_path):
            os.mkdir(tmp_path)
        for name in images_name_list:
            # 读取图片
            curr_img = cv2.imdecode(np.fromfile(os.path.join(file_dir, name), dtype=np.uint8), -1)
            images_list.append(curr_img)
            # 将当前图片包含的所有patches复制到对应的tmp文件夹下面
            cv2.imwrite(os.path.join(tmp_path, name), curr_img)
        # 进行图片纵向拼接
        image_vertical = np.vstack(images_list)
        # 保存拼接图片到todo文件夹
        cv2.imwrite(save_dir + new_file_name, image_vertical)
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
