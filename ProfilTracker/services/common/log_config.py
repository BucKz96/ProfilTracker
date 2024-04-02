import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import datetime


def setup_logging(service_name):
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.INFO)

    log_dir = Path(__file__).resolve().parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"{service_name}_{timestamp}.log"
    log_file_path = log_dir / log_filename

    handler = RotatingFileHandler(
        str(log_file_path), maxBytes=10000000, backupCount=5
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
