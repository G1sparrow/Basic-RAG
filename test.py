import chromadb
from chromadb.config import Settings
import config

client = chromadb.PersistentClient(
    path=config.chrom_db_path,
    settings=Settings(anonymized_telemetry=False)
)
collection = client.get_collection(config.collection_name)

# 查看所有数据
all_data = collection.get(include=["documents", "metadatas", "embeddings"])
print(f"总条数：{collection.count()}")
print("文本：", all_data["documents"][:3])  # 前3条文本
print("元数据：", all_data["metadatas"][:3]) # 前3条元数据