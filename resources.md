# Resources Catalog

## Summary

This document catalogs resources gathered for the project "Are repeated novel geometries addressable without reasoning?" Resources include papers, datasets, and code repositories. The local paper-finder service was attempted first but did not return within a bounded timeout, so manual search via arXiv, GitHub, Hugging Face, and project pages was used.

## Papers

Total papers downloaded: 8

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| Bongard-LOGO | Nie et al. | 2020/2021 | `papers/2010.00763_bongard_logo_benchmark.pdf` | Core 12K synthetic Bongard geometry benchmark |
| Visual Spatial Reasoning | Liu et al. | 2022/2023 | `papers/2205.00363_visual_spatial_reasoning.pdf` | Natural image spatial-relation verification |
| PuzzleVQA | Chia et al. | 2024 | `papers/2403.13315_puzzlevqa_abstract_patterns.pdf` | Abstract visual pattern VQA with reasoning-stage labels |
| Reasoning Limitations of MLLMs on Bongard Problems | Malkinski et al. | 2024/2025 | `papers/2411.01173_bongard_reasoning_limitations_mllms.pdf` | Prompting strategies for Bongard rule generation |
| Forgotten Polygons | Rudman et al. | 2025 | `papers/2502.15969_forgotten_polygons_shape_blind.pdf` | Polygon recognition/side-counting failures |
| VisuLogic | Xu et al. | 2025 | `papers/2504.15279_visulogic_visual_reasoning.pdf` | Visual-centric logic benchmark |
| Spatial-DISE | Huang et al. | 2025/2026 | `papers/2510.13394_spatial_dise_benchmark.pdf` | Spatial reasoning taxonomy and dataset |
| Symbolic Grounding | Vaishnav and Tammet | 2026 | `papers/2604.21346_symbolic_grounding_bottlenecks.pdf` | Symbolic LOGO inputs isolate representational bottlenecks |

See `papers/README.md` for detailed descriptions. Chunked PDFs and manifests are in `papers/pages/`.

## Datasets

Total datasets downloaded or locally prepared: 7

| Name | Source | Size | Task | Location | Notes |
|------|--------|------|------|----------|-------|
| Bongard-LOGO | Google Drive via NVlabs repo | 1.76 GB zip | Few-shot 2D geometry concept classification | `datasets/bongard_logo/` | Full archive kept compressed; samples extracted |
| Bongard-RWR | GitHub `pavonism/bongard-rwr` | 60 problems, 171 MB | Real-world Bongard rule generation/classification | `datasets/bongard_rwr/` | Copied from cloned repo |
| PuzzleVQA | GitHub/HF `declare-lab/PuzzleVQA` | 2,000 records, 65 MB | Abstract pattern VQA | `datasets/puzzlevqa/` | Includes generated PNGs |
| Shape-Blind | GitHub/HF `mgolov/shape-blind-dataset` | 8,911 PNGs, 46 MB | Polygon/abstract shape recognition and side counting | `datasets/shape_blind/` | CSVs plus extracted images |
| VSR | GitHub/HF `cambridgeltl/vsr_random` | 10,972 metadata records | Spatial relation truth verification | `datasets/visual_spatial_reasoning/` | Metadata plus 10 sample COCO images |
| VisuLogic | HF `VisuLogic/VisuLogic` | 1,000 records/images, 35 MB zip | Four-choice visual reasoning | `datasets/visulogic/` | Images extracted |
| Spatial-DISE CSV subset | HF `TACPS-liv/Spatial-DISE` | 12,914 CSV rows + 10 examples | Spatial reasoning benchmark/training metadata | `datasets/spatial_dise_csv/` | Full 15.9 GB image shards not downloaded |

See `datasets/README.md` for download/loading instructions and `datasets/samples/validation_summary.json` for validation counts.

## Code Repositories

Total repositories cloned: 6

| Name | URL | Purpose | Location | Notes |
|------|-----|---------|----------|-------|
| Bongard-LOGO | https://github.com/NVlabs/Bongard-LOGO | 2D Bongard generator and action-program library | `code/Bongard-LOGO/` | Key for synthetic experiment generation |
| Bongard-RWR | https://github.com/pavonism/bongard-rwr | Real-world Bongard dataset | `code/bongard-rwr/` | Dataset copied to `datasets/` |
| Shape-Blind | https://github.com/rsinghlab/Shape-Blind | Polygon and VC-CoT evaluation | `code/Shape-Blind/` | Includes CSVs and image archive |
| LLM-PuzzleTest | https://github.com/declare-lab/LLM-PuzzleTest | PuzzleVQA/AlgoPuzzleVQA data and eval | `code/LLM-PuzzleTest/` | PuzzleVQA copied to `datasets/` |
| Visual Spatial Reasoning | https://github.com/cambridgeltl/visual-spatial-reasoning | VSR data, splits, baselines | `code/visual-spatial-reasoning/` | Metadata copied to `datasets/` |
| VisuLogic-Eval | https://github.com/VisuLogic-Benchmark/VisuLogic-Eval | VisuLogic evaluation framework | `code/VisuLogic-Eval/` | Benchmark data downloaded separately from HF |

See `code/README.md` for details and entry points.

## Resource Gathering Notes

### Search Strategy
- Tried paper-finder first with diligent and fast queries; both calls timed out or hung.
- Used manual arXiv/web searches around Bongard-LOGO, abstract visual reasoning, shape-blind polygons, VSR, VisuLogic, and Spatial-DISE.
- Followed paper-linked GitHub/Hugging Face resources wherever possible.

### Selection Criteria
- Preference for datasets with controlled geometry, repeated examples, or diagnostic representation splits.
- Preference for papers with code/data.
- Included broader spatial benchmarks only when they provide useful taxonomies or baselines.

### Challenges Encountered
- Paper-finder service did not return results within bounded time.
- `uv add` initially failed because Hatchling could not build an empty metadata-only project; resolved with `uv add --no-sync` and `uv sync --no-install-project`.
- `rsync` and `unzip` were unavailable; used `cp -a` and Python `zipfile`.
- Spatial-DISE full image shards are large (about 15.9 GB); only CSVs and examples were downloaded.

### Gaps and Workarounds
- Symbolic Grounding code is not public yet; Bongard-LOGO action programs can support a comparable symbolic-input experiment.
- VSR full COCO images were not fully downloaded; metadata and 10 sample images are available, with full download instructions in `datasets/README.md`.
- Bongard-LOGO was kept compressed to avoid extracting 408,056 archive entries; sample files are available and the zip can be read directly.

## Recommendations for Experiment Design

1. Primary dataset: Bongard-LOGO, because it gives repeated novel 2D geometries and ground-truth symbolic programs.
2. Main manipulation: vary repetition count while holding geometry/rule fixed, and compare no-CoT direct prompts against action-program oracle prompts.
3. Secondary controls: Shape-Blind for primitive polygon addressability; PuzzleVQA for abstract pattern addressability.
4. Baselines: random, direct VLM, caption-then-answer, symbolic action-program LLM, explicit CoT, visually cued CoT.
5. Metrics: query classification accuracy, natural-language rule match, exact shape/relation token match, class bias, and performance under rotation/scale/style changes.

## Research Execution Notes

The final automated research run prioritized the submitter-provided arXiv paper, `https://arxiv.org/abs/2501.00070`, because it specifically studies in-context graph geometries rather than visual Bongard-style shape concepts. The gathered visual-geometry resources were still useful for framing the broader repetition/addressability question and for choosing controls: no-CoT direct prompting, explicit-reasoning ablation, repetition curves, and a memorization baseline.

Execution artifacts:
- Plan: `planning.md`
- Task generator: `src/generate_graph_tasks.py`
- API runner: `src/run_openai_experiment.py`
- Analysis: `src/analyze_results.py`
- Raw model outputs: `results/model_outputs/`
- Scored outputs and statistics: `results/evaluations/`
- Figures: `figures/`
- Final report: `REPORT.md`

The experiment used real `gpt-4.1` OpenAI API calls on 160 graph-tracing prompt bundles. No simulated model responses were used.
