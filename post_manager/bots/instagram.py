import asyncio
import logging
import random
import pandas as pd
from typing import Tuple, Optional, Any, TypeAlias

from post_manager.bot_core.logging_utils import setup_bot_logs, ContextualLogger
from post_manager.bot_core.posts import SocialMediaPost
from post_manager.bot_core.bots import SocialMediaBot
from post_manager.bot_core.utils import auto_log
from post_manager.bot_core.auth import AuthManager
from post_manager.bot_core import LogType
from logger_config import logger, console
from dataclasses import dataclass, asdict

import threading
import time


@dataclass
class InstagramPost(SocialMediaPost):
    reel: str = None  # Facebook specific attribute

    @classmethod
    def from_dataframe_row(cls, row: pd.Series) -> 'InstagramPost':
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


class AuthManagerInstagram(AuthManager):
    def login(self):
        # Instagram-specific login logic
        print("Instagram login")
        self.token = "Instagram_token"

    def refresh_token(self):
        # Instagram-specific token refresh logic
        print("Instagram token refreshed")
        self.token = "new_Instagram_token"


class InstagramBot(SocialMediaBot):
    platform_name = property(lambda self: "Instagram")

    def create_auth_manager(self, api_key, api_secret):
        return AuthManagerInstagram(api_key, api_secret)

    def create_post_from_dataframe_row(self, row: pd.Series) -> InstagramPost:
        instagram_post = InstagramPost.from_dataframe_row(row)
        return instagram_post

    @auto_log
    async def post(self, post: InstagramPost) -> LogType:

        # Simulate the request operation
        print(f"Posting {post}...")

        # Simulated delay or network operation
        await asyncio.sleep(random.uniform(0.1, 0.3))

        # This is where you would include your request code
        # For demonstration, we assume it's successful

        # The return value will be picked up by the auto_log decorator
        return logging.DEBUG, "message", True
