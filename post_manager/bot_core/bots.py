import logging
import pandas as pd
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

from post_manager.bot_core import LogType
from post_manager.bot_core.auth import AuthManager
from post_manager.bot_core.logging_utils import setup_bot_logs, ContextualLogger, LoggerSingleton
from post_manager.bot_core.posts import SocialMediaPost
from post_manager.bot_core.singleton import SingletonMeta


@runtime_checkable
class SocialMediaProtocol(Protocol):
    """
    A protocol for social media bots. Implementing classes are expected to accept
    an 'excel_file_name' parameter in their constructor for initializing with a specific Excel file.
    """

    def __init__(self, excel_file_name: str):
        self.excel_file_name = excel_file_name

    def post(self, post: SocialMediaPost) -> LogType: ...

    def create_post_from_dataframe_row(self, row: pd.Series) -> SocialMediaPost: ...


class SocialMediaBot(ABC, metaclass=SingletonMeta):
    """
    Abstract base class for social media bots responsible for posting content.

    Attributes:
        logs (ContextualLogger): Logger for recording bot activities, configured per bot instance.
        auth_manager (post_manager.bot_core.auth.AuthManager): Authentication manager instance for handling API authentication.
    """

    def __init__(self, excel_file_name):
        """
        Initializes the social media bot with a specific Excel file context.

        Args:
            excel_file_name (str): The name of the Excel file used for sourcing post data.
        """
        """base_logger = setup_bot_logs(excel_file_name)
        self.logs = ContextualLogger(base_logger,
                                     {'excel_file': excel_file_name, 'platform_name': self.platform_name})"""
        self.logs = LoggerSingleton.get_logger(excel_file_name, self.platform_name)
        self.auth_manager = self.create_auth_manager(api_key="your_api_key", api_secret="your_api_secret")
        self.excel_file_name = excel_file_name

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """
        Abstract property that returns the platform name as a string. Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def create_auth_manager(self, api_key: str, api_secret: str) -> AuthManager:
        """
        Factory method to create an AuthManager instance specific to the social media platform.

        Args:
            api_key (str): API key for the social media platform.
            api_secret (str): API secret for secure authentication.

        Returns:
            AuthManager: An instance of AuthManager for handling authentication.
        """
        pass

    @abstractmethod
    def create_post_from_dataframe_row(self, row: pd.Series) -> SocialMediaPost:
        pass

    @abstractmethod
    def post(self, post: SocialMediaPost) -> LogType:
        """
        Abstract method for posting content to the social media platform. Must be implemented by subclasses.

        Args:
            post (SocialMediaPost): The post object containing content to be shared.
        """
        pass

    def log_post(self, post: SocialMediaPost, level, message, data=None):
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
