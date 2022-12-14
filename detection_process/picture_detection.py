from utils import server_abs_path
from data_process import *
import os
from mmdet.apis import init_detector, inference_detector

# 设置项目的根本路径
project_path = 'D:/pycharm_work_place/python_server/'
# 指定模型的配置文件和 checkpoint 文件路径
config_file = project_path + \
              'detection_process/configs/fcos_r50_caffe_fpn_gn-head_1x_spdfk_coco_3000_2000.py'
checkpoint_file = project_path + \
                  'detection_process/checkpoints/fcos_r50_caffe_fpn_gn-head_1x_spdfk_coco_3000_2000/latest.pth'


# 模型初始化
def init_model():
    # 根据配置文件和 checkpoint 文件构建模型，使用gpu进行推理
    model = init_detector(config_file, checkpoint_file, device='cuda:0')
    return model


# 检测图片缺陷函数
async def backend_detection_picture(request_data):
    print("request_data: {}".format(request_data))
    # 得到传来的图片和用户信息
    picture_relative_save_path = request_data['detectionPictureSavePath']
    shooting_environment = request_data['shooting_environment']
    shooting_direction = request_data['shooting_direction']
    shooting_quality = request_data['shooting_quality']
    loginName = request_data['loginName']
    loginPassword = request_data['loginPassword']
    # 得到图片名称
    curr_picture_name = picture_relative_save_path.split("/")[4]
    print("curr_picture_name: {}".format(curr_picture_name))
    # 得到待检测图片在服务器中的绝对路径
    picture_abs_save_path = server_abs_path() + picture_relative_save_path
    # 得到已完成检测图片在服务器中保存的路径
    picture_detection_abs_save_path = server_abs_path() + "/static/images/done/"
    picture_detection_relative_save_path = "/static/images/done/"
    if os.path.exists(picture_abs_save_path) and picture_relative_save_path != "":
        # todo-如果存在直接调用so动态库对图片进行推理并返回标注结果数组
        model = init_model()
        # 在当前选择图片上进行推理并展示结果
        result = inference_detector(model, picture_abs_save_path)
        print("result: {}".format(result))
        # 将可视化结果保存为图片
        model.show_result(picture_abs_save_path, result,
                          out_file=os.path.join(picture_detection_abs_save_path, curr_picture_name))
        # 更新图片检测相关属性
        connect = get_connect()
        # 根据用户登录名和密码获得用户id
        user_id = get_user_id_by_name_and_pwd(connect, loginName, loginPassword)
        # 根据用户id和图片保存的相对路径来更新图片的其他属性值
        result = update_picture_respath_env_direction_quality(connect,
                                                              os.path.join(picture_detection_relative_save_path,
                                                                           curr_picture_name),
                                                              shooting_environment,
                                                              shooting_direction,
                                                              shooting_quality,
                                                              user_id,
                                                              picture_relative_save_path)
        # 判断是否更新成功
        if result["result"] == "success":
            # 模拟返回的检测结果数组
            return [
                       {'uid': 1,
                        'box':
                            {'x': 340,
                             'y': 450,
                             'width': 150,
                             'height': 180
                             },
                        'annotationLabel':
                            {'id': 1,
                             'name': 'scratch'
                             }
                        },
                       {'uid': 2,
                        'box':
                            {'x': 560,
                             'y': 670,
                             'width': 230,
                             'height': 230
                             },
                        'annotationLabel':
                            {'id': 2,
                             'name': 'spot'
                             }
                        },
                       {'uid': 3,
                        'box':
                            {'x': 450,
                             'y': 350,
                             'width': 360,
                             'height': 280
                             },
                        'annotationLabel':
                            {'id': 1,
                             'name': 'scratch'
                             }
                        },
                       {'uid': 4,
                        'box':
                            {'x': 200,
                             'y': 750,
                             'width': 230,
                             'height': 120
                             },
                        'annotationLabel':
                            {'id': 3,
                             'name': 'rust'
                             }
                        },
                   ], os.path.join(picture_detection_relative_save_path,
                                   curr_picture_name)
        else:
            return [], os.path.join(picture_detection_relative_save_path,
                                    curr_picture_name)
    else:
        return [], os.path.join(picture_detection_relative_save_path,
                                curr_picture_name)
