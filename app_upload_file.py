import streamlit as st
import os
from streamlit import file_uploader
import base_konwledge
import time

st.title('上传文件')

upload_file = st.file_uploader(label='选择文件', type=['csv', 'txt'])

if upload_file is not None:
    fiel_type = upload_file.type
    file_name = upload_file.name
    file_size = upload_file.size
    st.subheader('文件信息')
    st.write(f'文件：{file_name}，类型：{fiel_type},大小：{file_size / 1024:.2f}KB')

    # 读取文件内容
    file_value = upload_file.getvalue().decode("utf-8")
    #st.write(f'文件内容：{file_value}')

    # 创建BaseKonwledge对象
    base_knowledge = base_konwledge.BaseKonwledge()
    # 将向量库添加到session_state，避免每次上传文件都重新创建对象
    if "base_knowledge" not in st.session_state:
        st.session_state["base_knowledge"] = base_knowledge
    
    
    with st.spinner('正在上传文件...'):
        time.sleep(1)
        res= base_knowledge.upload(file_value,file_name)
        st.write(res)

    # # 保存文件到uploads文件夹
    # save_path = os.path.join("uploads", upload_file.name)
    # with open(save_path, "wb") as f:
    #     f.write(upload_file.getbuffer())
    # st.success(f"已保存到：{save_path}")

