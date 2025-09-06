from pathlib import Path

# Project root (one level up from this file)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Data / output / logs
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
OUT_RESULTS = OUTPUT_DIR / "results"
OUT_PLOTS = OUTPUT_DIR / "plots"
OUT_REPORTS = OUTPUT_DIR / "reports"
LOGS_DIR = PROJECT_ROOT / "logs"

# Tick resampling settings
RESAMPLE_RULE = "1T"  # 1 minute

# Strategy hyperparams
STRAT = {
    "ma_window": 5,         # moving average window (in minutes)
    "threshold_pct": 0.002, # entry threshold as fraction (0.2%)
    "position_size": 1000   # shares (not value) per trade example
}
