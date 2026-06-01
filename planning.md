# Research Plan: Verbal Addressability of In-Context 2D Geometries

## Motivation & Novelty Assessment

### Why This Research Matters
Park et al. (ICLR 2025; arXiv:2501.00070) show that language models can reorganize internal representations around a context-specified graph geometry when enough random-walk evidence is supplied. A practical follow-up is whether that learned geometry is externally addressable through ordinary prompts, because representation-level structure is less useful if users cannot query it reliably. This matters for prompt-based control, in-context world models, and settings where a model must use newly defined relations without fine-tuning.

### Gap in Existing Work
The user-linked ICLR paper measures next-token rule-following accuracy and internal representation geometry, not whether the model can verbally answer explicit graph-neighborhood questions after seeing the same kind of traces. The gathered visual-geometry literature similarly shows that models often benefit from repeated examples or symbolic representations, but it does not isolate sparse in-context graph traces, no-chain-of-thought prompting, and unobserved true edges.

### Our Novel Contribution
This experiment turns in-context graph tracing into a direct prompt evaluation. We vary context length, graph topology, and prompt style, then ask a real model to answer bundled adjacency questions with no visible reasoning. We separately score observed true edges and unobserved true edges to distinguish simple repetition/memorization from inferred geometric addressability.

### Experiment Justification
- Experiment 1: Direct no-reasoning adjacency queries across context lengths. This is the core test of whether context-learned geometry is verbally addressable without explicit reasoning.
- Experiment 2: Explicit-reasoning ablation on the same query bundles. This tests whether failures are specific to terse prompting or persist even when the model is invited to reconstruct the graph.
- Experiment 3: Baseline comparison against random choice and observed-edge memorization. This separates genuine geometric inference from copying transitions that already appeared in the prompt.

## Research Question
Can a current LLM verbally address a newly specified 2D or cyclic graph geometry from random-walk context alone, especially under limited repetition and without explicit reasoning traces?

## Background and Motivation
The ICLR paper "In-Context Learning of Representations" defines graph tracing: familiar words are randomly assigned to nodes of a square grid, ring, or hexagonal lattice, and a model receives random-walk traces over that graph. The paper reports that internal representations increasingly mirror the graph as context grows, with accuracy improving after enough context. The open question here is behavioral and user-facing: after sparse or dense traces, can the model answer plain-language adjacency questions about the induced geometry?

The pre-gathered Bongard, Shape-Blind, PuzzleVQA, VSR, VisuLogic, and Spatial-DISE resources support the broader concern that repeated examples and symbolic descriptions can reveal geometric competence hidden by weak direct prompting. They motivate the same controls here: repetition curves, no-CoT prompts, explicit-reasoning ablations, and memorization baselines.

## Hypothesis Decomposition
- H1: Direct no-reasoning adjacency accuracy rises with trace length, because longer context provides more edge evidence.
- H2: At low trace lengths, performance is close to an observed-edge memorization baseline and weak on unobserved true edges.
- H3: If a verbal geometry is actually inferred, the model should answer some unobserved true-edge queries above the observed-edge baseline.
- H4: Explicit reasoning should improve performance if failures are due to prompt surface form rather than unavailable internal structure.

Independent variables:
- Graph topology: 4x4 square grid and 16-node ring.
- Context length: 16, 32, 64, 128, and 256 random-walk transitions.
- Prompt style: direct JSON-only no-reasoning vs. explicit reasoning.
- Query type: observed true edge, sparse or unobserved true edge, distance-2 false edge, random false edge.

Dependent variables:
- Binary adjacency accuracy.
- Accuracy by query type and context length.
- Gap from random and observed-edge memorization baselines.
- Parsed response validity and API/token cost.

## Proposed Methodology

### Approach
Generate synthetic graph-tracing tasks matching the structure of the ICLR paper: a fixed known topology with words randomly assigned to nodes and a random-walk context as evidence. Each API call contains one trace and a bundle of eight adjacency questions. The model returns JSON answers only in the direct condition; the explicit condition permits brief rationale fields but is scored on the same YES/NO labels.

### Experimental Steps
1. Generate square-grid and ring graphs with deterministic seeds, random word-to-node assignments, and random-walk traces.
2. For each graph/context pair, construct balanced query bundles containing true and false candidate adjacencies.
3. Run `gpt-4.1` via the real OpenAI API at temperature 0, caching raw prompts, responses, model IDs, timestamps, and token usage.
4. Parse JSON responses and score each query against ground truth.
5. Compute random and observed-edge memorization baselines from the trace.
6. Analyze performance by context length, graph type, prompt style, and query type.
7. Generate tables and figures for report documentation.

### Baselines
- Random: 50% expected accuracy on balanced yes/no adjacency decisions.
- Always-no: useful because sparse bundles include hard unobserved positives.
- Observed-edge memorization: predicts YES only if the candidate edge appeared in the trace; otherwise predicts NO. This is a strong non-geometric baseline for repetition-driven addressability.

### Evaluation Metrics
- Accuracy with 95% bootstrap confidence intervals.
- Query-type accuracy, especially unobserved or low-count true edges.
- McNemar/permutation-style paired comparisons where useful.
- Cohen's h for differences in proportions.
- Response parse-validity rate.

### Statistical Analysis Plan
Use bootstrap confidence intervals over query-level examples, grouped by graph seed when comparing context lengths. Use two-proportion z-tests or Fisher's exact tests for key contrasts, with Holm correction for multiple context-length comparisons. Treat query-level independence cautiously because queries are bundled within traces; report this as a limitation and prefer effect sizes plus grouped bootstrap intervals.

## Expected Outcomes
Results supporting verbal addressability would show direct no-reasoning accuracy above both random and observed-edge baselines, particularly on true edges not directly observed in the trace. Results refuting the hypothesis would show performance dominated by observed-edge copying and poor unobserved-edge accuracy, especially at low repetition.

## Timeline and Milestones
- Planning and setup: complete isolated environment, GPU/API checks, and this plan.
- Implementation: create `src/generate_graph_tasks.py`, `src/run_openai_experiment.py`, and `src/analyze_results.py`.
- Experimentation: run cached API calls for the selected graph/context/prompt matrix.
- Analysis: compute metrics, figures, and error slices.
- Documentation: write `REPORT.md`, update `README.md`, and validate reproducibility.

## Potential Challenges
- API output may contain malformed JSON; mitigation: use JSON response format, retry malformed outputs, and log parse failures.
- The model may answer by observed transition copying; mitigation: score unobserved true edges separately and compare to the observed-edge baseline.
- Context length may create prompt-size or latency issues; mitigation: use bundled queries and cap traces at 256 transitions for this run.
- Directional geometry is not identifiable from unlabeled random walks; mitigation: evaluate adjacency, which is the identifiable graph property in the ICLR setup.

## Success Criteria
The research succeeds if it produces a reproducible benchmark, real model outputs, statistical analysis, and a report answering whether sparse in-context geometries can be verbally addressed without explicit reasoning. A negative result is successful if it clearly distinguishes failure from random variation and from simple memorization.
