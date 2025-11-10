# UVLM: Underwater Video-Language Benchmark 🌊

[🌐 Website](https://yourname.github.io/uvlm-benchmark/) •
[🤗 Dataset on Hugging Face](https://huggingface.co/your-org/uvlm) •
[📄 Paper](https://arxiv.org/abs/xxxx.xxxxx)

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

## 8. Citation

If you use UVLM in your research, please cite:

```bibtex
@article{uvlm2025,
  title={UVLM: Benchmarking Video-Language Model for Underwater World Understanding},
  author={XIZHE XUE, Yangzhou, Dawei Yan, lijie tao, Junjie Li, Ying Li, Haokui Zhang, Rong Xiao },
  journal={Proceedings of the AAAI Conference on Artificial Intelligence},
  year={2026}
}
