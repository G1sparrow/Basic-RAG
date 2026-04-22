import streamlit as st
from rag import RagService
import config

# 初始化rag服务
if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

st.title("智能助手")
st.divider()        #分隔符

#输出历史对话
prompt = st.chat_input("请输入你的问题")
if "message" not in st.session_state:
    st.session_state["message"] = [{"role":"assistant","content":"你好，有什么可以帮助你的"}]
for message in st.session_state["message"]:
    st.chat_message(message['role']).write(message['content'])


if prompt:
    #用户输入
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})
    #调用rag服务
    res_stream = st.session_state["rag"].chain.stream({"input":prompt},config.session_config)
    res_list = []
    def capture_ouput(data,res_list):
        for chunk in data:
            res_list.append(chunk)
            #保持流式输出
            yield chunk
    st.chat_message("assistant").write(capture_ouput(res_stream,res_list))
    st.session_state["message"].append({"role":"assistant","content":"".join(res_list)})

