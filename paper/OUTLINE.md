# Paper Outline

## Title
Repeated Novel Geometries Are Addressable Only as Repeated Transitions

## Abstract
- State the behavioral gap: internal in-context geometry may not be verbally queryable.
- Describe the graph tracing probe with hidden 4x4 grids and 16-node rings.
- Report the main quantitative result: direct accuracy is 72.7%, below the 82.5% observed-edge baseline.
- Emphasize the critical negative slice: direct prompting finds 4/112 unobserved positives and explicit reasoning finds 0/112.

## Introduction
- Hook: users need to query newly induced relations, not only rely on hidden activations.
- Background: Park et al. study internal graph representations induced by random-walk traces.
- Gap: prior work does not test whether the induced structure is addressable through ordinary adjacency questions.
- Approach: build hidden graph tracing tasks, vary context length, graph type, and prompt style, then compare against memorization.
- Contributions:
  - Propose a behavioral probe for verbal addressability of in-context graph geometry.
  - Conduct a 1,280-query API evaluation of GPT-4.1.
  - Separate observed edges from unobserved true edges.
  - Show explicit reasoning does not rescue unobserved adjacency recovery.

## Related Work
- In-context graph representations: Park et al.
- Abstract and visual geometry benchmarks: Bongard-LOGO, Shape-Blind, PuzzleVQA, VSR, VisuLogic, Spatial-DISE.
- Prompting and symbolic grounding: Bongard prompting studies and symbolic grounding work.

## Methodology
- Define hidden graph tracing and verbal addressability.
- Describe graph families, random word assignments, random-walk traces, query bundles, and prompt styles.
- Define baselines: random, always-no, observed-edge memorization.
- Define metrics and statistics: accuracy, bootstrap intervals, exact tests, McNemar tests, Holm correction.
- Document model, API settings, parse-validity, tokens, and environment.

## Results
- Main context-length table and figure: model rises with repetition but never beats observed-edge memorization.
- Query-type table and figure: observed true edges are nearly perfect, false distant pairs are easy, false distance-2 pairs are harder.
- Critical slice: unobserved true edges are almost never recovered.
- Reasoning ablation: small nonsignificant overall gain, worse on unobserved positives.

## Discussion
- Interpretation: prompt-accessible knowledge is dominated by repeated local evidence.
- Failure mode: near-neighbor false positives suggest vague locality without exact edge resolution.
- Limitations: one model, behavioral API study, bundled queries, unlabeled walks, no internal activation analysis.
- Implications: representation learning and prompt addressability should be evaluated separately.

## Conclusion
- Summarize the benchmark and negative finding.
- State the key takeaway: repeated edges are addressable, unobserved topology is not.
- Future work: more models, directed moves, algorithmic graph reconstruction baselines, and activation probes.
