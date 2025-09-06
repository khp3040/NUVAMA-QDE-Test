import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from .config import LOGS_DIR

def configure_logging(log_dir: Path = None, level=logging.INFO):
    """Configure root logger: console + rotating file handler."""
    if log_dir is None:
        log_dir = LOGS_DIR
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "app.log"

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-5s | %(name)s | %(message)s"
    ))

    # Rotating file handler
    file_handler = RotatingFileHandler(str(log_file), maxBytes=10*1024*1024, backupCount=3)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-5s | %(name)s | %(module)s:%(lineno)d | %(message)s"
    ))

    root = logging.getLogger()
    # avoid duplicate handlers on reconfigure
    if root.handlers:
        for h in list(root.handlers):
            root.removeHandler(h)

    root.setLevel(level)
    root.addHandler(console_handler)
    root.addHandler(file_handler)

    root.info("Logging initialized. Writing logs to %s", log_file)
