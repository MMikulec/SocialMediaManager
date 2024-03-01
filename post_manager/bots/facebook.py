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

request_lock = threading.Lock()


@dataclass
class FacebookPost(SocialMediaPost):
    video: str = None  # Facebook specific attribute

    @classmethod
    def from_dataframe_row(cls, row: pd.Series) -> 'FacebookPost':
        """
        Overrides the factory method to include Facebook-specific data.
        """
        # Create an instance of the base class
        base_post = super().from_dataframe_row(row)
        # Convert the base class instance to a dictionary
        base_post_dict = asdict(base_post)
        # Now update the dictionary with subclass-specific fields
        base_post_dict.update({'video': row.get('Video', '')})
        # Create and return an instance of the subclass
        return cls(**base_post_dict)


class AuthManagerFacebook(AuthManager):
    def login(self):
        # Facebook-specific login logic
        print("Facebook login")
        self.token = "facebook_token"

    def refresh_token(self):
        # Facebook-specific token refresh logic
        print("Facebook token refreshed")
        self.token = "new_facebook_token"


class FacebookBot(SocialMediaBot):
    platform_name = property(lambda self: "Facebook")

    def create_auth_manager(self, api_key, api_secret):
        return AuthManagerFacebook(api_key, api_secret)

    def create_post_from_dataframe_row(self, row: pd.Series) -> FacebookPost:
        facebook_post = FacebookPost.from_dataframe_row(row)
        return facebook_post

    @auto_log
    async def post(self, post: FacebookPost) -> LogType:
        with request_lock:
            # Simulate the request operation
            print(f"Posting {post}...")

            # Simulated delay or network operation
            await asyncio.sleep(random.uniform(0.1, 0.3))

            # This is where you would include your request code
            # For demonstration, we assume it's successful

        # The return value will be picked up by the auto_log decorator
        return logging.DEBUG, "message", True

    @auto_log
    def test(self):
        return logging.DEBUG, "test", True