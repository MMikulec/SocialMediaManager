import logging
from functools import wraps

from logger_config import logger
import threading

# Create a global lock for logging
logging_lock = threading.Lock()


def auto_log(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        action = func.__name__
        # Safely attempt to find a specific logging method or use log_action as a fallback
        log_method = getattr(self, f"log_{action}", self.log_action)
        # Initialize result in case it's referenced before being assigned
        result = None

        try:
            result = func(self, *args, **kwargs)
            level = logging.INFO
            message = f"Function {action} without message"
            data = None

            if isinstance(result, tuple):
                level, message = result[:2]
                data = result[2] if len(result) > 2 else None

            # Prepare logging arguments
            log_kwargs = {'level': level, 'message': message, 'data': data, **kwargs}

            # Acquire the logging lock before performing any logging action
            with logging_lock:
                # Check if log_method is callable to avoid 'not callable' warning
                if callable(log_method):
                    # Combine args and kwargs for the original function with log_kwargs
                    log_method(*args, **log_kwargs)
                else:
                    # If log_method is somehow not callable, log a warning or error
                    self.logs.warning(f"Log method for action '{action}' is not callable.")

        except Exception as e:
            # Handle exceptions by logging them at the ERROR level
            # Acquire the logging lock before performing any logging action
            with logging_lock:
                if callable(self.log_action):
                    self.log_action(level=logging.ERROR, message=f"Exception in '{action}': {str(e)}", data=None)
                else:
                    # This is a fallback safety net and should ideally never be reached
                    logger.critical(f"Critical: log_action method not callable. Exception in '{action}': {str(e)}")

        return result

    return wrapper
