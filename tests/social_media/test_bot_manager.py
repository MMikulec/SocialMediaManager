#  Copyright (c) 2024.
import json
import pandas as pd
from social_media.bot_manager import BotManager  # Assuming BotManager is in this location
from bot_management.core.bots_base import BotProtocol, MediaContent  # Adjust if necessary
from data_management.data_holder import DataHolder
from datetime import datetime, timedelta

# Sample data for use in tests
credentials_data = {
    "facebook": [{"user_name": "testuser1", "api_key": "testkey1"},
                 {"user_name": "testuser2", "api_key": "testkey2"}],
    "instagram": [{"user_name": "instauser", "access_token": "instatoken"}]
}

credentials_json = json.dumps(credentials_data)


def test_bots_loading(tmp_path):
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
        'User Name': ['testuser1', 'testuser1', 'testuser2'],
        'Remarks': ['', '', '']
    })

    credentials_file = tmp_path / "credentials.json"
    credentials_file.write_text(credentials_json)

    bot_manager = BotManager(DataHolder(df, "plan_post.xlsx", str(credentials_file)))
    bot_manager2 = BotManager(DataHolder(df, "plan_post2.xlsx", str(credentials_file)))
    bot_manager3 = BotManager(DataHolder(df, "plan_post3.xlsx", str(credentials_file)))

    # Attempt to load a bot for a specific platform, adjust 'facebook' as necessary
    bot_instance = bot_manager.load_bot("testuser1", 'facebook')
    bot_instance2 = bot_manager2.load_bot("testuser1", 'facebook')
    bot_instance3 = bot_manager3.load_bot("testuser2", 'facebook')

    assert bot_instance is bot_instance2
    assert bot_instance is not bot_instance3
    # Check if the bot_instance is not None and is an instance of the correct protocol
    assert bot_instance is not None, "Bot instance should not be None"
    assert isinstance(bot_instance, BotProtocol), "Bot instance should implement BotProtocol"
