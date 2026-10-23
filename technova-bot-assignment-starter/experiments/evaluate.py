"""Simple reference-answer dataset smoke evaluation; not an LLM-as-judge."""
import os, sys, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from langchain_core.messages import HumanMessage
from app.graph import build_graph

CASES = [
 ("What is the return policy?", "Returns accepted within 30 days in original packaging."),
 ("How long is the warranty?", "All electronics carry a 1-year manufacturer warranty."),
 ("Is shipping free?", "Free shipping above Rs. 999. Delivery in 3-5 days."),
 ("Where is order TN1001?", "Laptop Pro 14; status Shipped; estimated delivery 2 days."),
 ("Where is order TN1002?", "Noise-cancel Earbuds; status Processing; estimated delivery 5 days."),
 ("What is order TN1003?", "Phone X; status Delivered."),
 ("Can I return an item after 20 days?", "Returns accepted within 30 days in original packaging."),
 ("What is the standard delivery time?", "Delivery in 3-5 days."),
 ("What item is in TN1001?", "Laptop Pro 14."),
 ("What is the manufacturer warranty?", "1-year manufacturer warranty.")
]

def main():
    graph = build_graph()
    rows=[]
    for i,(question,reference) in enumerate(CASES,1):
        try:
            out=graph.invoke({"messages":[HumanMessage(content=question)]},
                             config={"configurable":{"thread_id":f"eval-{i}"}})
            answer=str(out["messages"][-1].content)
            error=""
        except Exception as exc:
            answer=""
            error=type(exc).__name__
        rows.append({"id":i,"question":question,"reference_answer":reference,
                     "model_answer":answer,"error_type":error,
                     "heuristic_contains_reference_terms":"not_scored"})
    os.makedirs("results",exist_ok=True)
    pd.DataFrame(rows).to_csv("results/evaluation_local.csv",index=False)
    print("Saved results/evaluation_local.csv. This script does not implement an LLM judge.")

if __name__ == "__main__":
    main()
