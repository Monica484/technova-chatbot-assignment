"""Basic end-to-end latency benchmark. Writes results/latency_local.csv."""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import pandas as pd
from langchain_core.messages import HumanMessage
from app.graph import build_graph

QUESTIONS = [
    "What is the return policy?", "How long is the warranty?",
    "Is shipping free?", "Where is my order TN1001?",
    "Where is my order TN1002?", "Where is my order TN1003?",
    "What is the delivery time?", "Can I return an item after 20 days?",
    "What is the warranty on electronics?", "What does order TN1001 contain?",
    "What is order TN1002 status?", "Does shipping cost extra over Rs. 999?",
    "Can you check TN1003?", "Tell me about returns.", "Tell me about shipping.",
    "What was the item in order TN1001?", "What is the warranty period?",
    "Check order TN1002 again.", "Can I return something in original packaging?",
    "How long does standard delivery take?"
]

def main():
    graph = build_graph()
    rows = []
    for i, question in enumerate(QUESTIONS, start=1):
        start = time.perf_counter()
        ok, answer, error = True, "", ""
        try:
            result = graph.invoke({"messages":[HumanMessage(content=question)]},
                                  config={"configurable":{"thread_id":f"latency-{i}"}})
            answer = str(result["messages"][-1].content)
        except Exception as exc:
            ok, error = False, type(exc).__name__
        rows.append({"question_id":i,"question":question,"success":ok,
                     "latency_seconds":round(time.perf_counter()-start,4),
                     "answer":answer,"error_type":error})
        print(f"{i}/{len(QUESTIONS)} success={ok} latency={rows[-1]['latency_seconds']}s")
    os.makedirs("results", exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv("results/latency_local.csv", index=False)
    successful = df[df.success]["latency_seconds"]
    summary = {"total_requests":len(df),"successful_requests":int(df.success.sum()),
               "failed_requests":int((~df.success).sum()),
               "average_seconds":successful.mean() if len(successful) else None,
               "p50_seconds":successful.quantile(.5) if len(successful) else None,
               "p95_seconds":successful.quantile(.95) if len(successful) else None}
    pd.DataFrame([summary]).to_csv("results/latency_local_summary.csv", index=False)
    print(summary)

if __name__ == "__main__":
    main()
