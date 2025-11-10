# UVLM: Underwater Video-Language Benchmark 🌊

[🌐 Website](https://yourname.github.io/uvlm-benchmark/) •
[🤗 Dataset on Hugging Face](https://huggingface.co/your-org/uvlm) •
[📄 Paper](https://arxiv.org/abs/2501.12345)

UVLM is a benchmark for **underwater video-language understanding**. It contains **2,109 videos**, ~**0.86M frames**, **419 marine species/categories**, and **20 fine-grained tasks** covering both **biological** and **environmental** aspects of underwater scenes.

This repository provides:

1. dataset structure and example annotations,
2. official evaluation scripts (MCQA + LLM-based),
3. submission format and leaderboard template,
4. a one-line script to download data from Hugging Face.

---

## 🔔 News

- 2025-11-10: Initial release of the UVLM benchmark repo.
- 2025-11-10: Dataset published on Hugging Face: https://huggingface.co/your-org/uvlm
- Coming soon: public leaderboard.

---

## Repository Structure

```text
uvlm-benchmark/
├── README.md
├── setup.py                  # optional, to install as a package
├── uvlm_benchmark/
│   ├── __init__.py
│   ├── data/
│   │   ├── downloader.py     # download from Hugging Face
│   │   ├── dataset.py        # unified dataset loader
│   │   └── schemas.py        # annotation field definitions
│   ├── eval/
│   │   ├── eval_mcqa.py
│   │   ├── eval_llm_judge.py
│   │   └── metrics.py
│   └── utils/
│       └── io.py
├── scripts/
│   ├── download_from_hf.sh   # one-click HF download
│   └── run_eval_mcqa.sh
├── dataset/
│   ├── README.md             # explains real data layout on HF
│   └── annotations_example.json
├── submissions/
│   └── sample_results.json
├── docs/
│   └── index.md              # GitHub Pages (optional)
└── CITATION.cff
```

---

## 1. Get the Dataset

All large files (videos, full annotations, splits) are hosted on **Hugging Face**.  
This repository only contains examples and format descriptions.

**Option A: clone from HF directly**

```bash
git lfs install
git clone https://huggingface.co/your-org/uvlm
```

**Option B: use our script (recommended)**

```bash
bash scripts/download_from_hf.sh
```

After download, your data directory should look like:

```text
uvlm/
 ├── videos/            # optional: raw or segmented videos
 ├── frames/            # optional: extracted frames
 ├── annotations/       # all .json annotation files
 └── splits/            # train / val / test split files
```

> **Note:** `dataset/annotations_example.json` in this repo is a toy example to show the JSON schema.  
> Please download the real annotations from Hugging Face.

---

## 2. Installation

Install the package locally:

```bash
pip install -e .
```

This installs the package `uvlm_benchmark`, so you can run evaluation as modules:

```bash
python -m uvlm_benchmark.eval.eval_mcqa --help
```

---

## 3. Dataset & Annotation Format

UVLM is organized around underwater perception and reasoning. Each video may contain multiple QA items.

**Example annotation (simplified):**

```json
{
  "video_id": "video_00001",
  "fps": 25,
  "duration": 8.2,
  "scene_type": "marine",
  "qas": [
    {
      "qa_id": "video_00001_q1",
      "question": "What species is shown in the video?",
      "options": ["lionfish", "clownfish", "seahorse", "octopus"],
      "answer": "clownfish",
      "task_type": "species_identification",
      "source": "human"
    },
    {
      "qa_id": "video_00001_q2",
      "question": "How clear is the water environment?",
      "answer": "The water is slightly turbid.",
      "task_type": "environment_description",
      "source": "gpt4o"
    }
  ]
}
```

**Key fields**

- `video_id`: unique ID of the video  
- `qas`: list of QA items linked to the video  
- `task_type`: tells the evaluator which metric to use (MCQA vs LLM-based)  
- `source`: where the QA comes from (human / GPT / expert)

A full field-by-field description should be placed in [`dataset/README.md`](dataset/README.md).

---

## 4. Evaluation

We provide **two** official evaluation routes to match the paper.

### 4.1 Objective (MCQA / classification)

Use this for multiple-choice questions.

```bash
python -m uvlm_benchmark.eval.eval_mcqa   --pred submissions/sample_results.json   --gt /path/to/uvlm/annotations
```

- `--pred`: your model predictions  
- `--gt`: ground-truth annotations downloaded from HF  
- Outputs: **MCA** (Multiple Choice Accuracy), **FGC** (Fine-grained Classification) – aligned with the paper.

**Prediction file format** (`submissions/sample_results.json`):

```json
[
  {
    "video_id": "video_00001",
    "qa_id": "video_00001_q1",
    "pred_answer": "clownfish"
  }
]
```

You can extend it with confidence scores if needed.

### 4.2 LLM-based Judgement

Some underwater questions require open-ended or knowledge-grounded evaluation.

```bash
python -m uvlm_benchmark.eval.eval_llm_judge   --pred submissions/sample_results.json   --gt /path/to/uvlm/annotations   --model gpt-4o
```

- Default setting assumes **GPT-4o** (same as the paper).  
- You may replace with your local / open-source LLM, but scores may not be directly comparable.  
- Prompts consistent with the paper are in `uvlm_benchmark/eval/prompts/`.

---

## 5. Submissions & Leaderboard

We start with a simple Markdown leaderboard in this repo.

### Leaderboard (test set)

| Rank | Method                   | MCA  | FGC  | Overall | Link |
|------|--------------------------|------|------|---------|------|
| 1    | GPT-4o (official)        | 77.72| 81.47| 77.95   | -    |
| 2    | VideoLLaMA3-7B + UVLM    | 76.85| 57.17| 73.04   | code |
| 3    | InternVL2.5-8B + UVLM    | 70.26| 43.94| 69.45   | code |

**How to submit**

1. Download data from HF.  
2. Run our official evaluation scripts.  
3. Open an Issue / PR and attach:
   - method name
   - model size
   - training data setting (UVLM-only / extra data)
   - evaluation script version
   - your `results.json`
4. We verify and update the leaderboard.

Later, this table can be moved to GitHub Pages / HF Spaces.

---

## 6. Programmatic Download (Python)

We provide a tiny helper to download from HF inside the codebase:

```python
from uvlm_benchmark.data.downloader import download_uvlm

download_uvlm(
    dest="./data/uvlm",
    repo_id="your-org/uvlm",
)
```

**Example implementation** (`uvlm_benchmark/data/downloader.py`):

```python
from huggingface_hub import snapshot_download
from pathlib import Path

def download_uvlm(dest="./data/uvlm", repo_id="your-org/uvlm", revision=None):
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    snapshot_download(
        repo_id=repo_id,
        local_dir=str(dest),
        repo_type="dataset",
        revision=revision,
        local_dir_use_symlinks=False,
    )
    return dest
```

This way, **real data stays on HF** while **GitHub only stores code and examples**.

---

## 7. Docs / Website (optional)

If you want a nicer “official” page:

1. Put a rendered version of this README in `docs/index.md`.  
2. On GitHub: **Settings → Pages → Deploy from branch** → `main` → `/docs`.  
3. The link at the top (`https://yourname.github.io/uvlm-benchmark/`) will become your benchmark homepage.

---

## 8. Citation

If you use UVLM in your research, please cite both the conference version and the arXiv version.

```bibtex
@article{xue2026uvlm,
  title   = {UVLM: Benchmarking Video-Language Model for Underwater World Understanding},
  author  = {Xizhe Xue and Yangzhou and Dawei Yan and Lijie Tao and Junjie Li and Ying Li and Haokui Zhang and Rong Xiao},
  journal = {Proceedings of the AAAI Conference on Artificial Intelligence},
  year    = {2026}
}

@misc{xue2025uvlm,
  title        = {UVLM: A Comprehensive Benchmark for Underwater Video-Language Understanding},
  author       = {Xizhe Xue and Yangzhou and Dawei Yan and Lijie Tao and Junjie Li and Ying Li and Haokui Zhang and Rong Xiao},
  howpublished = {arXiv preprint arXiv:2501.12345},
  year         = {2025}
}
```
