import os
import hashlib
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader,TextLoader



def get_file_md5_hex(file_path): # 获取文件md5的十六进制字符串

    # 判断文件是否存在
    if not os.path.exists(file_path):
        logger.error(f"[md5计算]文件不存在: {file_path}")
        return

    # 判断文件是否是文件
    if not os.path.isfile(file_path):
        logger.error(f"[md5计算]路径不是文件: {file_path}")
        return
    md5_obj = hashlib.md5() # 创建md5对象
    chunk_size = 4096 # 每次读取文件的大小
    try:
        with open(file_path, "rb") as f: # 二进制方式打开文件
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)

            """
            while chunk := f.read(chunk_size)
                md5_obj.update(chunk)
            -->
            
            chunk = f.read(chunk_size)
            while chunk:
                md5_obj.update(chunk)
                chunk = f.read(chunk_size)

            """
            md5_hex = md5_obj.hexdigest() # 获取md5的十六进制字符串
            return md5_hex

    except Exception as e:
        logger.error(f"[md5计算]文件读取错误: {file_path}, {str(e)}")
        return None

def listdir_with_allowed_type(path: str, allowed_type: tuple[str]): # 返回文件夹内的文件列表(仅返回允许的文件类型)
    files = []

    if not os.path.isdir( path):
        logger.error(f"[文件列表]路径不是文件夹: {path}")
        return allowed_type

    for f in os.listdir(path):# os.listdir(path): 返回文件夹内的文件列表信息
        if f.endswith(allowed_type):# 判断文件类型,endswith表示获取文件后缀
            files.append(os.path.join(path,f))

    return tuple(files)

def pdf_loader(file_path: str,password: str = None) -> list[Document]: # pdf文件加载
    return PyPDFLoader(file_path, password).load()

def txt_loader(file_path) -> list[ Document]: # txt文件加载
    return TextLoader(file_path, encoding="utf-8").load()