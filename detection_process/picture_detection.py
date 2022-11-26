import os
from utils import server_abs_path


# 检测图片缺陷函数
async def backend_detection_picture(picture_relative_save_path):
    # 得到图片在服务器中的绝对路径
    picture_abs_save_path = server_abs_path() + picture_relative_save_path
    if os.path.exists(picture_abs_save_path) and picture_relative_save_path != "":
        # todo-如果存在直接调用so动态库对图片进行推理并返回标注结果数组
        # 模拟返回的检测结果数组
        annotations_result_list = [
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
        ]
        return annotations_result_list
    else:
        return []

