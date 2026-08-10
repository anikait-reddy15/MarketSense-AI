import logging
import sys
from utils.config import Config

def setup_logger(name: str = "MarketSenseAI") -> logging.Logger:
    """
    Configures and returns a standardized system logger instance.
    Outputs structured log messages to stdout and data/system.log file.
    """
    Config.ensure_directories()
    log_file_path = Config.DATA_DIR / "system.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent registering duplicate handlers if initialized repeatedly
    if logger.hasHandlers():
        return logger

    # Log Message Formatting
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler (Persistent Log File)
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger