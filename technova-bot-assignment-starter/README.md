# TechNova Chatbot Observability Assignment

A LangGraph customer-support chatbot for the fictional TechNova electronics store, using NVIDIA NIM through `ChatNVIDIA` and LangSmith tracing.

## Important deployment note

The existing Streamlit website is kept separate from this assignment scaffold. Do not overwrite the current deployed website's `app.py` while preparing this repository. The current public demo is a simplified direct-model-call UI; this repository contains the LangGraph implementation used for the assignment.

## Features

- `get_order_status(order_id)` and `get_policy(topic)` tools
- LangGraph agent/tool routing using `MessagesState`, `ToolNode`, and `tools_condition`
- `MemorySaver` checkpointing with `thread_id`
- NVIDIA ChatNVIDIA integration
- Optional LangSmith tracing and metadata
- Experiment scripts for latency, token usage, fault scenarios, and evaluation
- Results folder with available summary metrics and a copy of the report

## Project structure

```text
technova-bot-assignment/
├── README.md
├── .env.example
├── .gitignore
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── tools.py
│   ├── graph.py
│   └── chat.py
├── experiments/
│   ├── latency.py
│   ├── tokens.py
│   ├── faults.py
│   └── evaluate.py
└── results/
    ├── README.md
    ├── latency_summary.csv
    ├── token_usage_summary.csv
    ├── fault_test_summary.csv
    ├── evaluation_summary.csv
    └── report.pdf
```

## Setup

Python 3.10+ is recommended.

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env`, then add your own keys locally:

```bash
cp .env.example .env
```

Never commit `.env`, real API keys, or private LangSmith credentials.

## Run the chatbot

```bash
python -m app.chat
```

Try:
- `Where is my order TN1001?`
- `What was the item in that order?` (same session/thread)
- `What is the return policy?`
- `How long is the warranty?`

## Run experiments

```bash
python experiments/latency.py
python experiments/tokens.py
python experiments/faults.py
python experiments/evaluate.py
```

The scripts write CSVs into `results/`. Check each script's comments and console output before interpreting results. Re-run the experiments with valid keys to refresh results for your current environment.

## Previously recorded results

The earlier Colab run used `nvidia/nemotron-3.5-lightning-30b-a3b`:
- 20/20 latency questions succeeded
- Average end-to-end latency: 3.543 s
- P50 latency: 1.764 s
- P95 latency: 12.887 s
- LangSmith token totals from 94 model runs: 46,780 input, 5,908 output, 52,688 total
- Fault scenarios: 5 local simulated cases passed
- Evaluation: 10 test questions generated; rule-based preliminary check marked 10/10, while only 6/10 LLM-judge records had parseable scores. The six parseable records averaged 5/5 for correctness, relevance, and completeness.

These are historical assignment results, not a fresh run from this repository. The cost estimate used the assignment's hypothetical rate card, not actual NVIDIA billing.

## Known gaps to disclose in the report

The prior run did not complete a measured second-model comparison, streaming TTFT for five questions, per-node latency, a fully parseable 10/10 judge run, or evidence screenshots for every failure/evaluation scenario. Do not claim these are complete until you run them and save supporting evidence.

## Existing deployed demo

The live simplified UI is separate from this scaffold. Keep the currently deployed repository and its root `app.py` unchanged until the LangGraph version has been tested and you intentionally choose to replace it.
