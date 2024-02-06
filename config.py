import logging

LOGGING_CONFIG = {
    # Set the minimum logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    "terminal_log_level": logging.DEBUG,  # recommended INFO
    "bots_log_level": logging.DEBUG,  # minimum INFO for correct functioning

    # TODO: Marek: Setting for directories. Not working yet.
    "terminal_logs_directory": "",
    "bots_logs_directory": 'post_manager/logs'
}
