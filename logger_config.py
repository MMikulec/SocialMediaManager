# logger_config.py

import logging
from rich.logging import RichHandler
from rich.console import Console
from config import LOGGING_CONFIG


# Setup logging using Rich
def setup_logger():
    logging.basicConfig(
        level=LOGGING_CONFIG["terminal_log_level"],
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

    logger = logging.getLogger("rich")
    return logger


# Initialize and export the logs
logger = setup_logger()

# Initialize Rich console
console = Console()
