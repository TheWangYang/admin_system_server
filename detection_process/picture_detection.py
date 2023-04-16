from data_process import *
import os
import numpy as np
import cv2
from mmdet.apis import init_detector, inference_detector
from utils import TEMP_IMAGES
from utils import TEMP_IMAGES_RESULT
from utils import PROJECT_PATH

# 设置项目的根本路径
project_path = 'D:/pycharm_work_place/admin_system_server/'
# 指定模型的配置文件和 checkpoint 文件路径
config_file = project_path + \
              'detection_process/configs/fcos_r50_caffe_fpn_gn-head_1x_spdfk_coco_3000_2000.py'
checkpoint_file = project_path + \
                  'detection_process/checkpoints/latest.pth'


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
    picture_abs_save_path = PROJECT_PATH + picture_relative_save_path
    # 得到已完成检测图片在服务器中保存的路径
    picture_detection_abs_save_path = PROJECT_PATH + "/static/images/done/"
    picture_detection_relative_save_path = "/static/images/done/"
    if os.path.exists(picture_abs_save_path) and picture_relative_save_path != "":
        # todo-如果存在直接调用so动态库对图片进行推理并返回标注结果数组
        model = init_model()
        # 创建保存tmp对应的图片集合
        # 读取curr_picture_name对应的tmp文件夹下面的图片集合保存到数组中
        tmp_path = PROJECT_PATH + TEMP_IMAGES + curr_picture_name[:-4] + "/"
        name_list = os.listdir(tmp_path)
        # 在当前选择图片上进行推理并展示结果
        images_path_list = []
        for name in name_list:
            images_path_list.append(tmp_path + name)
        # detection_list
        detection_list = [images_path_list[1], images_path_list[2]]
        result_list = inference_detector(model, detection_list)
        # print("result: {}".format(result))
        # 创建curr_name对应的tmp_result文件夹
        tmp_result = PROJECT_PATH + TEMP_IMAGES_RESULT + curr_picture_name[:-4] + "/"
        if not os.path.exists(tmp_result):
            os.mkdir(tmp_result)
        # 将可视化结果保存为图片
        # 创建结果保存数组用于图像拼接
        result_images_list = []
        flag = -1
        curr_img = None
        for name in name_list:
            flag = flag + 1
            if flag == 1 or flag == 2:
                model.show_result(tmp_path + name, result_list[flag - 1], out_file=tmp_result + name)
                curr_img = cv2.imdecode(np.fromfile(tmp_result + name, dtype=np.uint8), -1)
                result_images_list.append(curr_img)
            else:
                curr_img = cv2.imdecode(np.fromfile(tmp_path + name, dtype=np.uint8), -1)
                result_images_list.append(curr_img)
        # 进行拼接并保存到对应的真实缺陷图片展示文件夹下
        image_vertical = np.vstack(result_images_list)
        cv2.imwrite(picture_detection_abs_save_path + curr_picture_name, image_vertical)
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
            # set return annotations list = [], displays not use screen bboxes
            return [], os.path.join(picture_detection_relative_save_path,
                                    curr_picture_name)
        else:
            return [], os.path.join(picture_detection_relative_save_path,
                                    curr_picture_name)
    else:
        return [], os.path.join(picture_detection_relative_save_path,
                                curr_picture_name)
