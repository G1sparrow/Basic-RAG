"""
完成长期记忆历史
"""

import json
import os
from langchain_core.messages import messages_from_dict, message_to_dict
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_models.tongyi import ChatTongyi
from typing import Sequence
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import BaseMessage

class FileChatHistoryMessage(BaseChatMessageHistory):
    def __init__(self,session_id:str,storage_path:str):
        self.session_id = session_id
        self.storage_path = storage_path
        #历史文件
        self.file_path = os.path.join(self.storage_path,self.session_id)
        #确保文件所在文件夹存在
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)
    
    def add_messages(self, new_messages:Sequence[BaseMessage]) -> None:
        all_message = list(self.messages)     #调用成员方法
        all_message.extend(new_messages)    #添加新对话

        """
        将数据同步到本地文件,all_messages是List[BaseMessage]对象,通过message_to_dict转为字典，
        """
        new_message = []
        for message in all_message:
                d = message_to_dict(message)
                new_message.append(d)
        
        with open(self.file_path,'w',encoding='utf-8') as f:
            json.dump(new_message,f,ensure_ascii=False, indent=2)        #加入信息到文件

    @property
    #成员函数,读取列表
    def messages(self):
        try:
            with open(self.file_path,'r',encoding='utf-8') as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)            #将得到的字典转为json形式
        except FileNotFoundError:
            return []
    
    def clear(self):
        with open(self.file_path,'w') as f:
            json.dump([],f)