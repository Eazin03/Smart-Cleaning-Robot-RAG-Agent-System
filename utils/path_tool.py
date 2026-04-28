"""
为工程提供统一的绝对路径
"""

import os

def get_project_root_path():
    """
    获取工程根目录
    :return:字符串根目录
    """
    # 获取当前文件绝对路径
    current_file = os.path.abspath(__file__)# 获取当前文件绝对路径

    # 获取工程的根目录, 先获取文件所在的文件夹绝对路径
    current_dir = os.path.dirname(current_file) # 获取当前文件所在目录

    # 获取根目录
    project_root_path = os.path.dirname(current_dir)
    return project_root_path

def get_abs_path(relative_path):
    """
    传入相对路径, 获取绝对路径
    :param relative_path: 相对路径
    :return: 绝对路径
    """
    project_root_path = get_project_root_path()
    abs_path = os.path.join(project_root_path, relative_path) # 将工程根目录和相对路径拼接成绝对路径
    return abs_path

if __name__ == '__main__':
    print(get_abs_path('data\test.txt'))