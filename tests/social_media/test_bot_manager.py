#  Copyright (c) 2024.
import pytest
from pathlib import Path
import pandas as pd
from social_media.bot_manager import BotManager  # Assuming BotManager is in this location
from bot_manager.bot_core.bots import SocialMediaProtocol, SocialMediaPost  # Adjust if necessary
from data_management.data_holder import DataHolder
from datetime import datetime, timedelta


def test_bot_loading():
    """
    Test if BotManager correctly loads and instantiates bots based on platform names.
    """
    # Initialize the BotManager
    df = pd.DataFrame({
        'Post ID': [1, 2, 3],
        'Platform': ['Instagram', 'Facebook', 'Instagram'],
        'Content': ['Check out our new product', 'New product launch', 'Product giveaway'],
        'Image Path': ['img1', 'img1', 'img1'],
        'Hashtags': ['#new #tech #insta', '#new #tech #fcbk', '#new #tech #insta'],
        'Scheduled Time': [datetime.now() + timedelta(days=1), datetime.now(), datetime.now() - timedelta(days=1)],
        'Status': ['Scheduled', 'Scheduled', 'Posted'],
        'Remarks': ['', '', '']
    })

    bot_manager = BotManager(DataHolder(df, "plan_post.xlsx", "plan_post.json"))

    # Attempt to load a bot for a specific platform, adjust 'facebook' as necessary
    bot_instance = bot_manager.load_bot("default", 'facebook')
    bot_instance2 = bot_manager.load_bot("default", 'facebook')
    bot_instance3 = bot_manager.load_bot("name", 'facebook')

    assert bot_instance is bot_instance2
    assert bot_instance is not bot_instance3
    # Check if the bot_instance is not None and is an instance of the correct protocol
    assert bot_instance is not None, "Bot instance should not be None"
    assert isinstance(bot_instance, SocialMediaProtocol), "Bot instance should implement SocialMediaProtocol"


def test_bots_loading():
    """
    Test if BotManager correctly loads and instantiates bots based on platform names.
    """


    # Initialize the BotManager
    # Initialize the BotManager
    df = pd.DataFrame({
        'Post ID': [1, 2, 3],
        'Platform': ['Instagram', 'Facebook', 'Instagram'],
        'Content': ['Check out our new product', 'New product launch', 'Product giveaway'],
        'Image Path': ['img1', 'img1', 'img1'],
        'Hashtags': ['#new #tech #insta', '#new #tech #fcbk', '#new #tech #insta'],
        'Scheduled Time': [datetime.now() + timedelta(days=1), datetime.now(), datetime.now() - timedelta(days=1)],
        'Status': ['Scheduled', 'Scheduled', 'Posted'],
        'Remarks': ['', '', '']
    })

    bot_manager = BotManager(DataHolder(df, "plan_post.xlsx", "plan_post.json"))
    bot_manager2 = BotManager(DataHolder(df, "plan_post2.xlsx", "plan_post.json"))
    bot_manager3 = BotManager(DataHolder(df, "plan_post3.xlsx", "plan_post.json"))

    # Attempt to load a bot for a specific platform, adjust 'facebook' as necessary
    bot_instance = bot_manager.load_bot("default", 'facebook')
    bot_instance2 = bot_manager2.load_bot("default", 'facebook')
    bot_instance3 = bot_manager3.load_bot("name", 'facebook')

    assert bot_instance is bot_instance2
    assert bot_instance is not bot_instance3
    # Check if the bot_instance is not None and is an instance of the correct protocol
    assert bot_instance is not None, "Bot instance should not be None"
    assert isinstance(bot_instance, SocialMediaProtocol), "Bot instance should implement SocialMediaProtocol"
