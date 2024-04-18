import asyncio
import logging
import random
import pandas as pd
from typing import Tuple, Optional, Any, TypeAlias

from bot_management.core.logging_utils import setup_bot_logs, ContextualLogger
from bot_management.core.media import MediaContent
from bot_management.core.bots_base import AbstractBot
from bot_management.core.utils import auto_log
from bot_management.core.authenticator import AbstractAuthenticator
from bot_management.core import LogType
from logger_config import logger, console
from dataclasses import dataclass, asdict

from social_media.bot_manager import BotManager

import threading
import time


@dataclass
class InstagramContent(MediaContent):
    reel: str = None  # Facebook specific attribute

    @classmethod
    def from_dataframe_row(cls, row: pd.Series) -> 'InstagramContent':
        """
        Overrides the factory method to include Facebook-specific data.
        """
        # Create an instance of the base class
        base_post = super().from_dataframe_row(row)
        # Convert the base class instance to a dictionary
        base_post_dict = asdict(base_post)
        # Now update the dictionary with subclass-specific fields
        base_post_dict.update({'reel': row.get('Reel', '')})
        # Create and return an instance of the subclass
        return cls(**base_post_dict)


class AuthenticatorInstagram(AbstractAuthenticator):
    def login(self):
        # Instagram-specific login logic
        print("Instagram login")
        self.token = "Instagram_token"

    def refresh_token(self):
        # Instagram-specific token refresh logic
        print("Instagram token refreshed")
        self.token = "new_Instagram_token"


@BotManager.register_bot(platform_name='instagram')
class InstagramBot(AbstractBot):
    platform_name = property(lambda self: "Instagram")

    def create_auth_manager(self, api_key, api_secret):
        return AuthenticatorInstagram(api_key, api_secret)

    def create_post_from_dataframe_row(self, row: pd.Series) -> InstagramContent:
        instagram_post = InstagramContent.from_dataframe_row(row)
        return instagram_post

    @auto_log
    async def post(self, post: InstagramContent) -> LogType:

        # Simulate the request operation
        logger.debug(f"Posting {post}...")

        # Simulated delay or network operation
        await asyncio.sleep(random.uniform(0.1, 0.3))

        # This is where you would include your request code
        # For demonstration, we assume it's successful

        # The return value will be picked up by the auto_log decorator
        return logging.DEBUG, "message", True
