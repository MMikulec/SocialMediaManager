#  Copyright (c) 2024.
import pytest
from pathlib import Path
from social_media.bot_manager import BotManager  # Assuming BotManager is in this location
from bot_manager.bot_core.bots import SocialMediaProtocol, SocialMediaPost  # Adjust if necessary


def test_bot_loading():
    """
    Test if BotManager correctly loads and instantiates bots based on platform names.
    """
    # Initialize the BotManager
    bot_manager = BotManager(Path("plan.xlsx"))

    # Attempt to load a bot for a specific platform, adjust 'facebook' as necessary
    bot_instance = bot_manager.load_bot("default", 'facebook')
    bot_instance2 = bot_manager.load_bot("default", 'facebook')
    bot_instance3 = bot_manager.load_bot("name", 'facebook')

    assert bot_instance is bot_instance2
    assert bot_instance is not bot_instance3
    # Check if the bot_instance is not None and is an instance of the correct protocol
    assert bot_instance is not None, "Bot instance should not be None"
    assert isinstance(bot_instance, SocialMediaProtocol), "Bot instance should implement SocialMediaProtocol"
