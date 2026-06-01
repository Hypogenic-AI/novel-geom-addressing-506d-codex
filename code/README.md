# Cloned Repositories

All repositories were cloned with shallow history into `code/`.

## Bongard-LOGO
- URL: https://github.com/NVlabs/Bongard-LOGO
- Location: `code/Bongard-LOGO/`
- Purpose: Synthetic Bongard problem generator and Python library for LOGO-like 2D shape programs.
- Key files: `README.md`, `setup.py`, `examples/02-bongard_logo/`, `data/human_designed_shapes.tsv`.
- Notes: The full dataset archive was downloaded separately to `datasets/bongard_logo/bongard_logo_dataset.zip`. The repo is useful for generating controlled repeated novel geometries with known action programs.

## Bongard-RWR
- URL: https://github.com/pavonism/bongard-rwr
- Location: `code/bongard-rwr/`
- Purpose: Real-world translations of selected synthetic Bongard concepts.
- Key files: `README.md`, `dataset/`, `Side_by_Side_Comparison_To_Synthetic_Bongard.pdf`.
- Notes: The dataset was copied to `datasets/bongard_rwr/` for experiment use.

## Shape-Blind
- URL: https://github.com/rsinghlab/Shape-Blind
- Location: `code/Shape-Blind/`
- Purpose: Evaluation code and generation notebooks for polygon recognition, side counting, abstract shapes, and visually cued CoT.
- Key files: `evaluation/evaluate_MLLMs.py`, `CSVs_for_evaluation/*.csv`, `image_generation_code/*.ipynb`, `images.zip`.
- Notes: CSVs and extracted images were copied to `datasets/shape_blind/`.

## LLM-PuzzleTest / PuzzleVQA
- URL: https://github.com/declare-lab/LLM-PuzzleTest
- Location: `code/LLM-PuzzleTest/`
- Purpose: PuzzleVQA and AlgoPuzzleVQA data/generation/evaluation code for abstract visual patterns.
- Key files: `PuzzleVQA/data/`, `PuzzleVQA/generation/data_generation.py`, `main.py`, `requirements.txt`.
- Notes: PuzzleVQA data and images were copied to `datasets/puzzlevqa/`.

## Visual Spatial Reasoning
- URL: https://github.com/cambridgeltl/visual-spatial-reasoning
- Location: `code/visual-spatial-reasoning/`
- Purpose: VSR dataset metadata, train/dev/test splits, and baseline evaluation scripts.
- Key files: `data/splits/`, `data/data_files/`, `scripts/`, `analysis_scripts/`.
- Notes: Metadata/splits were copied to `datasets/visual_spatial_reasoning/`. Full COCO image download is documented in `datasets/README.md`; a small sample image set was downloaded locally.

## VisuLogic-Eval
- URL: https://github.com/VisuLogic-Benchmark/VisuLogic-Eval
- Location: `code/VisuLogic-Eval/`
- Purpose: Evaluation framework for the VisuLogic visual reasoning benchmark.
- Key files: `evaluation/eval_model.py`, `models/`, `scripts/`, `requirements.txt`.
- Notes: The benchmark data was downloaded from Hugging Face to `datasets/visulogic/`.
