"""
Entry point for the project.

Usage:
  python -m src.main
  or
  python src/main.py
"""
import sys
from pathlib import Path
import logging

# Make project root importable if running src/main.py directly
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils import make_dirs
from src.logging_config import configure_logging
from src.io import load_tick_data, save_results
from src.engine import resample_ticks_to_ohlc, run_simple_mean_reversion
from src.analysis import compute_performance, plot_equity, save_report_text
from src.config import DATA_DIR, OUT_RESULTS

def main():
    # setup
    make_dirs()
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info("=== Starting pipeline ===")

    try:
        # load data
        tick_file = DATA_DIR / "sample_tick_data.csv"
        df_ticks = load_tick_data(tick_file)

        # resample to OHLC
        ohlc = resample_ticks_to_ohlc(df_ticks)

        # run strategy
        strat_out = run_simple_mean_reversion(ohlc)

        # compute performance
        perf = compute_performance(strat_out)

        # save results
        OUT_RESULTS.mkdir(parents=True, exist_ok=True)
        results_path = OUT_RESULTS / "strategy_results.csv"
        save_results(strat_out.reset_index(), results_path)

        perf_path = OUT_RESULTS / "performance_summary.csv"
        save_results(perf, perf_path)

        # save plot
        plot_path = plot_equity(strat_out, filename="equity_curve.png")

        # save report
        report_path = save_report_text(strat_out, perf)

        logger.info("Pipeline finished. Results: %s, Perf: %s, Plot: %s, Report: %s",
                    results_path, perf_path, plot_path, report_path)
    except Exception as e:
        logger.exception("Pipeline failed: %s", e)
        raise

if __name__ == "__main__":
    main()
