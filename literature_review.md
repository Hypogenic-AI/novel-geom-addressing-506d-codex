# Literature Review: Repeated Novel Geometries and Addressability Without Explicit Reasoning

## Review Scope

### Research Question
Can models verbally address or classify repeated novel 2D geometries from prompts with limited repetition, without relying on explicit reasoning traces?

### Inclusion Criteria
- Benchmarks involving 2D geometric, abstract, or spatial visual concepts.
- Work that separates visual perception/representation from language reasoning.
- Evaluation of VLMs/MLLMs/LLMs on few-shot visual abstraction, shape recognition, or spatial relation tasks.
- Datasets or code suitable for downstream automated experiments.

### Exclusion Criteria
- Purely text-only spatial reasoning without visual grounding, unless used as contrast.
- General VQA benchmarks with weak control over geometry or abstract visual concepts.
- Papers without accessible PDF or reproducible resources, unless they define an important benchmark taxonomy.

### Time Frame and Sources
Primary focus: 2020-2026. Sources: paper-finder attempt, arXiv, Hugging Face dataset cards, GitHub repositories, and project pages. The local paper-finder service did not return within a 45-second bounded call, so manual search was used.

## Search Log

| Date | Query | Source | Results | Notes |
|------|-------|--------|---------|-------|
| 2026-06-01 | novel 2D geometry visual language models spatial reasoning prompting | paper-finder | timed out | Service hung under bounded timeout |
| 2026-06-01 | visual language models spatial reasoning geometry benchmark | paper-finder | timed out | Fell back to manual search |
| 2026-06-01 | Bongard LOGO large language models visual reasoning | arXiv/web | 3 core papers | Bongard-LOGO, Bongard MLLM limitations, Symbolic Grounding |
| 2026-06-01 | PuzzleVQA abstract visual patterns | arXiv/web | 1 dataset paper | Relevant controlled abstract pattern benchmark |
| 2026-06-01 | MLLMs shape-blind polygons | arXiv/web | 1 paper + dataset | Directly relevant to geometry naming/counting |
| 2026-06-01 | visual spatial reasoning benchmark VLM | arXiv/web | VSR, VisuLogic, Spatial-DISE | Useful secondary spatial baselines |

## Key Papers

### Bongard-LOGO: A New Benchmark for Human-Level Concept Learning and Reasoning
- Authors: Nie et al.; Year: 2020/2021; Source: arXiv/NeurIPS. URL: https://arxiv.org/abs/2010.00763
- Key Contribution: Introduces 12,000 procedurally generated Bongard problems over 2D shapes with ground-truth LOGO action programs.
- Methodology: Positive and negative example panels define a latent concept; query images are classified as positive/negative. Concepts include free-form stroke programs, basic shape categories, and abstract attributes.
- Datasets Used: New Bongard-LOGO dataset; 9,300 train, 900 validation, 1,800 test problems.
- Results: Best model accuracies were around 66-73% on several splits, while expert humans exceeded 90% and reached about 99% on basic shapes.
- Code Available: Yes, https://github.com/NVlabs/Bongard-LOGO
- Relevance: The strongest base dataset for repeated novel 2D geometries. Its action programs make it possible to compare image-only prompts, symbolic descriptions, and explicit reasoning conditions.

### Reasoning Limitations of Multimodal Large Language Models: A Case Study of Bongard Problems
- Authors: Malkinski et al.; Year: 2024/2025; Source: arXiv/ICML. URL: https://arxiv.org/abs/2411.01173
- Key Contribution: Tests proprietary and open MLLMs on classical synthetic Bongard problems and real-world Bongard variants.
- Methodology: Direct image prompting, per-panel descriptive prompting, iterative prompting, and contrastive prompting; evaluates both free-form rule generation and binary classification.
- Datasets Used: Classical synthetic BPs, Bongard-HOI, Bongard-OpenWorld, and new Bongard-RWR.
- Results: Best generation score on synthetic BPs was only 22/100 across strategies. Descriptive prompting usually helped, but still fell far below human performance. On Bongard-RWR, humans averaged 65%, while models were much lower.
- Code Available: Yes, https://github.com/pavonism/bongard-rwr
- Relevance: Direct evidence that current MLLMs struggle to verbalize abstract geometry concepts even when the visual domain is simple or translated to real-world imagery.

### Symbolic Grounding Reveals Representational Bottlenecks in Abstract Visual Reasoning
- Authors: Vaishnav and Tammet; Year: 2026; Source: arXiv. URL: https://arxiv.org/abs/2604.21346
- Key Contribution: Uses Bongard-LOGO action programs and natural-language action descriptions to test whether VLM failure is due to perception/representation or reasoning.
- Methodology: Componential-Grammatical pipeline: replace pixels with ground-truth LOGO-style symbolic inputs, then ask LLMs to infer the rule and classify the query.
- Datasets Used: Bongard-LOGO subset of 2,000 problems across FF, BD, HD-Comb, and HD-Novel.
- Results: Raw visual Gemini-2.5 baseline was near chance around 50%; symbolic conditions averaged roughly 69-79% on FF/BD and reached mid-90s for the best models on Free-form. Randomizing support categories or action sequences reduced accuracy, showing use of structure rather than surface token matching.
- Code Available: Not yet; paper states code to be released after acceptance.
- Relevance: Most directly answers the hypothesis. It suggests current VLMs can reason over repeated novel geometry if given the right representation, but raw visual addressing remains a bottleneck.

### Forgotten Polygons: Multimodal Large Language Models are Shape-Blind
- Authors: Rudman et al.; Year: 2025; Source: arXiv/Findings ACL. URL: https://arxiv.org/abs/2502.15969
- Key Contribution: Demonstrates failures in simple polygon identification and side counting.
- Methodology: Controlled regular polygons, two-shape summation, abstract merged/irregular shapes, and visually cued CoT.
- Datasets Used: New Shape-Blind image/CSV suite plus MathVerse visual-dominant subset.
- Results: Many MLLMs identify common shapes but fail on less frequent polygons, especially heptagons. Text-only backbones know polygon facts, while vision encoders fail to separate shapes. VC-CoT raised GPT-4o accuracy on random-letter heptagon side-counting from 7% to 93%.
- Code Available: Yes, https://github.com/rsinghlab/Shape-Blind
- Relevance: Strong evidence that the issue is not just high-level reasoning; even basic geometric primitives may be poorly represented visually.

### PuzzleVQA: Diagnosing Multimodal Reasoning Challenges with Abstract Visual Patterns
- Authors: Chia et al.; Year: 2024; Source: arXiv/Findings ACL. URL: https://arxiv.org/abs/2403.13315
- Key Contribution: Introduces 2,000 abstract visual pattern puzzles with generated captions, pattern explanations, and deductions.
- Methodology: Multiple-choice VQA over colors, numbers, size, and shapes; progressively supplies ground-truth perception/induction/deduction to locate bottlenecks.
- Results: GPT-4V scored 46.4% on single-concept and 45.5% on dual-concept puzzles; humans scored 91.6% on a sampled subset. Bottlenecks were visual perception and inductive reasoning.
- Code Available: Yes, https://github.com/declare-lab/LLM-PuzzleTest
- Relevance: Useful for testing whether repeated demonstrations help with abstract pattern addressing without explicit reasoning.

### Visual Spatial Reasoning
- Authors: Liu et al.; Year: 2022/2023; Source: arXiv/TACL. URL: https://arxiv.org/abs/2205.00363
- Key Contribution: 10,972 validated natural image-text pairs with 66 spatial relations.
- Methodology: Binary true/false caption verification; includes random and zero-shot object-concept splits.
- Results: Human ceiling 95.4%; VLM baselines around 56-70% on random split and worse on zero-shot. Orientation relations remain near chance.
- Code Available: Yes, https://github.com/cambridgeltl/visual-spatial-reasoning
- Relevance: Good baseline for verbal addressing of spatial relations, though less focused on novel geometry.

### VisuLogic
- Authors: Xu et al.; Year: 2025; Source: arXiv. URL: https://arxiv.org/abs/2504.15279
- Key Contribution: 1,000 visual-centric reasoning problems designed to limit language shortcuts.
- Methodology: Four-choice visual reasoning across quantity, spatiality, position, attribute, style, and other categories.
- Results: Most models score below 30%, near 25% random baseline and far below 51.4% human performance. CoT gives minimal gains.
- Code Available: Yes, https://github.com/VisuLogic-Benchmark/VisuLogic-Eval
- Relevance: Supports the view that verbal descriptions often lose critical visual structure.

### Spatial-DISE
- Authors: Huang et al.; Year: 2025/2026; Source: arXiv/ICLR. URL: https://arxiv.org/abs/2510.13394
- Key Contribution: Defines an intrinsic/extrinsic and static/dynamic taxonomy for spatial reasoning and releases a 559-item benchmark plus 12K training set.
- Methodology: Multiple-choice spatial tasks including 2D/3D rotation, folding, projection, shape finding, and combination.
- Results: Average model accuracy across 32 VLMs was 28.4%, near 25% chance and far below 76.8% human baseline. Fine-tuning on Spatial-DISE-12K improved Qwen2.5-VL-7B from 26.1% to 47.0%.
- Code/Data Available: Dataset at https://huggingface.co/datasets/TACPS-liv/Spatial-DISE
- Relevance: Useful taxonomy and synthetic-data pipeline, but broader than the immediate 2D geometry-addressing hypothesis.

## Common Methodologies

- Bongard-style few-shot concept induction: positive and negative examples define a rule, then a query is classified or the rule is verbalized.
- Prompt decomposition: direct whole-image prompting, per-panel captioning, iterative refinement, and contrastive pair comparison.
- Symbolic grounding: convert images to action programs, structured descriptions, object attributes, or captions before reasoning.
- Controlled synthetic generation: use programs/templates to produce large numbers of verified images and labels.
- Bottleneck diagnosis: progressively supply perception, induction, deduction, or symbolic representations to isolate failures.

## Standard Baselines

- Random choice: 50% for binary Bongard/VSR, 25% for four-choice datasets.
- Human baseline: essential because many tasks are simple for humans but difficult for models.
- Direct VLM prompting: raw image plus task instruction, no explicit reasoning.
- Caption-then-reason: image descriptions generated by model or oracle, then LLM solves.
- Symbolic oracle: LOGO/action-program input for upper-bound representation tests.
- CoT/VC-CoT: explicit reasoning traces, with or without visual annotations.

## Evaluation Metrics

- Accuracy for binary classification or multiple-choice tasks.
- Rule-generation correctness, usually manually or model-ensemble judged.
- Per-category accuracy, especially by concept type, spatial relation, or DISE quadrant.
- Positive/negative class accuracy to detect liberal "positive" bias in Bongard tasks.
- Robustness under perturbation: action sequence permutation, category permutation, rotation, size, color, or contrast changes.

## Datasets in the Literature

- Bongard-LOGO: primary dataset for repeated novel 2D geometries with action programs.
- Bongard-RWR: real-world image translations of synthetic Bongard concepts.
- Shape-Blind: controlled polygon/abstract-shape images and CSV task metadata.
- PuzzleVQA: abstract visual puzzle patterns with ground-truth explanations.
- VSR: natural-image spatial relation verification.
- VisuLogic: visual-centric logic benchmark with images and MCQ data.
- Spatial-DISE: spatial reasoning taxonomy, benchmark CSVs, examples, and larger image-shard dataset.

## Gaps and Opportunities

- Raw image VLMs are weak at extracting exact 2D geometric structure, even when the reasoning backend can use that structure.
- Existing benchmarks often test either classification or explicit reasoning; fewer isolate "verbal addressability" under no-CoT, limited repetition, and novel geometry.
- Repetition is underexplored as an independent variable. Bongard tasks use six positives/six negatives, but the effect of 1, 2, 3, or more repeated examples should be tested directly.
- Symbolic oracle conditions are useful but may overstate practical performance unless paired with noisy perception-derived descriptions.
- Prompting can help, but explicit reasoning or visual cues may change the construct being measured. The proposed experiment should separate direct answer, hidden/internal reasoning, explicit CoT, and symbolic/description-only conditions.

## Recommendations for Our Experiment

- Primary dataset: Bongard-LOGO, using the downloaded archive and action programs. Generate reduced-repetition variants with 1/2/3/6 positives and negatives.
- Secondary dataset: Shape-Blind for simple polygon addressing and side-counting controls; PuzzleVQA for abstract pattern transfer.
- Baselines: direct VLM label/rule prompt; no-CoT short answer; caption-then-answer; action-program oracle; optional explicit CoT and VC-CoT as upper-bound interventions.
- Metrics: binary query accuracy, rule-verbalization agreement, shape/relation token accuracy, calibration by positive/negative class, and sensitivity to rotation/scale/style perturbations.
- Main methodological control: compare raw image prompts against exact action-program prompts. If symbolic prompts succeed while raw images fail, the bottleneck is representation/addressability rather than abstract reasoning alone.
