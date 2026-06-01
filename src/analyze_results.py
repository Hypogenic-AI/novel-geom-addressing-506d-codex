"""Analyze graph-tracing API outputs and generate figures."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

from graph_task_common import edge_key, normalize_answer, read_jsonl


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", default="results/graph_tasks.jsonl")
    parser.add_argument("--outputs-dir", default="results/model_outputs")
    parser.add_argument("--figures-dir", default="figures")
    parser.add_argument("--eval-dir", default="results/evaluations")
    parser.add_argument("--model", default="gpt-4.1")
    parser.add_argument("--bootstrap-iters", type=int, default=2000)
    return parser.parse_args()


def safe_name(text: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "_.-" else "_" for ch in text)


def parse_answers(content: str | None) -> dict[str, str | None]:
    if not content:
        return {}
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        return {}
    answers = parsed.get("answers", parsed)
    if isinstance(answers, dict):
        return {str(k): normalize_answer(v) for k, v in answers.items()}
    if isinstance(answers, list):
        output: dict[str, str | None] = {}
        for item in answers:
            if isinstance(item, dict) and "id" in item:
                output[str(item["id"])] = normalize_answer(item.get("answer"))
        return output
    return {}


def load_outputs(outputs_dir: Path, model: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(outputs_dir.glob(f"{safe_name(model)}_*.jsonl")):
        rows.extend(read_jsonl(path))
    return rows


def score_outputs(tasks: list[dict[str, Any]], outputs: list[dict[str, Any]]) -> pd.DataFrame:
    task_by_id = {task["task_id"]: task for task in tasks}
    rows = []
    for output in outputs:
        task = task_by_id.get(output["task_id"])
        if task is None:
            continue
        answers = parse_answers(output.get("content"))
        parse_valid = output.get("error") is None and bool(answers)
        word_to_node = task["hidden"]["word_to_node"]
        observed_counts = {
            tuple(map(int, key.split("-"))): count
            for key, count in task["hidden"]["observed_edge_counts"].items()
        }
        for query in task["queries"]:
            pred = answers.get(query["id"])
            gold = query["answer"]
            current_node = word_to_node[query["current"]]
            candidate_node = word_to_node[query["candidate"]]
            observed_count = observed_counts.get(edge_key(current_node, candidate_node), 0)
            observed_pred = "YES" if observed_count > 0 else "NO"
            rows.append(
                {
                    "task_id": task["task_id"],
                    "graph_type": task["graph_type"],
                    "context_length": task["context_length"],
                    "seed": task["seed"],
                    "model": output["model"],
                    "prompt_style": output["prompt_style"],
                    "query_id": query["id"],
                    "query_type": query["query_type"],
                    "gold": gold,
                    "pred": pred,
                    "correct": pred == gold,
                    "parse_valid": parse_valid and pred is not None,
                    "observed_edge_count": observed_count,
                    "observed_baseline_pred": observed_pred,
                    "observed_baseline_correct": observed_pred == gold,
                    "always_no_correct": gold == "NO",
                    "shortest_path_distance": query["shortest_path_distance"],
                    "completion_tokens": (output.get("usage") or {}).get("completion_tokens", 0),
                    "prompt_tokens": (output.get("usage") or {}).get("prompt_tokens", 0),
                    "total_tokens": (output.get("usage") or {}).get("total_tokens", 0),
                    "api_error": output.get("error"),
                }
            )
    return pd.DataFrame(rows)


def bootstrap_ci(values: np.ndarray, rng: np.random.Generator, iters: int) -> tuple[float, float]:
    if len(values) == 0:
        return (math.nan, math.nan)
    boot = np.empty(iters)
    for i in range(iters):
        sample = rng.choice(values, size=len(values), replace=True)
        boot[i] = sample.mean()
    return tuple(np.quantile(boot, [0.025, 0.975]))


def grouped_summary(df: pd.DataFrame, group_cols: list[str], metric_col: str, iters: int) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []
    for key, group in df.groupby(group_cols, dropna=False):
        if not isinstance(key, tuple):
            key = (key,)
        values = group[metric_col].astype(float).to_numpy()
        lo, hi = bootstrap_ci(values, rng, iters)
        row = dict(zip(group_cols, key, strict=True))
        row.update(
            {
                "n": int(len(group)),
                "mean": float(values.mean()) if len(values) else math.nan,
                "ci95_low": float(lo),
                "ci95_high": float(hi),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def cohen_h(p1: float, p2: float) -> float:
    p1 = min(max(p1, 0.0), 1.0)
    p2 = min(max(p2, 0.0), 1.0)
    return 2 * (math.asin(math.sqrt(p1)) - math.asin(math.sqrt(p2)))


def key_tests(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (prompt_style, graph_type, context_length), group in df.groupby(
        ["prompt_style", "graph_type", "context_length"]
    ):
        successes = int(group["correct"].sum())
        n = int(len(group))
        binom = stats.binomtest(successes, n, p=0.5, alternative="greater")
        observed_successes = int(group["observed_baseline_correct"].sum())
        observed_acc = observed_successes / n
        model_acc = successes / n
        model_correct = group["correct"].astype(bool).to_numpy()
        observed_correct = group["observed_baseline_correct"].astype(bool).to_numpy()
        model_only = int(np.logical_and(model_correct, ~observed_correct).sum())
        observed_only = int(np.logical_and(~model_correct, observed_correct).sum())
        discordant = model_only + observed_only
        if discordant:
            mcnemar_p = min(
                1.0,
                2.0
                * stats.binom.cdf(min(model_only, observed_only), discordant, 0.5),
            )
        else:
            mcnemar_p = 1.0
        rows.append(
            {
                "prompt_style": prompt_style,
                "graph_type": graph_type,
                "context_length": context_length,
                "n": n,
                "model_accuracy": model_acc,
                "random_p_value": float(binom.pvalue),
                "observed_baseline_accuracy": observed_acc,
                "model_minus_observed": model_acc - observed_acc,
                "cohen_h_vs_observed": cohen_h(model_acc, observed_acc),
                "mcnemar_model_only": model_only,
                "mcnemar_observed_only": observed_only,
                "mcnemar_model_vs_observed_p": float(mcnemar_p),
            }
        )
    tests = pd.DataFrame(rows).sort_values(["prompt_style", "graph_type", "context_length"])
    tests["holm_random_p"] = np.nan
    for prompt_style, sub_idx in tests.groupby("prompt_style").groups.items():
        pvals = tests.loc[sub_idx, "random_p_value"].to_numpy()
        order = np.argsort(pvals)
        adjusted = np.empty_like(pvals)
        m = len(pvals)
        running = 0.0
        for rank, idx in enumerate(order):
            value = min(1.0, pvals[idx] * (m - rank))
            running = max(running, value)
            adjusted[idx] = running
        tests.loc[sub_idx, "holm_random_p"] = adjusted
    return tests


def make_figures(df: pd.DataFrame, eval_dir: Path, figures_dir: Path, iters: int) -> None:
    figures_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    overall = grouped_summary(
        df,
        ["prompt_style", "graph_type", "context_length"],
        "correct",
        iters,
    )
    baseline = grouped_summary(
        df,
        ["graph_type", "context_length"],
        "observed_baseline_correct",
        iters,
    )
    graph_types = sorted(df["graph_type"].unique())
    fig, axes = plt.subplots(1, len(graph_types), figsize=(6 * len(graph_types), 4), sharey=True)
    axes = np.atleast_1d(axes)
    for ax, graph_type in zip(axes, graph_types, strict=True):
        sub = overall[overall["graph_type"] == graph_type]
        for prompt_style, style_df in sub.groupby("prompt_style"):
            ax.errorbar(
                style_df["context_length"],
                style_df["mean"],
                yerr=[
                    style_df["mean"] - style_df["ci95_low"],
                    style_df["ci95_high"] - style_df["mean"],
                ],
                marker="o",
                label=f"model/{prompt_style}",
            )
        base = baseline[baseline["graph_type"] == graph_type]
        ax.plot(
            base["context_length"],
            base["mean"],
            linestyle="--",
            marker="s",
            color="black",
            label="observed-edge baseline",
        )
        ax.axhline(0.5, color="gray", linestyle=":", label="random")
        ax.set_title(graph_type)
        ax.set_xlabel("Random-walk transitions")
        ax.set_ylabel("Accuracy")
        ax.set_ylim(0, 1.02)
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(figures_dir / "accuracy_by_context.png", dpi=180)
    plt.close(fig)

    true_low = df[(df["query_type"] == "true_low_seen") & (df["observed_edge_count"] == 0)]
    if not true_low.empty:
        unobserved = grouped_summary(
            true_low,
            ["prompt_style", "graph_type", "context_length"],
            "correct",
            iters,
        )
        fig, axes = plt.subplots(1, len(graph_types), figsize=(6 * len(graph_types), 4), sharey=True)
        axes = np.atleast_1d(axes)
        for ax, graph_type in zip(axes, graph_types, strict=True):
            sub = unobserved[unobserved["graph_type"] == graph_type]
            for prompt_style, style_df in sub.groupby("prompt_style"):
                ax.errorbar(
                    style_df["context_length"],
                    style_df["mean"],
                    yerr=[
                        style_df["mean"] - style_df["ci95_low"],
                        style_df["ci95_high"] - style_df["mean"],
                    ],
                    marker="o",
                    label=prompt_style,
                )
            ax.axhline(0, color="black", linestyle="--", label="observed-edge baseline")
            ax.axhline(0.5, color="gray", linestyle=":", label="random")
            ax.set_title(f"{graph_type}: unobserved true edges")
            ax.set_xlabel("Random-walk transitions")
            ax.set_ylabel("Accuracy")
            ax.set_ylim(0, 1.02)
            ax.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(figures_dir / "unobserved_true_edge_accuracy.png", dpi=180)
        plt.close(fig)

    by_type = grouped_summary(
        df,
        ["prompt_style", "query_type"],
        "correct",
        iters,
    )
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(data=by_type, x="query_type", y="mean", hue="prompt_style", ax=ax)
    ax.axhline(0.5, color="gray", linestyle=":")
    ax.set_xlabel("Query type")
    ax.set_ylabel("Accuracy")
    ax.set_ylim(0, 1.02)
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(figures_dir / "accuracy_by_query_type.png", dpi=180)
    plt.close(fig)

    overall.to_csv(eval_dir / "accuracy_summary.csv", index=False)
    baseline.to_csv(eval_dir / "observed_baseline_summary.csv", index=False)
    grouped_summary(
        df,
        ["prompt_style", "graph_type", "context_length", "query_type"],
        "correct",
        iters,
    ).to_csv(eval_dir / "accuracy_by_query_type_context.csv", index=False)


def main() -> None:
    args = parse_args()
    tasks = read_jsonl(Path(args.tasks))
    outputs = load_outputs(Path(args.outputs_dir), args.model)
    eval_dir = Path(args.eval_dir)
    figures_dir = Path(args.figures_dir)
    eval_dir.mkdir(parents=True, exist_ok=True)
    df = score_outputs(tasks, outputs)
    if df.empty:
        raise RuntimeError("No scored rows were produced")
    df.to_csv(eval_dir / "scored_responses.csv", index=False)
    tests = key_tests(df)
    tests.to_csv(eval_dir / "statistical_tests.csv", index=False)
    make_figures(df, eval_dir, figures_dir, args.bootstrap_iters)

    summary = {
        "rows": int(len(df)),
        "api_calls": int(df[["task_id", "prompt_style"]].drop_duplicates().shape[0]),
        "parse_valid_rate": float(df["parse_valid"].mean()),
        "overall_accuracy": float(df["correct"].mean()),
        "observed_baseline_accuracy": float(df["observed_baseline_correct"].mean()),
        "total_tokens": int(df.drop_duplicates(["task_id", "prompt_style"])["total_tokens"].sum()),
        "prompt_tokens": int(df.drop_duplicates(["task_id", "prompt_style"])["prompt_tokens"].sum()),
        "completion_tokens": int(df.drop_duplicates(["task_id", "prompt_style"])["completion_tokens"].sum()),
    }
    (eval_dir / "analysis_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
