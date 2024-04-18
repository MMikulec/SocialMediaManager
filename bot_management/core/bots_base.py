import logging
import pandas as pd
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

from logger_config import logger, console
from bot_management.core import LogType
from bot_management.core.authenticator import AbstractAuthenticator
from bot_management.core.logging_utils import setup_bot_logs, ContextualLogger, LoggerSingleton
from bot_management.core.media import MediaContent
from bot_management.core.singleton import SingletonMeta, UserBasedSingletonMeta


@runtime_checkable
class BotProtocol(Protocol):
    """
    A protocol for social media bots. Implementing classes are expected to accept
    an 'source_name' parameter in their constructor for initializing with a specific source file.
    """

    def __init__(self, user_name: str, source_name: str, credentials: dict):
        self.user_name = user_name
        self.source_name = source_name
        self.credentials = credentials

    def post(self, post: MediaContent) -> LogType: ...

    def create_post_from_dataframe_row(self, row: pd.Series) -> MediaContent: ...


class AbstractBot(ABC, metaclass=UserBasedSingletonMeta):
    """
    Abstract base class for social media bots responsible for posting content.

    Attributes:
        logs (ContextualLogger): Logger for recording bot activities, configured per bot instance.
        auth_manager (bot_manager.core.authenticator.AbstractAuthenticator): Authentication manager instance for handling API authentication.
    """

    def __init__(self, user_name, source_name: str, credentials: dict):
        """
        Initializes the social media bot with a specific source file context.

        :param source_name: The name of the source file used for sourcing post data.
        """
        """base_logger = setup_bot_logs(source_name)
        self.logs = ContextualLogger(base_logger,
                                     {'excel_file': source_name, 'platform_name': self.platform_name})"""
        self.user_name = user_name
        self.source_name = source_name
        self.credentials = credentials
        logger.debug(f"Initializing social media bot with "
                     f"user_name: {self.user_name} "
                     f"source_name: {self.source_name} "
                     f"credentials: {self.credentials}")

        self.logs = LoggerSingleton.get_logger(self.source_name, self.platform_name)
        self.auth_manager = self.create_auth_manager(api_key="your_api_key", api_secret="your_api_secret")


    @property
    @abstractmethod
    def platform_name(self) -> str:
        """
        Abstract property that returns the platform name as a string. Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def create_auth_manager(self, api_key: str, api_secret: str) -> AbstractAuthenticator:
        """
        Factory method to create an AuthManager instance specific to the social media platform.

        Args:
            api_key (str): API key for the social media platform.
            api_secret (str): API secret for secure authentication.

        Returns:
            AbstractAuthenticator: An instance of AuthManager for handling authentication.
        """
        pass

    @abstractmethod
    def create_post_from_dataframe_row(self, row: pd.Series) -> MediaContent:
        pass

    @abstractmethod
    def post(self, post: MediaContent) -> LogType:
        """
        Abstract method for posting content to the social media platform. Must be implemented by subclasses.

        Args:
            post (MediaContent): The post object containing content to be shared.
        """
        pass

    def log_post(self, post: MediaContent, level, message, data=None):
        """
        Logs actions related to a social media post, incorporating the post's ID into the logging context for
        enhanced traceability.

        :param post: The social media post object that is central to the log entry. This object's ID is used to
        update the logging context for improved specificity.
        :param level: The severity level of the log,
        corresponding to standard logging levels (e.g., logging.INFO, logging.ERROR), which dictates how the log is
        processed and filtered.
        :param message: A descriptive message detailing the nature of the log entry.
        :param data: Additional data or context that might be relevant to the log entry, provided as a dictionary.
        Optional.
        :return: None. This method updates the logging context and performs logging without returning any value.

        This method updates the logging context to include the ID of the post being acted upon before logging the
        specified message. After logging, it cleans up by removing the post's ID from the context,
        ensuring subsequent logs are not incorrectly associated with this post.
        """
        if post:
            # Temporarily augment the logging context with the post's ID for this entry
            self.logs.update_context(post_id=post.post_id)

        # Perform the actual logging with the provided level and message
        self.logs.log(level, message)

        if post:
            # Ensure the context is cleared of the post's ID after logging to maintain accuracy
            self.logs.update_context(post_id=None)

    def log_action(self, level, message, data=None):
        # Convert string level to logging constants if necessary
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)

        # Combine message and data if data is present
        combined_message = message + (f" | Additional data: {data}" if data else "")

        # Log the combined message at the specified level
        self.logs.log(level, combined_message)
