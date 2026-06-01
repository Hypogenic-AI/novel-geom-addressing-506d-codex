# Novel Geometry Addressing

This project tests whether in-context graph geometries are verbally addressable through prompting, inspired by Park et al.'s ICLR 2025 graph-tracing study. It uses real `gpt-4.1` API calls, not simulated model outputs.

## Key Findings

- Direct no-reasoning prompting reached 72.7% accuracy overall, above the 50% random baseline.
- The observed-edge memorization baseline reached 82.5%, outperforming the model overall.
- Observed true edges were addressable: 98.8% model accuracy.
- Truly unobserved true edges were not: 3.6% direct accuracy and 0% explicit-reasoning accuracy.
- Explicit reasoning did not significantly improve accuracy over direct JSON-only prompting.

See [REPORT.md](REPORT.md) for methodology, tables, figures, and limitations.

## Reproduce

Requires `OPENAI_API_KEY` in the environment.

```bash
source .venv/bin/activate
uv sync --no-install-project
python src/generate_graph_tasks.py
python src/run_openai_experiment.py --prompt-styles direct reasoned --max-workers 5
python src/analyze_results.py --bootstrap-iters 2000
```

## File Structure

- `planning.md`: preregistered motivation, novelty, and experiment plan.
- `src/`: task generation, API execution, and analysis scripts.
- `results/graph_tasks.jsonl`: generated hidden-graph task bundles.
- `results/model_outputs/`: raw OpenAI prompts and responses.
- `results/evaluations/`: scored responses, summaries, and statistical tests.
- `figures/`: report figures.
- `REPORT.md`: final research report.
