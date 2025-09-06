import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
from pathlib import Path
from .config import OUT_PLOTS, OUT_RESULTS, OUT_REPORTS

logger = logging.getLogger(__name__)

def compute_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute summary performance metrics and return as single-row DataFrame.
    Metrics: total_return, cumulative_pnl, max_drawdown, sharpe (simple)
    """
    res = {}
    if "equity" not in df.columns:
        raise ValueError("DataFrame must contain 'equity' column for performance computation.")

    equity = df["equity"].fillna(method="ffill").fillna(0)
    if len(equity) < 2:
        res = {
            "total_return": 0.0,
            "cum_pnl": float(df.get("cum_pnl", pd.Series([0])).iloc[-1]),
            "max_drawdown": 0.0,
            "sharpe": 0.0
        }
        return pd.DataFrame([res])

    # total return (relative to first non-zero equity)
    start = equity.iloc[0] if equity.iloc[0] != 0 else (equity.replace(0, np.nan).dropna().iloc[0] if (equity != 0).any() else 0)
    end = equity.iloc[-1]
    res["total_return"] = (end - start) / (start if start != 0 else 1.0)
    res["cum_pnl"] = float(df.get("cum_pnl", pd.Series([0])).iloc[-1])

    # drawdown
    roll_max = equity.cummax()
    drawdown = (equity - roll_max) / roll_max.replace(0, np.nan)
    res["max_drawdown"] = float(drawdown.min()) if not drawdown.empty else 0.0

    # simple Sharpe: mean(return)/std(return). Use period returns from equity
    eq_ret = equity.pct_change().replace([np.inf, -np.inf], np.nan).fillna(0)
    if eq_ret.std() == 0:
        res["sharpe"] = 0.0
    else:
        res["sharpe"] = float(eq_ret.mean() / eq_ret.std())

    return pd.DataFrame([res])

def plot_equity(df: pd.DataFrame, filename: str = "equity_curve.png"):
    OUT_PLOTS.mkdir(parents=True, exist_ok=True)
    path = OUT_PLOTS / filename
    fig, ax = plt.subplots(figsize=(8, 4))
    if "equity" in df.columns:
        df["equity"].plot(ax=ax)
        ax.set_title("Equity Curve")
        ax.set_ylabel("Equity")
        ax.grid(True)
    else:
        ax.text(0.5, 0.5, "No equity data", ha="center")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved plot to %s", path)
    return path

def save_report_text(summary_df: pd.DataFrame, perf_df: pd.DataFrame, filename: str = "report.md"):
    OUT_REPORTS.mkdir(parents=True, exist_ok=True)
    path = OUT_REPORTS / filename
    lines = []
    lines.append("# Backtest Report\n")
    lines.append("## Performance Summary\n")
    lines.append(perf_df.to_markdown(index=False))
    lines.append("\n## Backtest Result Head (sample)\n")
    lines.append(summary_df.head().to_markdown())
    path.write_text("\n\n".join(lines), encoding="utf-8")
    logger.info("Saved report to %s", path)
    return path
