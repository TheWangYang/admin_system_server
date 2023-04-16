import time

# 得到图片数据的arr对象格式
def get_user_data_obj_arr(connect, data):
    # 查询数据测试
    # 查询语句
    # 得到用户登录名和密码
    loginName = data["loginName"]
    loginPassword = data["loginPassword"]
    # print("到这了...")
    try:
        # 得到数据库返回值
        cursor = connect.cursor()
        sql = "select * from tbl_user where login_name='" + loginName + "' and login_password='" + loginPassword + "'"
        # 执行sql语句
        cursor.execute(sql)
        # 得到行数
        rows = cursor.fetchall()
        # print("rows : ", rows)
        row = rows[0]
        # 判断行数是否为0
        if row is not None:
            # 创建返回数据列表对象
            curr_user = {"user_id": str(row[0]), "user_name": str(row[1]), "login_name": str(row[2]),
                         "login_password": str(row[3]), "phone_number": str(row[4]), "info": str(row[5]),
                         "identification": str(row[6]), "lastLoginTime": str(row[7]), "register_time": str(row[8])}

            # 返回图片数据数组
            return curr_user
        else:
            return {}
    except Exception as e:
        print("error : ", e)
        return {}  # 返回空对象

# 得到用户id函数
def get_user_id_by_name_and_pwd(connect, user_name, user_pwd):
    try:
        cursor = connect.cursor()
        sql = "select user_id from tbl_user where login_name='" + user_name + "' and login_password='" + user_pwd + "'"
        cursor.execute(sql)
        rows = cursor.fetchall()
        row = rows[0]
        return row[0]
    except Exception as e:
        print("error : ", e)
        return None

# 得到所有用户对象函数
def get_all_users(connect):
    # 得到所有用户对象
    try:
        # 得到数据库返回值
        cursor = connect.cursor()
        sql = "select * from tbl_user"
        cursor.execute(sql)
        rows = cursor.fetchall()
        # 创建用户数据列表对象用于返回
        object_list = []
        # 遍历每行数据
        for row in rows:
            # 对每行数据得到对应的行数据json对象
            obj_result = {"user_id": str(row[0]), "user_name": str(row[1]), "login_name": str(row[2]),
                          "login_password": str(row[3]), "phone_number": str(row[4]), "info": str(row[5]),
                          "identification": str(row[6]), "lastLoginTime": str(row[7]), "register_time": str(row[8])}

            object_list.append(obj_result)
        # 返回用户数据数组
        return object_list
    except Exception as e:
        print("get_all_users inner error : ", e)
        print(f'error file:{e.__traceback__.tb_frame.f_globals["__file__"]}')
        print(f"error line:{e.__traceback__.tb_lineno}")
        return []  # 返回空数组


# 新增用户到数据库中
def add_user(connect, data):
    # 获得当前用户登录时间
    times = time.time()
    local_time = time.localtime(times)
    print("data: ", data)
    # 判断data不是空字典，那么进行插入数据库操作
    if data != {}:
        cursor = connect.cursor()
        sql = "insert into tbl_user(user_name, login_name, login_password, phone_number, info, identification, lastLoginTime, register_time) values('" + str(
            data["user_name"]) + "', '" + str(data["login_name"]) + "','" + str(
            data["login_password"]) + "', '" + str(data["phone_number"]) + "', '" + str(
            data["info"]) + "','" + str(data["identification"]) + "','" + time.strftime("%Y-%m-%d %H:%M:%S", local_time) + "','" + time.strftime("%Y-%m-%d %H:%M:%S", local_time) + "')"  # sql语句
        flag = cursor.execute(sql)
        connect.commit()
        print("add user inner success!")
        if flag == 1:
            # 插入成功，返回成功
            return {'flag': 'success'}
        else:
            # 插入失败，因为数据库原因，并返回failed
            return {'flag': 'error'}
    else:
        return {'flag': 'failed'}


# 根据用户id删除用户函数
def delete_user(connect, data):
    print("delete user_id: ", data)
    # 判断data不是空字典，那么进行插入数据库操作
    if data != {}:
        cursor = connect.cursor()
        sql = "delete from tbl_user where user_id='" + str(data['user_id']) + "'"
        flag = cursor.execute(sql)
        connect.commit()
        print("delete user inner success!")
        if flag == 1:
            # 删除成功，返回成功
            return {'flag': 'success'}
        else:
            # 删除失败，因为数据库原因，并返回failed
            return {'flag': 'error'}
    else:
        # 因为前端传来数据为空，删除失败，返回failed
        return {'flag': 'failed'}


# 设置修改用户信息函数
def edit_user(connect, data):
    try:
        cursor = connect.cursor()
        sql = "UPDATE tbl_user SET identification='" + data['identification'] + "'WHERE user_id='" + str(data['user_id']) + "'"
        flag = cursor.execute(sql)
        connect.commit()
        if flag == 1:
            print("edit user success.")
            # 编辑用户成功，返回成功结果
            return {'flag': "success"}
        else:
            # 编辑用户失败，返回failed
            return {'flag': "failed"}
    except Exception as e:
        print("edit_picture_by_userid_and_pictureid inner error : ", e)
        print(f'error file:{e.__traceback__.tb_frame.f_globals["__file__"]}')
        print(f"error line:{e.__traceback__.tb_lineno}")
        # 编辑用户出现错误，返回error
        return {'flag': "error"}







