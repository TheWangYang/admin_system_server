import sys

SERVER_PREFIX = "http://127.0.0.1:8001"
PATH_SUFFIX = "/static/images/todo/"
PATH_NEW_PICTURE_SUFFIX = "D:/pycharm_work_place/admin_system_server_v2/static/images/database"
TEMP_IMAGES = "/static/images/tmp/"  # 用来保存发动机表面的patch图片集
TEMP_IMAGES_RESULT = "/static/images/tmp_result/"
PROJECT_PATH = "D:/pycharm_work_place/admin_system_server_v2"


# D:\\pycharm_work_place\\detection_parameters\\images
# C:\\Users\\wyysu\\MVS\\Data\\MV-CL086-91GC (K78947478)\\
# /static/images/database/


def server_abs_path():
    path = sys.path[0]
    return path
