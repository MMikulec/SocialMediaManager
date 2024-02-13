from abc import ABC, abstractmethod

from post_manager.bot_core.singleton import SingletonMeta


class AuthManager(ABC, metaclass=SingletonMeta):
    """
    Abstract base class for authentication management with social media APIs.

    Attributes:
        api_key (str): API key for the social media platform.
        api_secret (str): API secret for secure authentication.
        token (str): Authenticated token obtained after login.
    """

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.token = None

    @abstractmethod
    def login(self):
        """Performs the login operation to authenticate with the social media platform."""
        pass

    @abstractmethod
    def refresh_token(self):
        """Refreshes the authentication token if it has expired or needs renewal."""
        pass
