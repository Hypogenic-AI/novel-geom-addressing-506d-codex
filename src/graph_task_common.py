"""Shared utilities for in-context graph tracing experiments."""

from __future__ import annotations

import json
import random
from collections import Counter, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any


WORDS = [
    "amber",
    "violin",
    "glacier",
    "candle",
    "helmet",
    "lotus",
    "anchor",
    "velvet",
    "comet",
    "marble",
    "pepper",
    "ladder",
    "willow",
    "engine",
    "prism",
    "canyon",
]


@dataclass(frozen=True)
class GraphSpec:
    graph_type: str
    node_count: int
    edges: tuple[tuple[int, int], ...]
    positions: dict[int, tuple[int, int] | tuple[int]]
    description: str


def get_graph_spec(graph_type: str) -> GraphSpec:
    """Return the fixed hidden topology used for a task."""
    if graph_type == "grid4x4":
        edges: list[tuple[int, int]] = []
        positions: dict[int, tuple[int, int]] = {}
        for row in range(4):
            for col in range(4):
                node = row * 4 + col
                positions[node] = (row, col)
                if col < 3:
                    edges.append((node, node + 1))
                if row < 3:
                    edges.append((node, node + 4))
        return GraphSpec(
            graph_type=graph_type,
            node_count=16,
            edges=tuple(tuple(sorted(edge)) for edge in edges),
            positions=positions,
            description="a 4 by 4 square grid with horizontal and vertical neighbor edges",
        )
    if graph_type == "ring16":
        edges = [tuple(sorted((i, (i + 1) % 16))) for i in range(16)]
        return GraphSpec(
            graph_type=graph_type,
            node_count=16,
            edges=tuple(edges),
            positions={i: (i,) for i in range(16)},
            description="a 16-node ring where each node has exactly two neighbors",
        )
    raise ValueError(f"Unknown graph_type: {graph_type}")


def adjacency_from_edges(node_count: int, edges: tuple[tuple[int, int], ...]) -> dict[int, set[int]]:
    adj = {i: set() for i in range(node_count)}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def shortest_path_lengths(node_count: int, adj: dict[int, set[int]]) -> dict[tuple[int, int], int]:
    """All-pairs shortest path lengths for small unweighted graphs."""
    distances: dict[tuple[int, int], int] = {}
    for start in range(node_count):
        seen = {start: 0}
        queue: deque[int] = deque([start])
        while queue:
            node = queue.popleft()
            for nxt in adj[node]:
                if nxt not in seen:
                    seen[nxt] = seen[node] + 1
                    queue.append(nxt)
        for end, dist in seen.items():
            distances[(start, end)] = dist
    return distances


def edge_key(a: int, b: int) -> tuple[int, int]:
    return tuple(sorted((a, b)))


def generate_random_walk(adj: dict[int, set[int]], length: int, rng: random.Random) -> list[int]:
    """Generate a random walk with `length` transitions and length + 1 nodes."""
    current = rng.randrange(len(adj))
    trace = [current]
    for _ in range(length):
        current = rng.choice(sorted(adj[current]))
        trace.append(current)
    return trace


def choose_ordered_pair(edge: tuple[int, int], rng: random.Random) -> tuple[int, int]:
    a, b = edge
    return (a, b) if rng.random() < 0.5 else (b, a)


def sample_queries(
    *,
    spec: GraphSpec,
    trace: list[int],
    rng: random.Random,
) -> list[dict[str, Any]]:
    """Create a balanced bundle of true and false adjacency questions."""
    adj = adjacency_from_edges(spec.node_count, spec.edges)
    distances = shortest_path_lengths(spec.node_count, adj)
    edge_counts = Counter(edge_key(a, b) for a, b in zip(trace[:-1], trace[1:]))
    true_edges = list(spec.edges)
    observed_true = [edge for edge in true_edges if edge_counts[edge] > 0]
    low_seen_true = sorted(true_edges, key=lambda edge: (edge_counts[edge], edge))

    all_pairs = [
        tuple(sorted((a, b)))
        for a in range(spec.node_count)
        for b in range(a + 1, spec.node_count)
    ]
    true_edge_set = set(true_edges)
    non_edges = [pair for pair in all_pairs if pair not in true_edge_set]
    distance_two = [
        pair for pair in non_edges if distances[(pair[0], pair[1])] == 2
    ]
    distant_false = [
        pair for pair in non_edges if distances[(pair[0], pair[1])] >= 3
    ]

    def pick(pool: list[tuple[int, int]], count: int) -> list[tuple[int, int]]:
        if len(pool) <= count:
            return list(pool)
        return rng.sample(pool, count)

    selected: list[tuple[str, tuple[int, int], bool]] = []
    selected.extend(("true_observed", edge, True) for edge in pick(observed_true or true_edges, 2))
    selected.extend(("true_low_seen", edge, True) for edge in low_seen_true[:2])
    selected.extend(("false_distance2", pair, False) for pair in pick(distance_two, 2))
    selected.extend(("false_distant", pair, False) for pair in pick(distant_false or non_edges, 2))
    rng.shuffle(selected)

    queries: list[dict[str, Any]] = []
    for idx, (query_type, pair, is_adjacent) in enumerate(selected, start=1):
        current, candidate = choose_ordered_pair(pair, rng)
        queries.append(
            {
                "id": f"q{idx}",
                "current_node": current,
                "candidate_node": candidate,
                "current": "",
                "candidate": "",
                "answer": "YES" if is_adjacent else "NO",
                "query_type": query_type,
                "edge_observed_count": int(edge_counts[edge_key(current, candidate)]),
                "shortest_path_distance": int(distances[(current, candidate)]),
            }
        )
    return queries


def make_task(graph_type: str, context_length: int, seed: int) -> dict[str, Any]:
    spec = get_graph_spec(graph_type)
    rng = random.Random(seed)
    words = WORDS[: spec.node_count]
    shuffled = words[:]
    rng.shuffle(shuffled)
    node_to_word = {node: shuffled[node] for node in range(spec.node_count)}
    word_to_node = {word: node for node, word in node_to_word.items()}
    adj = adjacency_from_edges(spec.node_count, spec.edges)
    trace_nodes = generate_random_walk(adj, context_length, rng)
    queries = sample_queries(spec=spec, trace=trace_nodes, rng=rng)
    for query in queries:
        query["current"] = node_to_word[query["current_node"]]
        query["candidate"] = node_to_word[query["candidate_node"]]

    observed_edge_counts = Counter(edge_key(a, b) for a, b in zip(trace_nodes[:-1], trace_nodes[1:]))
    true_edges_observed = sum(1 for edge in spec.edges if observed_edge_counts[edge] > 0)
    return {
        "task_id": f"{graph_type}_L{context_length}_S{seed}",
        "graph_type": graph_type,
        "graph_description": spec.description,
        "context_length": context_length,
        "seed": seed,
        "node_count": spec.node_count,
        "trace": [node_to_word[node] for node in trace_nodes],
        "queries": queries,
        "hidden": {
            "node_to_word": node_to_word,
            "word_to_node": word_to_node,
            "positions": spec.positions,
            "edges_node_ids": [list(edge) for edge in spec.edges],
            "edges_words": [
                sorted([node_to_word[a], node_to_word[b]]) for a, b in spec.edges
            ],
            "true_edges_observed": true_edges_observed,
            "true_edges_total": len(spec.edges),
            "observed_edge_counts": {
                f"{a}-{b}": count for (a, b), count in sorted(observed_edge_counts.items())
            },
        },
    }


def build_prompt(task: dict[str, Any], prompt_style: str) -> tuple[str, str]:
    """Return system and user prompts for a task."""
    trace = " -> ".join(task["trace"])
    query_lines = "\n".join(
        f'{q["id"]}: current="{q["current"]}", candidate="{q["candidate"]}"'
        for q in task["queries"]
    )
    ids = ", ".join(q["id"] for q in task["queries"])
    system = (
        "You answer hidden-graph adjacency questions from random-walk evidence. "
        "Return valid JSON only."
    )
    if prompt_style == "direct":
        user = f"""A set of ordinary words has been assigned to nodes of {task["graph_description"]}.
The trace below is a random walk on the hidden graph: every consecutive pair of words in the trace are adjacent nodes.

Use only the trace and the stated graph type. For each query, decide whether the candidate word can be a valid next word after the current word.
Do not explain or show reasoning.

Return exactly one JSON object with this shape:
{{"answers":[{{"id":"q1","answer":"YES"}},{{"id":"q2","answer":"NO"}}]}}
Use only ids from this list: {ids}.

Trace:
{trace}

Queries:
{query_lines}
"""
        return system, user
    if prompt_style == "reasoned":
        user = f"""A set of ordinary words has been assigned to nodes of {task["graph_description"]}.
The trace below is a random walk on the hidden graph: every consecutive pair of words in the trace are adjacent nodes.

Reconstruct the likely hidden adjacency structure before answering. For each query, decide whether the candidate word can be a valid next word after the current word.

Return exactly one JSON object with this shape:
{{"answers":[{{"id":"q1","answer":"YES","reason":"brief reason"}},{{"id":"q2","answer":"NO","reason":"brief reason"}}]}}
Use only ids from this list: {ids}.

Trace:
{trace}

Queries:
{query_lines}
"""
        return system, user
    raise ValueError(f"Unknown prompt_style: {prompt_style}")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def normalize_answer(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip().upper()
    if text in {"YES", "Y", "TRUE", "ADJACENT", "VALID"}:
        return "YES"
    if text in {"NO", "N", "FALSE", "NOT ADJACENT", "INVALID"}:
        return "NO"
    if text.startswith("YES"):
        return "YES"
    if text.startswith("NO"):
        return "NO"
    return None
