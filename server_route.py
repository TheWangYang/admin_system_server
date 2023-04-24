from sanic import Sanic
from sanic.response import json, file, empty
from data_process import *

import json as j_son
from detection_process import backend_detection_picture
import os

# 创建app实例对象
app = Sanic(__name__)


# 得到未检测图片函数
@app.get("/static/images/todo/<img_file_name:path>")
async def todo_image(_, img_file_name):
    # 每次请求的时候得到所有文件列表
    img_file_names = tuple(*[files for (_, _, files) in os.walk('./static/images/todo')])
    if img_file_name in img_file_names:
        return await file('./static/images/todo/' + img_file_name)
    return empty()


@app.get("/static/images/done/<img_file_name:path>")
async def done_image(_, img_file_name):
    # 每次请求的时候得到所有文件列表
    img_file_names = tuple(*[files for (_, _, files) in os.walk('./static/images/done')])
    if img_file_name in img_file_names:
        return await file('./static/images/done/' + img_file_name)
    return empty()


# 设置提供图片信息请求接口

'''
==========================================图片相关请求api接口===========================================
'''


@app.post('/picture_table')
async def get_picture_table(request):
    data = j_son.loads(request.body.decode("utf-8").replace("'", '"'))
    # 得到数据连接对象
    connect = get_connect()
    # 根据userName和userPwd得到用户Id
    userId = get_user_id_by_name_and_pwd(connect, data["login_name"], data["login_password"])
    if userId is not None:
        # print("userId : ", userId)
        # 得到图片数据数组
        picture_arr = get_picture_data_obj_arr(connect, userId)
        # 调用数据库封装好的对象，得到数据
        return json(picture_arr)
    else:
        return json([])


@app.post('/add_picture')
async def add_picture(request):
    data = j_son.loads(request.body.decode("utf-8").replace("'", '"'))
    connect = get_connect()
    userId = get_user_id_by_name_and_pwd(connect, data["login_name"], data["login_password"])
    if userId is not None:
        return json(add_picture_by_userinfo(connect, userId, data["login_name"]))
    else:
        return json({'error': "userId is None"})


# 设置删除图片的接口
@app.post('/picture_delete')
async def picture_delete(request):
    data = j_son.loads(request.body.decode("utf-8").replace("'", '"'))
    connect = get_connect()
    userId = get_user_id_by_name_and_pwd(connect, data["login_name"], data["login_password"])
    if userId is not None:
        return json(delete_picture_by_userid_and_pictureid(connect,
                                                           userId,
                                                           data["pictureId"],
                                                           data['save_path'],
                                                           data['result_path']))
    else:
        return json({'result': "userId is None"})


@app.post('/picture_edit')
async def picture_edit(request):
    data = j_son.loads(request.body.decode("utf-8").replace("'", '"'))
    connect = get_connect()
    userId = get_user_id_by_name_and_pwd(connect, data['login_name'], data['login_password'])
    if userId is not None:
        return json(edit_picture_by_userid_and_pictureid(connect,
                                                         data['description'],
                                                         userId,
                                                         data['picture_id']))
    else:
        return json({'result': "userId is None"})


@app.post('/detection_picture')
async def detection_picture(request):
    data = j_son.loads(request.body.decode("utf-8").replace("'", '"'))
    # 调用图片检测函数
    annotations_list, detection_relative_result_path = await backend_detection_picture(data)
    return json(
        {'annotations_list': annotations_list, 'detection_relative_result_path': detection_relative_result_path})


'''
=================================================================用户相关请求api接口===========================================================
'''

# 设置提供用户信息的接口
@app.post('/user_is_exist')
async def user_is_exist_front(request):
    data = j_son.loads(request.body.decode("utf-8").replace("'", '"'))
    # 得到数据库连接对象
    connect = get_connect()
    # 得到是否存在用户，如果存在直接返回用户信息
    curr_user = get_user_data_obj_arr(connect, data)
    return json(curr_user)


# 得到所有用户列表的函数
@app.post('/user_list')
async def user_list_front(request):
    # 得到关于mysql的连接
    connect = get_connect()
    # 得到所有用户信息列表
    get_users_list = get_all_users(connect)
    return json(get_users_list)


@app.post('/add_user')
async def add_user_front(request):
    # 解析前端传来的新增用户信息
    data = j_son.loads(request.body.decode("utf-8").replace("'", '"'))
    # 得到数据库连接对象
    connect = get_connect()
    # 新增用户对象到mysql数据库中
    add_user_is_flag = add_user(connect, data)
    print("add_user_is_flag: ", add_user_is_flag)
    return json(add_user_is_flag)


# 删除用户信息函数
@app.post('/delete_user')
async def delete_user_front(request):
    # 解析前端传来的新增用户信息
    data = j_son.loads(request.body.decode("utf-8").replace("'", '"'))
    # 得到数据库连接对象
    connect = get_connect()
    # 新增用户对象到mysql数据库中
    delete_user_is_flag = delete_user(connect, data)
    print("delete_user_is_flag: ", delete_user_is_flag)
    return json(delete_user_is_flag)


@app.post('/edit_user')
async def edit_user_front(request):
    # 解析前端传来的修改用户信息
    data = j_son.loads(request.body.decode("utf-8").replace("'", '"'))
    # 得到数据库连接对象
    connect = get_connect()
    # 新增用户对象到mysql数据库中
    edit_user_flag = edit_user(connect, data)
    print("edit_user_flag: ", edit_user_flag)
    return json(edit_user_flag)


# -------------------------------------------------------------提供用户中心服务接口-----------------------------------------------------
@app.post('/update_user_login_name')
async def update_login_name_front(request):
    # 解析前端传来的修改用户名
    data = j_son.loads(request.body.decode("utf-8").replace("'", '"'))
    # 得到数据库连接对象
    connect = get_connect()
    # 新增用户对象到mysql数据库中
    update_login_name_front_flag = update_user_login_name(connect, data)
    print("update_login_name_front_flag: ", update_login_name_front_flag)
    return json(update_login_name_front_flag)


@app.post('/update_user_login_password')
async def update_user_login_password_front(request):
    # 解析前端传来的修改用户密码
    data = j_son.loads(request.body.decode("utf-8").replace("'", '"'))
    # 得到数据库连接对象
    connect = get_connect()
    # 新增用户对象到mysql数据库中
    update_user_login_password_front_flag = update_user_login_password(connect, data)
    print("update_user_login_password_front_flag: ", update_user_login_password_front_flag)
    return json(update_user_login_password_front_flag)


@app.post('/update_user_phone_number')
async def update_user_phone_number_front(request):
    # 解析前端传来的修改用户名
    data = j_son.loads(request.body.decode("utf-8").replace("'", '"'))
    # 得到数据库连接对象
    connect = get_connect()
    # 更新用户手机号到mysql数据库中
    update_user_phone_number_front_flag = update_user_phone_number(connect, data)
    print("update_user_phone_number_front_flag: ", update_user_phone_number_front_flag)
    return json(update_user_phone_number_front_flag)


@app.post('/update_user_info')
async def update_user_info_front(request):
    # 解析前端传来的修改用户名
    data = j_son.loads(request.body.decode("utf-8").replace("'", '"'))
    # 得到数据库连接对象
    connect = get_connect()
    # 新增用户对象到mysql数据库中
    update_user_info_front_flag = update_user_info(connect, data)
    print("update_user_info_front_flag: ", update_user_info_front_flag)
    return json(update_user_info_front_flag)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081)
