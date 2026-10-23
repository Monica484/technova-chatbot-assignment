import uuid
from langchain_core.messages import HumanMessage
from langsmith import traceable
from app.graph import build_graph

@traceable(name="technova_cli_chat", tags=["technova", "assignment"], metadata={"component": "cli"})
def ask(graph, question: str, thread_id: str):
    if not question or not question.strip():
        return "Please enter a question."
    result = graph.invoke(
        {"messages": [HumanMessage(content=question.strip())]},
        config={"configurable": {"thread_id": thread_id}},
    )
    return result["messages"][-1].content

def main():
    try:
        app_graph = build_graph()
    except Exception as exc:
        print(f"Unable to start TechNova support: {exc}")
        return

    thread_id = str(uuid.uuid4())
    print("TechNova Support Bot. Type 'exit' to quit.")
    print(f"Conversation thread: {thread_id}")
    while True:
        try:
            question = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        try:
            print("TechNova:", ask(app_graph, question, thread_id))
        except Exception:
            print("Sorry, support is temporarily unavailable. Please try again.")

if __name__ == "__main__":
    main()
