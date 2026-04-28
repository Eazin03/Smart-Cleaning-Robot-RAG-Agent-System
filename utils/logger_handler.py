"""
获取项目运行日志
"""

import logging # 日志配置模块
import os
from datetime import datetime
from utils.path_tool import get_abs_path


# 日志保存的根目录
LOG_ROOT_PATH = get_abs_path('logs')

# 确保日志文件存在
os.makedirs(LOG_ROOT_PATH, exist_ok=True)

# 日志格式的配置 error表示错误日志 ; info表示正常信息 ; debug表示啰嗦模式
DEFAULT_LOG_FORMAT = logging.Formatter(
    #%(asctime)s - %(name)s - %(levelname)s - %(filename)s":"%(lineno)s - %(message)s: 时间 - 日志名称 - 日志级别 - 文件名:行号 - 日志内容
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s',

)

def get_logger(
        name: str = "agent",
        console_level: int = logging.INFO, # 控制台日志级别
        file_level: int = logging.DEBUG, # 文件日志级别
        log_file = None # 日志文件
) -> logging.Logger:
    """
    获取日志对象
    :param name: 日志名称
    :return: 日志对象
    """
    # 创建日志对象
    logger = logging.getLogger(name)
    # 设置日志级别
    logger.setLevel(logging.DEBUG)


    # 避免重复添加Handler
    if logger.handlers:
        return logger
    """
    为什么会多次调用 get_logger()？
    因为多个文件都在 import 日志！
    那行代码的作用：
    防止多次 import 导致日志重复打印！
    """

    # 控制台Handler
    console_handler = logging.StreamHandler() # 创建控制台处理器
    console_handler.setLevel(console_level) # 设置日志级别
    console_handler.setFormatter(DEFAULT_LOG_FORMAT) # 设置日志格式

    # 添加控制台Handler: 会在文件中显示
    logger.addHandler(console_handler)

    # 文件Handler
    if not log_file: # 如果没有指定日志文件
        log_file = os.path.join(LOG_ROOT_PATH, f'{name}_{datetime.now().strftime("%Y-%m-%d")}.log') # 日志文件

    file_handler = logging.FileHandler(log_file, encoding='utf-8') # 创建文件处理器
    file_handler.setLevel(file_level)# 设置日志级别: 存放在文件里,内容就会详细一点
    file_handler.setFormatter(DEFAULT_LOG_FORMAT) # 设置日志格式

    # 添加文件Handler
    logger.addHandler(file_handler)

    return  logger

# 快捷获取日志器
logger = get_logger()

if __name__ == '__main__':
    logger.info("测试日志")
    logger.error("测试错误日志")
    logger.warning("测试警告日志")
    logger.debug("测试调试日志")