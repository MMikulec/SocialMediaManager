import logging
from typing import Tuple, Optional, Any, TypeAlias

from post_manager.logger_config import ContextualLogger, setup_bot_logs
from post_manager.posts import SocialMediaPost, SocialMediaBot, AuthManager, auto_log, LogType
from logger_config import logger, console
from dataclasses import dataclass


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
        # return True or false
        return logging.DEBUG, "message", True
