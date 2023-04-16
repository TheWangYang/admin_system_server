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
