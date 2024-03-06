import logging
import os
import threading

from typing import Dict, Any

from config import LOGGING_CONFIG
from logger_config import logger


def setup_bot_logs(excel_file_name):
    """Set up a logs for a specific Excel file."""
    logs_dir = 'post_manager/logs'
    excel_base_name = os.path.splitext(os.path.basename(excel_file_name))[0]
    log_file = f'{logs_dir}/{excel_base_name}_posts.log'

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    logs = logging.getLogger(excel_base_name)
    logs.setLevel(LOGGING_CONFIG["bots_log_level"])
    logs.propagate = False

    # Check if the logs already has handlers
    if not logs.handlers:
        """file_handler = logging.FileHandler(log_file)
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logs.addHandler(file_handler)"""

        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()  # For console output

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)  # Using the same format for console output

        logs.addHandler(file_handler)
        logs.addHandler(console_handler)  # Add console handler

    return logs


class ContextualLogger(logging.LoggerAdapter):
    def process_(self, msg, kwargs):
        """
        Add extra logging

        :param msg:
        :param kwargs:
        :return:
        """
        return f'{self.extra["excel_file"]} - {self.extra["platform_name"]} - {msg}', kwargs

    def __init__(self, logs: logging.Logger, extra: Dict[str, Any]):
        """
        Initialize the ContextualLogger with a base logger and additional context.

        Args:
            logs (logging.Logger): The underlying logger to use.
            extra (Dict[str, Any]): A dictionary of additional context to include in log messages.
        """
        # Explicitly call the superclass initializer
        super().__init__(logs, extra)
        # Ensure self.extra is a dictionary; this line might be redundant but clarifies the type
        self.extra: Dict[str, Any] = extra if isinstance(extra, dict) else {}

    def process(self, msg: str, kwargs: Dict[str, Any]) -> (str, Dict[str, Any]):
        """
        Process the logging message and keyword arguments.

        Args:
            msg (str): The log message.
            kwargs (Dict[str, Any]): Keyword arguments for the log message.

        Returns:
            Tuple[str, Dict[str, Any]]: The modified log message and keyword arguments.
        """
        excel_file = self.extra.get("excel_file")
        platform_name = self.extra.get("platform_name")

        # Check for missing 'excel_file' or 'platform_name' and log a debug message if any are missing
        if excel_file is None:
            logger.debug("ContextualLogger 'excel_file' is missing in logging context.")
        if platform_name is None:
            logger.debug("ContextualLogger 'platform_name' is missing in logging context.")

        prefix = f'{excel_file if excel_file is not None else "unknown"} - {platform_name if platform_name is not None else "unknown"}'

        if "post_id" in self.extra:
            prefix += f' - Post ID: {self.extra["post_id"]}'

        return f'{prefix} - {msg}', kwargs

    def update_context(self, **kwargs) -> None:
        """
        Update the logging context with new key-value pairs.

        Args:
            **kwargs: Arbitrary keyword arguments to add to or update the logging context.
        """
        self.extra.update(kwargs)


class LoggerSingleton:
    _instances = {}
    _lock = threading.Lock()  # Class-level lock

    @classmethod
    def get_logger(cls, excel_file_name, platform_name):
        key = (excel_file_name, platform_name)
        with cls._lock:  # Ensure thread-safe access and creation of loggers
            if key not in cls._instances:
                base_logger = setup_bot_logs(excel_file_name)
                contextual_logger = ContextualLogger(base_logger, {'excel_file': excel_file_name, 'platform_name': platform_name})
                cls._instances[key] = contextual_logger
            return cls._instances[key]
