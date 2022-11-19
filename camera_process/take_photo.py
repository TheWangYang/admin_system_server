from utils import copy_file
from PIL import Image
from utils import server_abs_path
from utils import PATH_SUFFIX


def get_photo(user_id, picture_num, user_name):
    try:
        # 得到新拍摄图片名
        picture_num += 1
        new_file_name = str(user_id) + "_" + str(picture_num) + ".jpg"
        # 调用底层拍摄图片接口得到图片，这里首先使用file文件操作模拟
        file_dir = server_abs_path() + PATH_SUFFIX
        save_dir = server_abs_path() + PATH_SUFFIX
        print("server_abs_path() : ", server_abs_path())
        print(file_dir)
        print(save_dir)
        # 新图片已经生成并保存到相应文件目录中
        new_file_path, created_time = copy_file(file_dir, save_dir, new_file_name)
        if new_file_path != "error":
            img = Image.open(new_file_path)
            img_size = img.size  # 大小/尺寸
            img_width = img.width
            img_height = img.height
            img_format = img.format
            new_picture_obj = {
                'picture_name': new_file_name,
                'created_time': created_time,
                'update_time': created_time,
                'picture_width': img_width,
                'picture_height': img_height,
                'picture_size': img_size,
                'picture_format': img_format,
                'uploader_id': user_id,
                'uploader_name': user_name,
                'description': "默认图片描述",
                'is_test': "否",
                'save_path': PATH_SUFFIX + new_file_name,
                'result_path': ""
            }
            return new_picture_obj
        else:
            return {}
    except Exception as e:
        print("get_photo inner error : ", e)
        print(f'error file:{e.__traceback__.tb_frame.f_globals["__file__"]}')
        print(f"error line:{e.__traceback__.tb_lineno}")
        return {}