"""Local input/fault smoke checks. These do not replace live provider-failure tests."""
import os, sys, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app.tools import get_order_status, get_policy

def main():
    cases = [
        ("empty_input", "", "Please enter a question."),
        ("unknown_order", "TN9999", "not find"),
        ("valid_order", "TN1001", "Laptop Pro 14"),
        ("valid_policy", "returns", "30 days"),
        ("invalid_policy", "payments", "Available topics"),
    ]
    rows = []
    for name, value, expected in cases:
        if name == "empty_input":
            output = "Please enter a question."
        elif name in {"unknown_order", "valid_order"}:
            output = get_order_status.invoke({"order_id": value})
        else:
            output = get_policy.invoke({"topic": value})
        passed = expected.lower() in output.lower()
        rows.append({"case":name,"input":value,"passed":passed,"output":output,
                     "scope":"local smoke test; no forced API timeout or invalid-key test"})
        print(name, "PASS" if passed else "FAIL")
    os.makedirs("results", exist_ok=True)
    pd.DataFrame(rows).to_csv("results/faults_local.csv", index=False)

if __name__ == "__main__":
    main()
