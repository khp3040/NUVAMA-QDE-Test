from typing import Tuple
import pandas as pd
import numpy as np
import logging
from .config import RESAMPLE_RULE, STRAT

logger = logging.getLogger(__name__)

def resample_ticks_to_ohlc(df: pd.DataFrame, rule: str = RESAMPLE_RULE) -> pd.DataFrame:
    """
    Resample tick DataFrame (timestamp, price, optional size) into OHLC at `rule` frequency.
    Returns DataFrame indexed by timestamp (period end).
    """
    if "timestamp" not in df.columns or "price" not in df.columns:
        raise ValueError("df must contain 'timestamp' and 'price' columns")

    df_ts = df.set_index("timestamp")
    ohlc = df_ts["price"].resample(rule).agg(["first", "max", "min", "last"])
    ohlc = ohlc.rename(columns={"first": "open", "max": "high", "min": "low", "last": "close"})
    # forward-fill missing prices if there are NaNs
    ohlc["close"] = ohlc["close"].ffill()
    ohlc["open"] = ohlc["open"].fillna(ohlc["close"])
    ohlc["high"] = ohlc["high"].fillna(ohlc["close"])
    ohlc["low"] = ohlc["low"].fillna(ohlc["close"])
    ohlc = ohlc.dropna(how="all")
    logger.info("Resampled ticks to %s OHLC rows: %d", rule, len(ohlc))
    return ohlc

def run_simple_mean_reversion(ohlc: pd.DataFrame, ma_window: int = None, threshold_pct: float = None, position_size: int = None) -> pd.DataFrame:
    """
    Simple mean-reversion strategy:
      - compute moving average on close
      - if close < ma * (1 - threshold) => go LONG position_size
      - if close > ma * (1 + threshold) => exit (flat)
    Produces a DataFrame with columns: open, high, low, close, ma, signal, position, returns, pnl, eq
    """
    ma_window = STRAT["ma_window"] if ma_window is None else ma_window
    threshold_pct = STRAT["threshold_pct"] if threshold_pct is None else threshold_pct
    position_size = STRAT["position_size"] if position_size is None else position_size

    df = ohlc.copy()
    df["ma"] = df["close"].rolling(window=ma_window, min_periods=1).mean()
    # signals: 1 means long, 0 flat
    df["signal"] = 0
    entry_cond = df["close"] < df["ma"] * (1 - threshold_pct)
    exit_cond = df["close"] > df["ma"] * (1 + threshold_pct)
    # simple logic: if entry_cond then 1 else if exit_cond then 0 else carry previous
    pos = 0
    positions = []
    for i in range(len(df)):
        if entry_cond.iloc[i]:
            pos = 1
        elif exit_cond.iloc[i]:
            pos = 0
        positions.append(pos)
    df["signal"] = positions
    # position in shares
    df["position"] = df["signal"] * position_size

    # compute returns (pct change on close)
    df["close_prev"] = df["close"].shift(1)
    df["price_ret"] = df["close"].pct_change().fillna(0)
    # strategy pnl approx = position_prev * price change
    df["position_prev"] = df["position"].shift(1).fillna(0)
    df["pnl"] = df["position_prev"] * (df["close"] - df["close_prev"])
    # cash and equity tracking
    df["cash_change"] = - (df["position"] - df["position_prev"]) * df["close"]  # cash spent to change position
    df["cash"] = df["cash_change"].cumsum().fillna(0)
    df["market_value"] = df["position"] * df["close"]
    df["equity"] = df["cash"] + df["market_value"]
    df["cum_pnl"] = df["pnl"].cumsum().fillna(0)

    # clean up helper cols
    df = df.drop(columns=["close_prev"])
    logger.info("Strategy run complete. Final equity: %s", df["equity"].iloc[-1] if len(df) else "N/A")
    return df
