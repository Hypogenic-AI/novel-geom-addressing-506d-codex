"""Run real OpenAI API calls for generated graph-tracing tasks."""

from __future__ import annotations

import argparse
import concurrent.futures as futures
import json
import os
import re
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from graph_task_common import build_prompt, read_jsonl


thread_local = threading.local()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", default="results/graph_tasks.jsonl")
    parser.add_argument("--out-dir", default="results/model_outputs")
    parser.add_argument("--model", default="gpt-4.1")
    parser.add_argument("--prompt-styles", nargs="+", default=["direct", "reasoned"])
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-workers", type=int, default=5)
    parser.add_argument("--max-tasks", type=int, default=None)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def safe_name(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", text)


def get_client() -> OpenAI:
    if not hasattr(thread_local, "client"):
        thread_local.client = OpenAI()
    return thread_local.client


@retry(wait=wait_exponential(min=1, max=30), stop=stop_after_attempt(5))
def call_openai(
    *,
    model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    seed: int,
    prompt_style: str,
) -> Any:
    max_tokens = 320 if prompt_style == "direct" else 1200
    return get_client().chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        seed=seed,
        response_format={"type": "json_object"},
        max_tokens=max_tokens,
    )


def run_one(task: dict[str, Any], args: argparse.Namespace, prompt_style: str) -> dict[str, Any]:
    system_prompt, user_prompt = build_prompt(task, prompt_style)
    started = datetime.now(timezone.utc)
    record: dict[str, Any] = {
        "task_id": task["task_id"],
        "graph_type": task["graph_type"],
        "context_length": task["context_length"],
        "seed": task["seed"],
        "model": args.model,
        "prompt_style": prompt_style,
        "temperature": args.temperature,
        "api_seed": args.seed,
        "started_at": started.isoformat(),
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
    }
    try:
        response = call_openai(
            model=args.model,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=args.temperature,
            seed=args.seed,
            prompt_style=prompt_style,
        )
        finished = datetime.now(timezone.utc)
        message = response.choices[0].message
        record.update(
            {
                "finished_at": finished.isoformat(),
                "elapsed_seconds": (finished - started).total_seconds(),
                "content": message.content,
                "finish_reason": response.choices[0].finish_reason,
                "usage": response.usage.model_dump() if response.usage else None,
                "response_id": response.id,
                "error": None,
            }
        )
    except Exception as exc:  # noqa: BLE001 - full error is logged for failed API calls.
        finished = datetime.now(timezone.utc)
        record.update(
            {
                "finished_at": finished.isoformat(),
                "elapsed_seconds": (finished - started).total_seconds(),
                "content": None,
                "finish_reason": None,
                "usage": None,
                "response_id": None,
                "error": f"{type(exc).__name__}: {exc}",
            }
        )
    return record


def load_done(path: Path) -> set[str]:
    if not path.exists():
        return set()
    done = set()
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("error") is None:
                done.add(row["task_id"])
    return done


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")


def main() -> None:
    args = parse_args()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set")
    tasks = read_jsonl(Path(args.tasks))
    if args.max_tasks is not None:
        tasks = tasks[: args.max_tasks]

    for prompt_style in args.prompt_styles:
        out_path = Path(args.out_dir) / f"{safe_name(args.model)}_{prompt_style}.jsonl"
        if args.overwrite and out_path.exists():
            out_path.unlink()
        done = load_done(out_path)
        remaining = [task for task in tasks if task["task_id"] not in done]
        print(
            json.dumps(
                {
                    "model": args.model,
                    "prompt_style": prompt_style,
                    "output": str(out_path),
                    "already_done": len(done),
                    "remaining": len(remaining),
                },
                sort_keys=True,
            )
        )
        if not remaining:
            continue
        with futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
            future_to_task = {
                executor.submit(run_one, task, args, prompt_style): task for task in remaining
            }
            for idx, future in enumerate(futures.as_completed(future_to_task), start=1):
                row = future.result()
                append_jsonl(out_path, row)
                status = "ok" if row.get("error") is None else "error"
                print(
                    json.dumps(
                        {
                            "prompt_style": prompt_style,
                            "idx": idx,
                            "total": len(remaining),
                            "task_id": row["task_id"],
                            "status": status,
                            "elapsed_seconds": row["elapsed_seconds"],
                        },
                        sort_keys=True,
                    )
                )


if __name__ == "__main__":
    main()
