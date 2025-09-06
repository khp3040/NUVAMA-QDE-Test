from pathlib import Path
import pandas as pd
import logging
from typing import Optional
from .config import DATA_DIR

logger = logging.getLogger(__name__)

def load_tick_data(path: Optional[Path] = None) -> pd.DataFrame:
    """
    Load tick CSV into a DataFrame.
    Tries to auto-detect timestamp column and parse datetimes.
    Expected minimal columns: timestamp, price, (optional) size, symbol
    """
    if path is None:
        path = DATA_DIR / "sample_tick_data.csv"
    path = Path(path)
    logger.info("Loading tick data from %s", path)
    if not path.exists():
        raise FileNotFoundError(f"Tick data not found: {path}")

    # Read CSV, attempt to parse timestamp columns
    df = pd.read_csv(path, low_memory=False)
    # heuristics for timestamp column
    ts_cols = [c for c in df.columns if "time" in c.lower() or "timestamp" in c.lower() or c.lower() == "date"]
    if ts_cols:
        ts_col = ts_cols[0]
        df[ts_col] = pd.to_datetime(df[ts_col], errors="coerce")
        df = df.rename(columns={ts_col: "timestamp"})
    else:
        # fallback: look for first column that can be parsed
        for c in df.columns:
            try:
                df[c] = pd.to_datetime(df[c])
                df = df.rename(columns={c: "timestamp"})
                break
            except Exception:
                continue

    if "timestamp" not in df.columns:
        raise ValueError("Could not find/parse a timestamp column in CSV.")

    # ensure sorting by time
    df = df.sort_values("timestamp").reset_index(drop=True)

    # price column heuristics
    price_cols = [c for c in df.columns if c.lower() in ("price", "last", "px", "tick")]
    if price_cols:
        price_col = price_cols[0]
        df = df.rename(columns={price_col: "price"})
    if "price" not in df.columns:
        raise ValueError("Could not find a price column in CSV (searched price,last,px,tick).")

    # ensure correct dtypes
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    if "size" in df.columns:
        df["size"] = pd.to_numeric(df["size"], errors="coerce")

    logger.info("Loaded %d rows, time range: %s to %s", len(df), df["timestamp"].min(), df["timestamp"].max())
    return df

def save_results(df, path):
    """Save DataFrame (or object convertible to CSV) to path."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if hasattr(df, "to_csv"):
        df.to_csv(p, index=False)
    else:
        # fallback for strings or bytes
        with open(p, "w", encoding="utf-8") as f:
            f.write(str(df))
    logger.info("Saved results to %s", p)
