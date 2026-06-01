# Downloaded Datasets

This directory contains local datasets for the project. Large files are excluded from git by `datasets/.gitignore`; small samples are kept under each dataset's `samples/` folder.

Validation summary: `datasets/samples/validation_summary.json`.

## Bongard-LOGO

### Overview
- Source: Google Drive archive linked from https://github.com/NVlabs/Bongard-LOGO
- Location: `datasets/bongard_logo/bongard_logo_dataset.zip`
- Size: 1.76 GB compressed, about 2.03 GB uncompressed
- Contents: 168,000 PNG images plus split/action-program JSON files for 12,000 Bongard-LOGO problems
- Task: Few-shot binary concept classification over synthetic 2D shape concepts
- License: See upstream repository

### Download Instructions

```bash
source .venv/bin/activate
uv add --no-sync gdown
uv sync --no-install-project
mkdir -p datasets/bongard_logo
gdown 1-1j7EBriRpxI-xIVqE6UEXt-SzoWvwLx -O datasets/bongard_logo/bongard_logo_dataset.zip
```

### Loading

```python
from zipfile import ZipFile

with ZipFile("datasets/bongard_logo/bongard_logo_dataset.zip") as zf:
    split = zf.read("ShapeBongard_V2/ShapeBongard_V2_split.json")
```

### Sample Data
- Sample action-program JSON and PNGs are in `datasets/bongard_logo/samples/`.

## Bongard-RWR

### Overview
- Source: https://github.com/pavonism/bongard-rwr
- Location: `datasets/bongard_rwr/`
- Size: 60 real-world Bongard problems, 171 MB
- Format: Per-problem folders with left/right/whole images
- Task: Natural-language rule generation or image-to-side classification
- License: See upstream repository

### Download Instructions

```bash
git clone --depth 1 https://github.com/pavonism/bongard-rwr.git code/bongard-rwr
mkdir -p datasets/bongard_rwr
cp -a code/bongard-rwr/dataset/. datasets/bongard_rwr/
```

### Loading

```python
from pathlib import Path
problem_dirs = sorted(Path("datasets/bongard_rwr").iterdir())
```

### Sample Data
- `datasets/bongard_rwr/samples/sample_index.json`

## PuzzleVQA

### Overview
- Source: https://github.com/declare-lab/LLM-PuzzleTest and https://huggingface.co/datasets/declare-lab/PuzzleVQA
- Location: `datasets/puzzlevqa/`
- Size: 2,000 records, 65 MB including generated PNGs
- Format: 20 JSONL files, each with 100 records plus `images/`
- Task: Multiple-choice abstract visual pattern VQA over colors, numbers, shapes, and size
- License: See upstream repository/dataset card

### Download Instructions

```bash
git clone --depth 1 https://github.com/declare-lab/LLM-PuzzleTest.git code/LLM-PuzzleTest
mkdir -p datasets/puzzlevqa
cp -a code/LLM-PuzzleTest/PuzzleVQA/data/. datasets/puzzlevqa/
```

### Loading

```python
import json

with open("datasets/puzzlevqa/color_hexagon.json") as f:
    first = json.loads(next(f))
```

### Sample Data
- `datasets/puzzlevqa/samples/sample_records.json`

## Shape-Blind

### Overview
- Source: https://github.com/rsinghlab/Shape-Blind and https://huggingface.co/datasets/mgolov/shape-blind-dataset
- Location: `datasets/shape_blind/`
- Size: 8,911 PNG images plus six CSV evaluation files, 46 MB extracted
- Format: CSV metadata and PNG images
- Task: Shape naming, side counting, two-shape reasoning, abstract shape counting, VC-CoT tests
- License: See upstream repository/dataset card

### Download Instructions

```bash
git clone --depth 1 https://github.com/rsinghlab/Shape-Blind.git code/Shape-Blind
mkdir -p datasets/shape_blind/CSVs_for_evaluation
cp -a code/Shape-Blind/CSVs_for_evaluation/. datasets/shape_blind/CSVs_for_evaluation/
python - <<'PY'
from zipfile import ZipFile
with ZipFile("code/Shape-Blind/images.zip") as zf:
    zf.extractall("datasets/shape_blind")
PY
```

### Loading

```python
import pandas as pd
df = pd.read_csv("datasets/shape_blind/CSVs_for_evaluation/regular_polygons.csv")
```

### Sample Data
- `datasets/shape_blind/samples/sample_records.json`

## Visual Spatial Reasoning

### Overview
- Source: https://github.com/cambridgeltl/visual-spatial-reasoning and Hugging Face `cambridgeltl/vsr_random`, `cambridgeltl/vsr_zeroshot`
- Location: `datasets/visual_spatial_reasoning/`
- Size: 10,972 validated metadata records in the random split; 10 sample COCO images downloaded locally
- Format: JSONL splits with COCO image links
- Task: True/false spatial relation verification in natural images
- License: Apache-2.0 for repo; COCO image licenses apply to images

### Download Instructions

Metadata:

```bash
git clone --depth 1 https://github.com/cambridgeltl/visual-spatial-reasoning.git code/visual-spatial-reasoning
mkdir -p datasets/visual_spatial_reasoning/data_files datasets/visual_spatial_reasoning/splits
cp -a code/visual-spatial-reasoning/data/data_files/. datasets/visual_spatial_reasoning/data_files/
cp -a code/visual-spatial-reasoning/data/splits/. datasets/visual_spatial_reasoning/splits/
```

Full images, from upstream instructions:

```bash
cd code/visual-spatial-reasoning/data
wget http://images.cocodataset.org/zips/train2017.zip
wget http://images.cocodataset.org/zips/val2017.zip
```

### Loading

```python
import json
with open("datasets/visual_spatial_reasoning/splits/random/train.jsonl") as f:
    first = json.loads(next(f))
```

### Sample Data
- Metadata sample: `datasets/visual_spatial_reasoning/samples/sample_records.json`
- Image sample: `datasets/visual_spatial_reasoning/samples/images/`

## VisuLogic

### Overview
- Source: https://huggingface.co/datasets/VisuLogic/VisuLogic
- Location: `datasets/visulogic/`
- Size: 1,000 records, 1,000 images, 35 MB archive plus extracted images
- Format: `data.jsonl`, `images/`
- Task: Four-choice visual reasoning over quantity, spatiality, position, attributes, style, and other patterns
- License: See dataset card

### Download Instructions

```python
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id="VisuLogic/VisuLogic",
    repo_type="dataset",
    local_dir="datasets/visulogic",
    allow_patterns=["README.md", "*.jsonl", "*.zip", "images/**"],
)
```

Then extract images:

```python
from zipfile import ZipFile
with ZipFile("datasets/visulogic/images.zip") as zf:
    zf.extractall("datasets/visulogic")
```

### Sample Data
- `datasets/visulogic/samples/sample_records.json`

## Spatial-DISE CSV Subset

### Overview
- Source: https://huggingface.co/datasets/TACPS-liv/Spatial-DISE
- Location: `datasets/spatial_dise_csv/`
- Size: CSV subset plus examples, 4 MB; full dataset with image shards is about 15.9 GB and was not downloaded
- Format: CSV files and example images
- Task: Multiple-choice spatial reasoning under intrinsic/extrinsic and static/dynamic taxonomy
- License: CC-BY-NC-SA-4.0

### Download Instructions

```python
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id="TACPS-liv/Spatial-DISE",
    repo_type="dataset",
    local_dir="datasets/spatial_dise_csv",
    allow_patterns=["README.md", "dataset/*.csv", "DISE-bench/*.csv", "examples/**"],
)
```

For the full image-shard dataset, remove `allow_patterns`, but expect roughly 15.9 GB.

### Sample Data
- `datasets/spatial_dise_csv/samples/sample_records.json`
