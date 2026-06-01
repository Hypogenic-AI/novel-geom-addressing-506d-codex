# Code Walkthrough

## Overview

The code implements a text-only graph-tracing evaluation aligned with the user-provided ICLR paper. It generates hidden graph tasks, sends real OpenAI API calls, and scores model answers against graph ground truth and memorization baselines.

## Scripts

### `src/graph_task_common.py`
Shared utilities:
- defines the 4x4 grid and 16-node ring topologies
- assigns ordinary words to hidden nodes
- generates random-walk traces
- samples balanced adjacency queries
- builds direct and explicit-reasoning prompts
- normalizes YES/NO answers

### `src/generate_graph_tasks.py`
Creates `results/graph_tasks.jsonl` and `results/graph_task_config.json`.

Default design:
- graph types: `grid4x4`, `ring16`
- context lengths: `16 32 64 128 256`
- seeds: 8 per graph/context pair
- queries: 8 per task

### `src/run_openai_experiment.py`
Runs real API calls using `OPENAI_API_KEY`.

Important options:
```bash
python src/run_openai_experiment.py --prompt-styles direct reasoned --max-workers 5
```

Outputs:
- `results/model_outputs/gpt-4.1_direct.jsonl`
- `results/model_outputs/gpt-4.1_reasoned.jsonl`

The script caches successful task IDs and skips them on rerun unless `--overwrite` is passed.

### `src/analyze_results.py`
Parses responses, scores each query, computes baselines and statistical tests, and writes figures.

Important outputs:
- `results/evaluations/scored_responses.csv`
- `results/evaluations/accuracy_summary.csv`
- `results/evaluations/statistical_tests.csv`
- `figures/accuracy_by_context.png`
- `figures/accuracy_by_query_type.png`
- `figures/unobserved_true_edge_accuracy.png`

## Reproduction

```bash
source .venv/bin/activate
uv sync --no-install-project
python src/generate_graph_tasks.py
python src/run_openai_experiment.py --prompt-styles direct reasoned --max-workers 5
python src/analyze_results.py --bootstrap-iters 2000
```

Expected scale:
- 160 API calls
- 1,280 scored query-level answers
- about 106k total API tokens

## Validation

The analysis checks parse validity, API errors, random-baseline significance, and paired model-vs-observed-edge baseline differences. The completed run had 100% parse validity and no API errors.
