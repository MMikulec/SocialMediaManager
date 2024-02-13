import logging
from typing import Tuple, Optional, Any, TypeAlias

from post_manager.bot_core.logging_utils import setup_bot_logs, ContextualLogger
from post_manager.bot_core.posts import SocialMediaPost
from post_manager.bot_core.bots import SocialMediaBot
from post_manager.bot_core.utils import auto_log
from post_manager.bot_core.auth import AuthManager
from post_manager.bot_core import LogType
from logger_config import logger, console
from dataclasses import dataclass


@dataclass
class InstagramPost(SocialMediaPost):
    pass


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

    @auto_log
    def post(self, post: InstagramPost) -> LogType:
        # return True or false
        return logging.INFO, "message"
