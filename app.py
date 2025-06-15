import streamlit as st
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from langgraph.graph.state import CompiledStateGraph
import uuid
import asyncio
from typing import Any, cast

from core import builder
from utils import parse_config, pull_model

st.set_page_config("language expert", page_icon="./public/einstein.png")

# pull ollama models
config = parse_config("./config.yaml")
models = config["models"]
pull_model(models)

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

if "thread" not in st.session_state:
    st.session_state.thread = None
if "graph" not in st.session_state:
    st.session_state.graph = graph
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    avatar = (
        "./public/blobstudent.png"
        if message["role"] == "user"
        else "./public/einstein.png"
    )
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

with st.sidebar:
    model = st.selectbox("Choose a model", models)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.0)

    service = st.radio(
        "Language services",
        ["Chatbot", "Gramma Checker", "Summarizer", "Paraphraser"]
    )
    
col1, col2 = st.columns(2, border=False)
with col1:
    # cont1 = st.container(border=True)
    inp = st.text_area("input", height=300)
    st.button("generate")
with col2:
    # cont2 = st.container(border=True)
    oup = st.text_area("output", height=300)

