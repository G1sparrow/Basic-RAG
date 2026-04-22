#chrom
collection_name = "test"
chrom_db_path = "data/chroma_db"


#text_splitter
chunk_size = 50
chunk_overlap = 10
separators = ['\n', '\t', '. ', '? ', '!\n','。']
max_split_length = 1000

#retrieval
search_kwargs = {
    'k': 2,
}

#model
model = "qwen3-max"

#vector_store
persist_directory = "data/chroma_db"

#session
session_config={
        "configurable":{
            "session_id":"user_a"
        }
    }