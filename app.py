import streamlit as st
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from langgraph.graph.state import CompiledStateGraph
import uuid
import asyncio
from typing import Any, cast

from core import builder
from utils import parse_config, pull_model
from prompts import CHAT_PROMPT, SUMMARIZE_PROMPT, REPHRASE_PROMPT

st.set_page_config("language expert", page_icon="./public/einstein.png")

# pull ollama models
config = parse_config("./config.yaml")
models = config["models"]
pull_model(models)

# memory = MemorySaver()
# graph = builder.compile(checkpointer=memory)
graph = builder.compile()

if "thread" not in st.session_state:
    st.session_state.thread = None
if "graph" not in st.session_state:
    st.session_state.graph = graph
if "summarize_clicked" not in st.session_state:
    st.session_state.summarize_clicked = False
# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# for message in st.session_state.messages:
#     avatar = (
#         "./public/blobstudent.png"
#         if message["role"] == "user"
#         else "./public/einstein.png"
#     )
#     with st.chat_message(message["role"], avatar=avatar):
#         st.markdown(message["content"])

with st.sidebar:
    model = st.selectbox("Choose a model", models)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.0)

    service = st.radio(
        "Language services",
        ["Summarizer", "Paraphraser", "Chatbot", "Gramma Checker"]
    )
    
col1, col2 = st.columns(2, border=False)
with col1:
    def click_summarize():
        st.session_state.summarize_clicked = True
    inp = st.text_area("input", height=300)
    btn_summarize = st.button("summarize", on_click = click_summarize)
    thread = {
        "thread_id": str(uuid.uuid4()),
        "system_prompt": SUMMARIZE_PROMPT,
        "model": model,
        "temperature": temperature
    }

    # stream = graph.stream(inp, thread)
with col2:
    with st.empty():
        st.write(inp)
        if st.session_state.summarize_clicked:

            stream = graph.stream({"messages": inp}, thread)
            st.write_stream(stream)
            st.session_state.click_summarize = False
    # oup = st.text_area("output", btn_summarize, height=300)

