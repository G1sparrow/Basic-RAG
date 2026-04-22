"""
创建向量检索器
"""


from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
import config

class VectorStoreService():
    # 初始化向量库
    def __init__(self):
        self.vec_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(),
            persist_directory=config.persist_directory
        )
    # 获取检索器
    def get_retriever(self):
        return self.vec_store.as_retriever(search_kwargs=config.search_kwargs)
    

if __name__ == "__main__":
    vector_store_service = VectorStoreService()
    res = vector_store_service.get_retriever().invoke("hello")
    print(res)

