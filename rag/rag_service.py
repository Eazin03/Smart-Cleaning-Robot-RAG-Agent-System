"""
rag总结服务类: 用户提问, 搜索参考资料, 将提问和参考资料提交给模型, 让模型总结回复
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document


from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompt
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model

class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreService() # 向量存储服务
        self.retriever = self.vector_store.get_retriever() # 检索器
        self.prompt_text = load_rag_prompt()  # 提示语文本+

        self.prompt_template = PromptTemplate.from_template(self.prompt_text) # 提示语

        self.model = chat_model
        self.chain = self._init_chain() # 调用这个方法初始化链

    # 打印提示语
    @staticmethod
    def print_prompt(inputs):
        print("="*20,inputs.to_string(),"="*20)
        return  inputs
    """
    创建 _init_chain () 不是语法必须，而是工程规范：
    让 init 更干净
    让 chain 逻辑独立、清晰
    方便以后扩展、重置、调试
    符合 Python & LangChain 最佳实践
    
    如果你以后想：
    重新创建 chain
    动态修改 prompt
    重置链
    只要调用 _init_chain() 就行，不用重新创建整个类。
    """
    def _init_chain(self):
        chain = self.prompt_template | self.print_prompt | self.model | StrOutputParser()
        return chain

    # 完成检索文档
    def retriever_docs(self, query: str) -> list[Document]:
        return self.retriever.invoke(query)

    def rag_summarize(self, query: str) -> str:
        context_docs = self.retriever_docs(query)

        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"[参考资料{counter}]: 参考资料: {doc.page_content} | 参考元数据: {doc.metadata}\n"

        return self.chain.invoke({"input": query, "context": context})

if __name__ == '__main__':
    rag = RagSummarizeService()
    print(rag.rag_summarize("小户型适合那些扫地机器人"))