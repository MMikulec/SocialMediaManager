"""import asyncio
import inspect
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
            # with logging_lock:
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
            # with logging_lock:
            if callable(self.log_action):
                self.log_action(level=logging.ERROR, message=f"Exception in '{action}': {str(e)}", data=None)
            else:
                # This is a fallback safety net and should ideally never be reached
                logger.critical(f"Critical: log_action method not callable. Exception in '{action}': {str(e)}")

        return result

    return wrapper
"""

import asyncio
import inspect
import logging
from functools import wraps

from logger_config import logger

def auto_log(func):
    @wraps(func)
    async def async_wrapper(self, *args, **kwargs):
        action = func.__name__
        # Safely attempt to find a specific logging method or use log_action as a fallback
        log_method = getattr(self, f"log_{action}", self.log_action)
        # Initialize result in case it's referenced before being assigned
        result = None

        try:
            # Await the function if it's an async function
            if asyncio.iscoroutinefunction(log_method):
                result = await func(self, *args, **kwargs)
            else:
                result = func(self, *args, **kwargs)

            level = logging.INFO
            message = "Function executed without a message"
            data = None

            if isinstance(result, tuple):
                level, message = result[:2]
                data = result[2] if len(result) > 2 else None

                # Prepare logging arguments
            log_kwargs = {'level': level, 'message': message, 'data': data, **kwargs}

            # Acquire the logging lock before performing any logging action
            # with logging_lock:
            # Check if log_method is callable to avoid 'not callable' warning

            if callable(log_method):
                if asyncio.iscoroutinefunction(log_method):
                    await log_method(*args, **log_kwargs)
                else:
                    log_method(*args, **log_kwargs)
        except Exception as e:
            if callable(self.log_action):
                await self.log_action(level=logging.ERROR, message=f"Exception in '{action}': {str(e)}", data=None) if asyncio.iscoroutinefunction(self.log_action) else self.log_action(level=logging.ERROR, message=f"Exception in '{action}': {str(e)}", data=None)
            else:
                logger.error(f"Critical: log_action method not callable. Exception in '{action}': {str(e)}")
        return result

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if inspect.iscoroutinefunction(func):
            # If the original function is asynchronous, return the coroutine object
            return async_wrapper(self, *args, **kwargs)
        else:
            # If the original function is synchronous, schedule the coroutine to be run in the event loop
            return asyncio.run(async_wrapper(self, *args, **kwargs))

    return wrapper

