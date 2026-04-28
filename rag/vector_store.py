import os

from langchain_chroma import Chroma
from utils.config_handler import chroma_config
from utils.logger_handler import logger
from utils.path_tool import get_abs_path
from model.factory import embedding_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.file_handler import txt_loader,pdf_loader,listdir_with_allowed_type,get_file_md5_hex
from langchain_core.documents import Document


# 向量存储服务
class VectorStoreService(object):
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_config["collection_name"],
            persist_directory=get_abs_path(chroma_config["persist_directory"]),
            embedding_function=embedding_model,
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_config["chunk_size"],
            chunk_overlap=chroma_config["chunk_overlap"],
            separators=chroma_config["separators"],
            length_function=len  # 统计字符的依据函数
        )

    def get_retriever(self):
        """
        获取检索器
        :return: 检索器
        """
        retriever = self.vector_store.as_retriever(
            search_kwargs={"k": chroma_config["k"]}
        )
        return retriever

    def load_document(self):
        """
        从数据文件夹内读取数据文件, 转为向量存入向量库
        要计算文件MD5做去重
        :return:
        """
        def check_md5_hex(md5_for_check: str):
            if  not os.path.exists(get_abs_path(chroma_config["md5_hex_store"])):
                open(get_abs_path(chroma_config["md5_hex_store"]), "w",encoding="utf-8").close()
                return False # md5 没处理过
            with open(get_abs_path(chroma_config["md5_hex_store"]), "r", encoding="utf-8") as f:
                md5_hex_list = f.readlines()
                for md5_hex in md5_hex_list:
                    if md5_hex.strip() == md5_for_check:
                        return True # md5 已经处理过

                return  False

        def save_md5(md5_str):
            with open(get_abs_path(chroma_config["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_str + "\n")

        # 将文件中的内容,变成document对象
        def get_file_documents(file_path: str):
            # 判断文件类型
            if file_path.endswith("pdf"):
                return pdf_loader(file_path)

            if file_path.endswith("txt"):
                return txt_loader(file_path)

            return  []

        allowed_files_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_config["data_path"]),
            tuple(chroma_config["allow_knowledge_file_type"])
        )
        for file_path in allowed_files_path:
            md5_hex = get_file_md5_hex(file_path)

            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]文件已处理过: {file_path}")
                continue
            try:
                documents: list[Document] = get_file_documents(file_path)

                if not documents:
                    logger.info(f"[加载知识库]文件内容为空: {file_path}")
                    continue
                split_document:list[Document] =self.spliter.split_documents(documents)

                if not split_document:
                    logger.warning(f"[加载知识库]文件内容已切分为空: {file_path}")
                    continue

                # 将内容存储到向量库
                self.vector_store.add_documents(split_document)

                # 保存md5, 避免重复处理
                save_md5(md5_hex)

                logger.info(f"[加载知识库]文件处理成功: {file_path}")
            except Exception as e:
                # exc_info为True时, 会记录详细的报错堆栈信息, 如果为False, 只会记录错误信息
                logger.error(f"[加载知识库]文件处理错误: {file_path}, {str(e)}", exc_info=True)
                continue

if __name__ == '__main__':
    vector_store = VectorStoreService()
    vector_store.load_document()
    retriever = vector_store.get_retriever()
    res = retriever.invoke("迷路")

    for r in res:
        print(r.page_content)
        print("-"*20)