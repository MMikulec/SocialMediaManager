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

import threading

facebook_lock = threading.Lock()


@dataclass
class FacebookPost(SocialMediaPost):
    pass


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

    @auto_log
    def post(self, post: FacebookPost) -> LogType:
        with facebook_lock:
            print("Facebook post lock")
            # return True or false
            return logging.DEBUG, "message", True
