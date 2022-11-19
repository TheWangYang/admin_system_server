import sys

SERVER_PREFIX = "http://127.0.0.1:8001"
PATH_SUFFIX = "/static/images/todo/"


def server_abs_path():
    path = sys.path[0]
    return path
