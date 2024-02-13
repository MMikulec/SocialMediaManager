from typing import Protocol

from post_manager.bot_core import LogType
from post_manager.bot_core.posts import SocialMediaPost


class SocialMediaProtocol(Protocol):
    def post(self, post: SocialMediaPost) -> LogType: ...
