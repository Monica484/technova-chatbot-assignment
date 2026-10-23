import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from app.tools import tools

load_dotenv()

SYSTEM_PROMPT = """You are TechNova customer support.
Use get_order_status for order lookups and get_policy for store policies.
Do not invent order information. If an order ID or policy topic is unknown, explain this politely.
Be concise, accurate, and helpful.
Store policies: returns within 30 days in original packaging; 1-year manufacturer warranty;
free shipping above Rs. 999; standard delivery in 3-5 days.
"""

def build_graph():
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise RuntimeError("NVIDIA_API_KEY is missing. Add it to your local .env file or deployment secrets.")

    model_name = os.getenv("NVIDIA_MODEL", "nvidia/nemotron-3.5-lightning-30b-a3b")
    llm = ChatNVIDIA(model=model_name, temperature=0, api_key=api_key).bind_tools(tools)

    def agent(state: MessagesState):
        messages = state["messages"]
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=SYSTEM_PROMPT), *messages]
        response = llm.invoke(messages)
        return {"messages": [response]}

    workflow = StateGraph(MessagesState)
    workflow.add_node("agent", agent)
    workflow.add_node("tools", ToolNode(tools))
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", tools_condition)
    workflow.add_edge("tools", "agent")

    return workflow.compile(checkpointer=MemorySaver())

graph = None
