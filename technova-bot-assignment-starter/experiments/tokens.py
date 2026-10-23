"""Inspect token metadata for one model response; provider metadata may vary by model."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import pandas as pd
from langchain_core.messages import HumanMessage
from app.graph import build_graph

def main():
    graph = build_graph()
    result = graph.invoke({"messages":[HumanMessage(content="What is the return policy?")]},
                          config={"configurable":{"thread_id":"token-test"}})
    message = result["messages"][-1]
    usage = getattr(message, "usage_metadata", None) or {}
    response_metadata = getattr(message, "response_metadata", None) or {}
    row = {
        "model": os.getenv("NVIDIA_MODEL", "nvidia/nemotron-3.5-lightning-30b-a3b"),
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens"),
        "total_tokens": usage.get("total_tokens"),
        "response_metadata_json": json.dumps(response_metadata, default=str)[:2000],
        "note": "Check LangSmith run metadata if provider usage fields are empty."
    }
    os.makedirs("results", exist_ok=True)
    pd.DataFrame([row]).to_csv("results/token_local.csv", index=False)
    print(row)

if __name__ == "__main__":
    main()
