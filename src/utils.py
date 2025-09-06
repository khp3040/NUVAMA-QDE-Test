from pathlib import Path
from typing import List
from .config import PROJECT_ROOT, OUT_RESULTS, OUT_PLOTS, OUT_REPORTS, LOGS_DIR

def make_dirs() -> List[Path]:
    """Create expected project directories (idempotent)."""
    expected = [
        OUT_RESULTS,
        OUT_PLOTS,
        OUT_REPORTS,
        LOGS_DIR
    ]
    for d in expected:
        d.mkdir(parents=True, exist_ok=True)
    return expected
