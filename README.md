# NUVAMA-QDE-Test

**NUVAMA — Quantitative Data Engineer (Take-Home Test)**

This repository contains a small, self-contained pipeline that loads tick data, resamples ticks to OHLC, runs a toy strategy, computes performance metrics, produces plots and a simple report, and writes runtime logs.

---

## Project structure

```text
project_root/
├── data/
│   └── sample_tick_data.csv
├── output/
│   ├── results/        # csv outputs (strategy, performance)
│   ├── plots/          # generated charts (png/svg)
│   └── reports/        # markdown/html/pdf reports
├── logs/
│   └── app.log         # runtime logs (created automatically)
├── src/
│   ├── __init__.py     # package marker & version
│   ├── config.py       # paths, resample rule, strategy defaults
│   ├── io.py           # data loading / saving helpers
│   ├── engine.py       # resampling + strategy/backtest logic
│   ├── analysis.py     # performance metrics, plotting, report creation
│   ├── utils.py        # helper utilities (e.g., make_dirs)
│   ├── logging_config.py
│   └── main.py         # pipeline entry point / orchestrator
├── requirements.txt
├── README_QuantDE_THT.md
└── README.md
---text

---

## Brief module summary

- **`src/__init__.py`**  
  Marks `src/` as a package; may hold package version or convenience imports.

- **`src/config.py`**  
  Centralized constants and defaults (paths, resampling rule, strategy hyperparameters). Change here to affect the whole pipeline.

- **`src/io.py`**  
  File I/O helpers: reading raw tick CSV(s) and saving results.

- **`src/engine.py`**  
  Core data transformation and strategy logic (tick → OHLC → strategy → PnL/equity).

- **`src/analysis.py`**  
  Performance & risk analytics, plotting and simple report generation.

- **`src/utils.py`**  
  Small reusable helpers (e.g., `make_dirs()` to create required directories).

- **`src/logging_config.py`**  
  Central logging configuration (console + rotating file handler writing to `logs/app.log`).

- **`src/main.py`**  
  Entry point / orchestrator. Typical flow:
  1. `utils.make_dirs()`  
  2. `logging_config.configure_logging()`  
  3. `io.load_tick_data()`  
  4. `engine.resample_ticks_to_ohlc()` + `engine.run_*()`  
  5. `analysis.compute_performance()` + `analysis.plot_equity()`  
  6. Save outputs to `output/*`

---

### Quick file/folder meaning
- **`data/`** — put your raw datasets here (do not commit large raw files).  
- **`output/`** — runtime artifacts; safe to ignore in git or keep small, reproducible outputs.  
- **`logs/`** — application logs; add to `.gitignore`.  
- **`src/`** — implementation code. `main.py` runs the pipeline; the other modules are small, focused responsibilities.  
- **`requirements.txt`** — pip installable dependencies; pin versions here for reproducibility.

---

## Requirements

- Python 3.10+ recommended.
- Minimal dependencies:
    - pandas
    - numpy
    - matplotlib
    - tabulate

---

## Quick start — Windows (PowerShell)

```powershell
# from project root
# 1. Create & activate venv
python -m venv .venv
.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt
# or, minimal:
# pip install pandas numpy matplotlib

# 3. Install editable package (optional but recommended)
pip install -e ./src

# 4. Run pipeline
python -m src.main
