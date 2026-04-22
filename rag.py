"""
创建rag对象，实现rag操作
要实现rag操作，首先需要有模型，提示词，向量库检索器，然后合并形成链
用户问题
   ↓
┌───────────────────┐
│  向量库检索文档    │
└───────────────────┘
   ↓
┌───────────────────┐
│  格式化字符串      │
└───────────────────┘
   ↓
┌───────────────────┐
│  组装提示词        │
└───────────────────┘
   ↓
┌───────────────────┐
│  通义千问大模型    │
└───────────────────┘
   ↓
输出答案
"""

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
import config
from vectore_store import VectorStoreService 
from langchain_core.output_parsers import StrOutputParser
from file_history import FileChatHistoryMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableLambda

class RagService():
    def __init__(self):
        #创建向量检索器
        self.vec_service = VectorStoreService()
        #创建模型
        self.model = ChatTongyi(model=config.model)
        #创建提示词
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system","你是一个助理，请根据以下素材回答问题，不要多余回答。素材：{example}"),
                MessagesPlaceholder(variable_name="history"),
                ("human","{input}")
            ]
        )
        #创建链
        self.chain = self.get_chain()

    def get_chain(self):
        """
        用户输入|向量检索器|模型|提示词|
        {"example":vec_store | format_func ,"input":RunnablePassthrough}   | prompt_template | print_prompt | model |StrOutputParser()

        """
        #将向量检索器返回的数据转为str类型
        retriever = self.vec_service.get_retriever()
        #格式化函数
        def format_func(doc):
            print("这是格式化函数")
            if not doc:
                return ''
            content = '['
            for data in doc:
                content += f"文档内容：{data.page_content}\n,文档元数据：{data.metadata},\n\n"
            content += ']'
            return content
        #打印提示词
        def print_prompt(prompt):
            print("这是提示词")
            print("="*10)
            print(prompt.to_string())
            print("="*10)
            return prompt
        
        #打印提示词
        def temp1(value):
            print(f"temp1: {value}")
            return value["input"]
        def temp2(value):
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["example"] = value["example"]
            new_value["history"] = value["input"]["history"]
            return new_value
            
        #基础链
        """
        在加入历史记录的链中，输入自动加入history，变为字典，temp1: {'input': 'hello', 'history': []}

        """
        chain = {"example": RunnableLambda(temp1) |retriever | format_func ,"input":RunnablePassthrough()}  |RunnableLambda(temp2)| self.prompt | print_prompt| self.model |StrOutputParser()

        #历史记录
        def get_history(session_id):
            return FileChatHistoryMessage(session_id, './history')

        # 带记忆链
        with_history_chain = RunnableWithMessageHistory(
            chain,
            get_session_history=get_history,
            input_messages_key="input",
            history_messages_key="history"
        )
        return with_history_chain

if __name__ == "__main__":
    
    # rag = RagService()
    # result = rag.chain.invoke(
    #     input={"input":"语言大师型嘉豪是什么"},
    #     config=session_config
    # )
    # print(result)

    pass