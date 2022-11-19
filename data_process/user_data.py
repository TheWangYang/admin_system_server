import pymysql


# 得到连接对象函数func
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
                              charset=charset)  # 服务器名,账户,密码，数据库名称
    return connect


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
