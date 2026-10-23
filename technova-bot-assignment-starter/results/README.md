# Results folder

`report.pdf` and summary CSVs are copied/generated from the earlier Colab work described in the report.

Important: raw row-level experiment files from Colab were not available to this packaging step. Download the real CSVs from Colab and upload them here, replacing none of the historical summary values unless you re-run the experiments.

Recommended raw evidence files:
- `latency_results.csv`
- `token_usage_results.csv`
- `fault_test_results.csv`
- `evaluation_questions.csv`
- `evaluation_results.csv`
- `llm_judge_results.csv`
- `evaluation_summary.csv`
- LangSmith screenshots: run tree, failed run, thread/memory test, evaluation results, feedback.

The new scripts write local fresh-run outputs with `_local` suffixes so they do not overwrite historical files.
