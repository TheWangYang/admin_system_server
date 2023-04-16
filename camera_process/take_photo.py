from utils import copy_file
from PIL import Image
from PIL import ImageFile

Image.MAX_IMAGE_PIXELS = 309715200
from utils import PROJECT_PATH
from utils import PATH_SUFFIX
from utils import PATH_NEW_PICTURE_SUFFIX
from .image_device_client import take_a_photo_from_image_device
import time


def get_photo(user_id, picture_last_key, user_name):
    try:
        # 得到新拍摄图片名，设置为当前数据库中存在的图片的最后一个主键值+1
        picture_last_key += 1
        new_file_name = str(user_id) + "_" + str(picture_last_key) + ".jpg"
        # 调用底层拍摄图片接口得到图片，这里首先使用file文件操作模拟
        file_dir = PATH_NEW_PICTURE_SUFFIX  # server_abs_path() + PATH_NEW_PICTURE_SUFFIX
        save_dir = PROJECT_PATH + PATH_SUFFIX
        # 调用图片拍摄接口拍摄得到的一张图片
        # receive_data = take_a_photo_from_image_device()
        receive_data = "OK!"
        print("receive_data: {}".format(receive_data))
        if receive_data == "OK!":  # 请求拍摄成功，等待前端拍摄完毕
            # 设置time等待5s时间，等待前端拍摄完成
            print("[INFO] taking picture begin")
            time.sleep(5)
            print("[INFO] taking picture end")
            # 保存生成的新图片到相应文件目录中
            new_file_path, created_time = copy_file(file_dir, save_dir, new_file_name)
            if new_file_path != "error":
                img = Image.open(new_file_path)
                img_size = img.size  # 大小/尺寸
                img_width = img.width
                img_height = img.height
                img_format = img.format
                # 创建新的图片对象
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
                    'result_path': "",
                    'shooting_environment': "",
                    'shooting_direction': "",
                    'shooting_quality': "",
                    'is_detection': "否"
                }
                return new_picture_obj
            else:
                return {}
        else:  # 图片拍摄失败
            return {}
    except Exception as e:
        print("get_photo inner error : ", e)
        print(f'error file:{e.__traceback__.tb_frame.f_globals["__file__"]}')
        print(f"error line:{e.__traceback__.tb_lineno}")
        return {}
