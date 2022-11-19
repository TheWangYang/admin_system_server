from sanic import Sanic
from sanic.response import json, file, empty
from data_process import *
import os
import json as j_son

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
@app.post('/picture_table')
async def get_picture_table(request):
    data = j_son.loads(request.body.decode("utf-8").replace("'", '"'))
    # 得到数据连接对象
    connect = get_connect()
    # 根据userName和userPwd得到用户Id
    userId = get_user_id_by_name_and_pwd(connect, data["loginName"], data["loginPassword"])
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
    userId = get_user_id_by_name_and_pwd(connect, data["loginName"], data["loginPassword"])
    if userId is not None:
        return json(add_picture_by_userinfo(connect, userId, data["loginName"]))
    else:
        return json({'error': "userId is None"})


# 设置删除图片的接口
@app.post('/picture_delete')
async def picture_delete(request):
    data = j_son.loads(request.body.decode("utf-8").replace("'", '"'))
    connect = get_connect()
    userId = get_user_id_by_name_and_pwd(connect, data["loginName"], data["loginPassword"])
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
    userId = get_user_id_by_name_and_pwd(connect, data['loginName'], data['loginPassword'])
    if userId is not None:
        return json(edit_picture_by_userid_and_pictureid(connect,
                                                         data['description'],
                                                         userId,
                                                         data['picture_id']))
    else:
        return json({'result': "userId is None"})


# 设置提供用户信息的接口
@app.post('/user_is_exist')
async def get_user_data(request):
    data = j_son.loads(request.body.decode("utf-8").replace("'", '"'))
    # 得到数据库连接对象
    connect = get_connect()
    # 得到是否存在用户，如果存在直接返回用户信息
    curr_user = get_user_data_obj_arr(connect, data)
    # print("curr_user : ", curr_user)
    return json(curr_user)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8001)
