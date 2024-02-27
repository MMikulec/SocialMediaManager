#  Copyright (c) 2024.
import pytest
from scheduler.social_media.bot_manager import BotManager  # Assuming BotManager is in this location
from post_manager.bot_core.bots import SocialMediaProtocol, SocialMediaPost  # Adjust if necessary


def test_load_platform_post_classes():
    assert False


# test_bot_manager.py

def test_bot_loading():
    """
    Test if BotManager correctly loads and instantiates bots based on platform names.
    """
    # Initialize the BotManager
    bot_manager = BotManager("plan.xlsx")

    # Attempt to load a bot for a specific platform, adjust 'facebook' as necessary
    bot_instance = bot_manager.load_bot('facebook')

    # Check if the bot_instance is not None and is an instance of the correct protocol
    assert bot_instance is not None, "Bot instance should not be None"
    assert isinstance(bot_instance, SocialMediaProtocol), "Bot instance should implement SocialMediaProtocol"
