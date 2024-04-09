import asyncio
import os
import importlib
from typing import Dict, Type, Optional, Tuple
from pathlib import Path
from bot_manager.bot_core.bots import SocialMediaProtocol, SocialMediaPost  # Import the protocol and post class
# from social_media.auth_manager import AuthManager
from logger_config import logger, console


class BotManager:
    # TODO: 5. 4. 2024: file_path to source
    def __init__(self, file_path: Path):
        self.file_path = file_path
        # self.auth_manager = AuthManager(file_path.with_suffix('.json'))
        self.bot_instances: Dict[Tuple[str, str], SocialMediaProtocol] = {}
        self.platform_classes = self.load_platform_post_classes()

        # Initialize AuthManager and load credentials
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(self.auth_manager.load_credentials())

        # logger.debug(f"Loading auth data from {self.auth_manager.credentials_file_path}")
        logger.debug(f"Loading platform post classes from {self.platform_classes}")
        # logger.debug(f"Loaded auth data: {self.auth_manager.credentials}")

    def load_platform_post_classes(self) -> Dict[str, Type[SocialMediaProtocol]]:
        platform_classes = {}
        # Assuming your bots.py file is in the correct location relative to this file
        bots_dir = Path(__file__).parent.parent / 'bot_manager' / 'bots'
        for file in bots_dir.iterdir():
            if file.is_file() and file.suffix == '.py' and file.name != '__init__.py':
                module_name = file.stem  # Extracts the file name without '.py'
                module = importlib.import_module(f'bot_manager.bots.{module_name}')
                class_name = module_name.capitalize() + 'Bot'  # Construct the class name based on file name
                bot_class = getattr(module, class_name, None)
                if bot_class and issubclass(bot_class, SocialMediaProtocol):
                    platform_classes[module_name.lower()] = bot_class
        return platform_classes

    def refresh_platform_classes(self):
        """Reloads the bot classes from the bots directory."""
        new_classes = self.load_platform_post_classes()
        self.platform_classes.update(new_classes)  # Update existing dictionary with any new entries

    def load_bot(self, user_name: str, platform_name: str) -> Optional[SocialMediaProtocol]:
        platform_name = platform_name.lower()  # Normalize to lowercase
        # Adjusted to create a tuple key of user_name and platform_name
        key = (user_name, platform_name)

        if key not in self.bot_instances:
            bot_class = self.platform_classes.get(platform_name)
            if not bot_class:
                self.refresh_platform_classes()
                bot_class = self.platform_classes.get(platform_name)
            if bot_class:
                try:
                    # Adjusted to pass user_name to the bot class constructor
                    bot_instance = bot_class(user_name, self.file_path.name)
                    self.bot_instances[key] = bot_instance
                    logger.debug(f"Created new instance of {bot_class.__name__} for user {user_name}.")
                    return bot_instance
                except Exception as e:
                    logger.error(f"Error instantiating bot for platform {platform_name} and user {user_name}: {e}")
            else:
                logger.error(f"No bot class found for platform: {platform_name}")
        return self.bot_instances.get(key)
