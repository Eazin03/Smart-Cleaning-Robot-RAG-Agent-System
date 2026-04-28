"""
工厂设计模式，统一创建、管理大模型（聊天模型 + 向量模型）。
简单说：
ChatModelFactory：专门造聊天大模型（ChatTongyi）
EmbeddingModelFactory：专门造向量嵌入模型（DashScopeEmbeddings）
两个工厂都遵守同一个规范（抽象类）


你只改模型名字 → 确实不用工厂。
但你要换模型厂商、换模型库 → 工厂能救你命！
工厂不是为了 “读配置”，
工厂是为了把 “创建模型的代码” 集中收起来！
"""
from abc import ABC # python中的抽象类
from abc import abstractmethod
from typing import Optional

from langchain_core.embeddings import  Embeddings
from langchain_community.chat_models.tongyi import ChatTongyi,BaseChatModel
from langchain_community.embeddings import DashScopeEmbeddings

from utils.config_handler import rag_config


class BaseModelFactory(ABC): # 抽象类,继承ABC
    # 定义抽象的方法
    @abstractmethod
    def generator(self) -> Optional[ Embeddings | BaseChatModel]:
        pass
"""
作用：
规定所有工厂必须实现 generator () 方法
不实现就报错，强制统一格式
“抽象方法本来就不需要逻辑，它只是强制要求子类必须实现这个方法。”
"""

class ChatModelFactory(BaseModelFactory):
    """
    聊天模型工厂类
    """
    def generator(self) -> Optional[ Embeddings | BaseChatModel]:
        return ChatTongyi(model=rag_config["chat_model_name"])

class EmbeddingModelFactory(BaseModelFactory):
    """
    向量模型工厂
    """
    def generator(self) -> Optional[ Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(model=rag_config["embedding_model_name"])

chat_model = ChatModelFactory().generator()
embedding_model = EmbeddingModelFactory().generator()