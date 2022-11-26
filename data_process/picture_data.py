import pymysql
from camera_process import get_photo
from utils import SERVER_PREFIX
from utils import delete_file
from utils import server_abs_path
from utils import ensure_dir_exists


# 得到连接对象函数function
def get_connect(host='localhost',
                user='root',
                password='wyy666888',
                db='defect_detection_system',
                charset='utf8'):
    # 创建数据库连接对象
    connect = pymysql.connect(host=host,  # 本地数据库
                              user=user,
                              password=password,
                              db=db,
                              autocommit=True,
                              charset=charset)  # 服务器名,账户,密码，数据库名称
    return connect


# 得到图片数据的arr对象格式
def get_picture_data_obj_arr(connect, user_id):
    # 查询数据测试
    # 查询语句
    try:
        # 得到数据库返回值
        cursor = connect.cursor()
        sql = "select * from tbl_picture where uploader_id='" + str(user_id) + "'"
        cursor.execute(sql)
        rows = cursor.fetchall()
        # print("rows : ", rows)
        # 创建返回数据列表对象
        object_list = []
        # 遍历每行数据
        for row in rows:
            # 对每行数据得到对应的行数据json对象
            obj_result = {"picture_id": str(row[0]), "picture_name": str(row[1]), "created_time": str(row[2]),
                          "update_time": str(row[3]), "picture_width": str(row[4]), "picture_height": str(row[5]),
                          "picture_size": str(row[6]), "picture_format": str(row[7]), "uploader_id": str(row[8]),
                          "uploader_name": str(row[9]), "description": str(row[10]), "is_test": str(row[11]),
                          "save_path": str(row[12]), "result_path": str(row[13]), "shooting_environment": str(row[14]),
                          "shooting_direction": str(row[15]), "shooting_quality": str(row[16]),
                          "is_detection": str(row[17])}

            object_list.append(obj_result)
        # 返回图片数据数组
        return object_list
    except Exception as e:
        print("get_picture_data_obj_arr inner error : ", e)
        print(f'error file:{e.__traceback__.tb_frame.f_globals["__file__"]}')
        print(f"error line:{e.__traceback__.tb_lineno}")
        return []  # 返回空数组


# 得到当前该用户拍摄的图片数量
def get_picture_number_by_userid(connect, user_id):
    try:
        cursor = connect.cursor()
        sql = "select count(*) from tbl_picture where uploader_id='" + str(user_id) + "'"
        cursor.execute(sql)
        rows = cursor.fetchall()
        row = rows[0]
        return row[0]
    except Exception as e:
        print("get_picture_number_by_userid inner error : ", e)
        print(f'error file:{e.__traceback__.tb_frame.f_globals["__file__"]}')
        print(f"error line:{e.__traceback__.tb_lineno}")
        return "error"


# 调用后端拍摄图像系统得到一张新的图片
def add_picture_by_userinfo(connect, user_id, user_name):
    try:
        # 在调用拍摄图片之前，得到当前用户todo图片总数据量
        picture_num = get_picture_number_by_userid(connect, user_id)
        # 调用后端的拍摄图片方法，得到拍摄的图片信息
        image_obj = get_photo(user_id, picture_num, user_name)
        if image_obj != {}:
            cursor = connect.cursor()
            print("cursor : ", cursor)
            sql = "insert into tbl_picture(picture_name, created_time, update_time, picture_width, picture_height, picture_size, picture_format, uploader_id, uploader_name, description, is_test, save_path, result_path, shooting_environment, shooting_direction, shooting_quality, is_detection) values('" + str(
                image_obj.get('picture_name')) + "', '" + str(image_obj.get('created_time')) + "','" + str(
                image_obj.get('update_time')) + "', '" + str(image_obj.get('picture_width')) + "', '" + str(
                image_obj.get('picture_height')) + "','" + str(image_obj.get('picture_size')) + "','" + str(
                image_obj.get('picture_format')) + "','" + str(image_obj.get('uploader_id')) + "','" + str(
                image_obj.get('uploader_name')) + "','" + str(image_obj.get('description')) + "','" + str(
                image_obj.get('is_test')) + "','" + str(image_obj.get('save_path')) + "','" + str(
                image_obj.get('result_path')) + "','" + str(
                image_obj.get('shooting_environment')) + "','" + str(image_obj.get('shooting_direction')) + "','" + str(
                image_obj.get('shooting_quality')) + "','" + str(image_obj.get('is_detection')) + "')"  # sql语句
            flag = cursor.execute(sql)
            if flag == 1:
                # 插入成功，返回图片的uri
                return {'new_image_uri': SERVER_PREFIX + image_obj.get('save_path'),
                        'save_path': image_obj.get('save_path')}
            else:
                # 插入失败，删除拍摄的照片，并返回空字符串
                return {'new_image_uri': ""}
        else:
            return {'new_image_uri': ""}
    except Exception as e:
        print("add_picture_by_userinfo inner error : ", e)
        print(f'error file:{e.__traceback__.tb_frame.f_globals["__file__"]}')
        print(f"error line:{e.__traceback__.tb_lineno}")
        # 出现错误，返回error
        return {'new_image_uri': "error"}


# 删除图片
def delete_picture_by_userid_and_pictureid(connect, user_id, picture_id, save_path, result_path):
    try:
        # 删除服务器中存放的图片数据
        save_abs_path = server_abs_path() + save_path
        result_abs_path = server_abs_path() + save_abs_path
        # 删除文件
        delete_file(save_abs_path)
        delete_file(result_abs_path)
        # print("@@@ : ", ensure_dir_exists(save_abs_path))
        # print("--- : ", ensure_dir_exists(result_abs_path))
        # 保证原始文件已经删除
        if ensure_dir_exists(save_abs_path) is False:
            # 表示原始图片删除成功
            # 然后接着判断检测结果图片是否存在
            if ensure_dir_exists(result_abs_path) is False:
                # 表示服务器端图片文件已经删除，下面删除数据库中数据
                cursor = connect.cursor()
                sql = "delete from tbl_picture where uploader_id='" + str(user_id) + "' and picture_id='" + str(
                    picture_id) + "'"
                flag = cursor.execute(sql)
                if flag == 1:  # 表示删除成功
                    return {'result': "success"}
                else:
                    return {'result': "failed"}
            else:
                # 表示没有同步删除成功，那么返回错误
                return {'result': "Remove UnSynchronized Error"}
        elif ensure_dir_exists(save_abs_path) is True:
            return {'result': "Original File Not Exists"}
        else:
            return {'result': "Remove File Inner Error"}
    except Exception as e:
        print("delete_picture_by_userid_and_pictureid inner error : ", e)
        print(f'error file:{e.__traceback__.tb_frame.f_globals["__file__"]}')
        print(f"error line:{e.__traceback__.tb_lineno}")
        return {'result': "error"}


# 设置修改图片详情的函数
def edit_picture_by_userid_and_pictureid(connect, description, user_id, picture_id):
    try:
        cursor = connect.cursor()
        sql = "UPDATE tbl_picture SET description='" + description \
              + "'WHERE uploader_id='" + str(user_id) + "' and picture_id='" + str(picture_id) + "'"
        flag = cursor.execute(sql)
        if flag == 1:
            # 修改成功，返回成功结果
            return {'result': "success"}
        else:
            return {'result': "failed"}
    except Exception as e:
        print("edit_picture_by_userid_and_pictureid inner error : ", e)
        print(f'error file:{e.__traceback__.tb_frame.f_globals["__file__"]}')
        print(f"error line:{e.__traceback__.tb_lineno}")
        # 出现错误，返回error
        return {'result': "error"}
