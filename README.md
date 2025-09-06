# NUVAMA-QDE-Test
This repo is NUVAMA's - Quantitative Data Engineer – Take-Home Test

project_structure/
│── data/
│   └── sample_tick_data.csv
│── output/
│   ├── results/
│   ├── plots/
│   └── reports/
│── logs/
│   └── app.log   # will be created automatically
│── src/
│   ├── __init__.py
│   ├── io.py # Read the CSV data.
│   ├── engine.py
│   ├── analysis.py
│   ├── utils.py
│   ├── logging_config.py
│   └── main.py
│── requirements.txt
│── README_QuantDE_THT.md
│── README.md

**Brief summary**

__init__.py
    - Makes src/ a Python package.
    - Can hold version info or convenience imports, but usually left minimal.

io.py
    - Handles input/output operations.
    - Examples: load tick data from data/, save processed results to output/results/.
    - Keeps all file-handling code in one place.

engine.py
    - Core backtesting or strategy execution engine.
    - Implements logic to transform tick data → resampled OHLC → apply trading rules → compute PnL & positions.
    - Should be the “heart” of the system.

analysis.py
    - Handles analytics and risk reporting.
    - Examples: Sharpe ratio, drawdowns, stress tests, risk constraints.
    - Generates reports/plots for output/reports/ and output/plots/.

utils.py
    - General helper functions not specific to trading or analysis.
    - Example: ensure folder structure exists (make_dirs()), small math helpers, config utilities.
    - Keeps code DRY (don’t repeat yourself).

logging_config.py
    - Centralized logging setup.
    - Configures log formatting, console/file handlers, rotation.
    - Ensures everything logs consistently to logs/app.log.

main.py
    - The entry point for running the project.
    - Typical flow:
        -Create folders (utils.make_dirs)
        -Initialize logging (logging_config.configure_logging)
        -Load tick data (io.load_tick_data)
        -Run strategy (engine.run_strategy)
        -Analyze results (analysis.generate_report)
        -Save outputs (io.save_results, analysis.save_plot)

config.py
    - Centralizes the project-wide constants and defaults so the rest of the code can import a single source of truth (paths, resampling rule, strategy hyper-parameters). Changing values in config.py alters behavior across the pipeline without editing multiple files.


**Steps to run**
1.	Unzip to a folder or Forkthe git repo and take a git checkout.
e.g.
NUVAMA-QDE-Test.zip
2.	Create venv
e.g.
cd C:\Users\Kshitij Pawar\Documents\NUVAMA\NUVAMA-QDE-Test
python -m venv .venv
..venv\Scripts\Activate.ps1
3.	Install dependencies
e.g.
pip install -r requirements.txt
6.	Run the project
e.g.
python -m src.main