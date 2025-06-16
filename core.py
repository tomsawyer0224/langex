from typing import Annotated, Optional
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.runnables import RunnableConfig, ensure_config
from langchain_core.messages import SystemMessage

from langchain_ollama import ChatOllama

from dataclasses import dataclass, field, fields
from prompts import CHAT_PROMPT, SUMMARIZE_PROMPT, REPHRASE_PROMPT

@dataclass(kw_only=True)
class Configuration:
    """The configuration for the agent."""

    system_prompt: str = CHAT_PROMPT
    model: str = "llama3.2:1b"
    temperature: float = 0.7

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig object."""
        config = ensure_config(config)
        configurable = config.get("configurable") or {}
        _fields = {f.name for f in fields(cls) if f.init}
        return cls(**{k: v for k, v in configurable.items() if k in _fields})


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


builder = StateGraph(State)


# def chatbot(state: State, config: RunnableConfig = None):
#     runtime_config = Configuration.from_runnable_config(config)
#     system_prompt = runtime_config.system_prompt
#     model = runtime_config.model
#     temperature = runtime_config.temperature
#     llm = ChatOllama(model=model, temperature=temperature)

#     response = llm.invoke([SystemMessage(content=system_prompt)] + state["messages"])
#     return {"messages": [response]}


# builder.add_edge(START, "chatbot")
# builder.add_node("chatbot", chatbot)
# builder.add_edge("chatbot", END)

def langbot(state: State, config: RunnableConfig = None):
    runtime_config = Configuration.from_runnable_config(config)
    system_prompt = runtime_config.system_prompt
    model = runtime_config.model
    temperature = runtime_config.temperature
    llm = ChatOllama(model=model, temperature=temperature)

    response = llm.invoke([SystemMessage(content=system_prompt)] + state["messages"])
    return {"messages": [response]}


builder.add_edge(START, "langbot")
builder.add_node("langbot", langbot)
builder.add_edge("langbot", END)