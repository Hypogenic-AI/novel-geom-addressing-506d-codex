"""Generate graph-tracing prompt tasks for the addressability experiment."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from graph_task_common import make_task, write_jsonl


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="results/graph_tasks.jsonl")
    parser.add_argument("--config-out", default="results/graph_task_config.json")
    parser.add_argument("--graph-types", nargs="+", default=["grid4x4", "ring16"])
    parser.add_argument("--context-lengths", nargs="+", type=int, default=[16, 32, 64, 128, 256])
    parser.add_argument("--num-seeds", type=int, default=8)
    parser.add_argument("--seed-offset", type=int, default=1000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tasks = []
    for graph_type in args.graph_types:
        for context_length in args.context_lengths:
            for seed_idx in range(args.num_seeds):
                seed = args.seed_offset + seed_idx
                tasks.append(make_task(graph_type, context_length, seed))

    out = Path(args.out)
    write_jsonl(out, tasks)
    config = {
        "graph_types": args.graph_types,
        "context_lengths": args.context_lengths,
        "num_seeds": args.num_seeds,
        "seed_offset": args.seed_offset,
        "num_tasks": len(tasks),
        "queries_per_task": len(tasks[0]["queries"]) if tasks else 0,
    }
    config_path = Path(args.config_out)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(config, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
