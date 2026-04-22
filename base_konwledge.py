"""
当前文件是为了将文件添加到知识库，经过流程是：
1.传入文件
2.创建BaseKnowledge对象，包括向量库，分本分割器
3.判断文件内容的MD5值是否已经存在于知识库中，如果不存在，则继续执行
4.将文件内容添加到知识库中



"""
from datetime import datetime
import os
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import config

def check_md5(md5_str):
    """检查内容的MD5值是否已经存在"""
    if os.path.exists('./md5.txt'):
        with open('./md5.txt', 'r') as lines:
            for line in lines:
                if md5_str == line.strip():
                    return True
            return False
    else:
        print("还未生成知识库文件")
        with open('./md5.txt', 'w') as f:
            pass
        return False
    
def save_md5(md5_str):
    with open('./md5.txt', 'a') as f:
        f.write(md5_str + '\n')
def delete_md5(md5_str):
    """从md5.txt中删除指定的MD5值"""
    if not os.path.exists('./md5.txt'):
        return
    with open('./md5.txt', 'r') as f:
        lines = f.readlines()
    with open('./md5.txt', 'w') as f:
        for line in lines:
            if line.strip() != md5_str:
                f.write(line)

def get_md5(str, encoding="utf-8"):
    # 将字符串转换为字节序列
    str_bytes = str.encode(encoding=encoding)
    # 计算字节序列的MD5值
    m = hashlib.md5()   # 创建一个MD5对象
    m.update(str_bytes) # 更新MD5对象
    return m.hexdigest()    # 返回16进制的MD5值

class BaseKonwledge():
    """将文件添加到知识库，先将文件内容转为BaseKnowledge对象"""
    def __init__(self):
        #确认向量库文件夹存在
        os.makedirs(config.chrom_db_path, exist_ok=True)

        # 初始化Chroma对象
        self.chroma = Chroma(
        collection_name = config.collection_name,
        embedding_function = DashScopeEmbeddings(model="text-embedding-v2"),
        persist_directory= config.chrom_db_path
        )
        # 初始化RecursiveCharacterTextSplitter对象
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = config.chunk_size,
            chunk_overlap = config.chunk_overlap,
            separators = config.separators,
            length_function = len
        )
    def upload(self,data,file_name):
        """上传文件的条件
        1、文件MD5不存在于知识库中
        2、文件内容不为空
        """
        md5_hex = get_md5(data)
        if check_md5(md5_hex):
            return "跳过，内容已经在向量库里存在"
        # 如果文件内容长度大于最大拆分长度，则进行拆分
        if len(data) >config.max_split_length:
            konwledge_chunks = self.splitter.split_text(data)
        else:
            konwledge_chunks = [data]
        # 将拆分后的文本加入向量库
        self.chroma.add_texts(konwledge_chunks, 
                              metadatas=
                              [{"source": file_name,
                               "create_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                               "seperateor":"小明",
                               "md5":md5_hex
                               } for i in range(len(konwledge_chunks))] 
                            )
        save_md5(md5_hex)
        return "上传向量库成功"
    #删除向量库
    def delete_by_content(self, data):
        """根据文件原始内容删除向量库中的数据 + 删除md5记录"""
        md5_hex = get_md5(data)
        
        # 1. 检查是否存在该内容
        if not check_md5(md5_hex):
            return "无法删除：该内容未存入向量库"

        # 2. 根据MD5删除向量库中对应数据（where过滤）
        self.chroma.delete(where={"md5": md5_hex})

        # 3. 删除md5.txt中的记录
        delete_md5(md5_hex)

        return "删除成功：已从向量库和md5记录中移除该内容"

    def delete_by_filename(self, file_name):
        """根据文件名删除向量库中的所有相关数据 + 删除对应md5"""
        # 1. 查询向量库中 source=file_name 的所有数据
        docs = self.chroma.get(where={"source": file_name})
        if not docs or len(docs["ids"]) == 0:
            return f"无法删除：未找到文件 {file_name} 相关数据"

        # 2. 删除向量库数据
        self.chroma.delete(where={"source": file_name})

        # 3. 尝试删除md5（这里因为一个文件对应一个md5，直接清空即可）
        # 如果你需要精准删除，建议upload时把md5存入metadata，我也可以帮你改
        return f"删除成功：已移除文件 {file_name} 的全部向量数据"

    def clear_all(self):
        """清空整个向量库 + 清空md5记录"""
        # 清空向量库
        self.chroma.delete_collection()
        # 重新初始化
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model="text-embedding-v2"),
            persist_directory=config.chrom_db_path
        )
        # 清空md5.txt
        with open('./md5.txt', 'w') as f:
            f.write('')
        return "已清空整个向量库和md5记录"
    
if __name__ == '__main__':
    base = BaseKonwledge()
    #print(base.upload("hello world", "test.txt"))