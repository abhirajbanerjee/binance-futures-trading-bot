"""Configure logging for the trading bot."""

import logging
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent / "trading_bot.log"
LOG_FORMAT = "%(asctime)s | %(levelname)-5s | %(module)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level: int = logging.DEBUG) -> None:
    """Set up console (INFO) and file (DEBUG) log handlers."""
    root = logging.getLogger()
    root.setLevel(level)

    if root.handlers:
        return

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    root.addHandler(console)

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)
