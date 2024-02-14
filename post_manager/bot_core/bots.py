import logging
from abc import ABC, abstractmethod
from typing import Protocol

from post_manager.bot_core import LogType
from post_manager.bot_core.auth import AuthManager
from post_manager.bot_core.logging_utils import setup_bot_logs, ContextualLogger
from post_manager.bot_core.posts import SocialMediaPost
from post_manager.bot_core.singleton import SingletonMeta


class SocialMediaProtocol(Protocol):
    def post(self, post: SocialMediaPost) -> LogType: ...


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
        base_logger = setup_bot_logs(excel_file_name)
        self.logs = ContextualLogger(base_logger,
                                     {'excel_file': excel_file_name, 'platform_name': self.platform_name})
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
    def post(self, post: SocialMediaPost) -> LogType:
        """
        Abstract method for posting content to the social media platform. Must be implemented by subclasses.

        Args:
            post (SocialMediaPost): The post object containing content to be shared.
        """
        pass

    def log_post_(self, post: SocialMediaPost, action: str, success: bool, error: str = ''):
        """
        Logs actions taken on a post, dynamically including the post's ID in the log message.

        Args:
            post (SocialMediaPost): The post object.
            action (str): Description of the action being logged (e.g., 'Posting', 'Deleting').
            success (bool): Whether the action was successful.
            error (str, optional): Error message if the action failed.
        """
        # Update the logs context to include this post's ID
        self.logs.update_context(post_id=post.post_id)

        if success:
            self.logs.info(f"{action} to {self.platform_name} succeeded.")
        else:
            self.logs.error(f"{action} to {self.platform_name} failed. Error: {error}")

        # Optionally reset the post_id in the context if you don't want it to persist
        self.logs.update_context(post_id=None)

    def log_action_(self, action: str, *args, success: bool, error: str = ''):
        """
        Generic method for logging various actions.

        Args:
            action (str): The name of the action (typically the method name).
            *args: Arguments passed to the action method (can be used to extract additional context).
            success (bool): Whether the action was successful.
            error (str, optional): Error message if the action failed.
        """
        # Example logging logic
        if success:
            self.logs.info(f"{action} succeeded.")
        else:
            self.logs.error(f"{action} failed. Error: {error}")

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

        # Log the message at the specified level
        self.logs.log(level, message)

        # Log additional data at DEBUG level, if present
        if data:
            self.logs.debug(f"Additional data: {data}")
