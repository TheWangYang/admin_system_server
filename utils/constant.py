import sys

SERVER_PREFIX = "http://127.0.0.1:8001"
PATH_SUFFIX = "/static/images/todo/"
PATH_NEW_PICTURE_SUFFIX = "/static/images/done/"


def server_abs_path():
    path = sys.path[0]
    return path
