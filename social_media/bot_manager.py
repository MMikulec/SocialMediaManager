import os
import importlib
from typing import Dict, Type, Optional
from pathlib import Path
from bot_manager.bot_core.bots import SocialMediaProtocol, SocialMediaPost  # Import the protocol and post class
from logger_config import logger, console


class BotManager:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.bot_instances: Dict[str, SocialMediaProtocol] = {}
        self.platform_classes = self.load_platform_post_classes()

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

    def load_bot(self, platform_name: str) -> Optional[SocialMediaProtocol]:
        platform_name = platform_name.lower()  # Normalize to lowercase
        if platform_name not in self.bot_instances:
            bot_class = self.platform_classes.get(platform_name)

            if not bot_class:
                # Attempt to reload the platform classes if bot not found
                self.refresh_platform_classes()
                bot_class = self.platform_classes.get(platform_name)

            if bot_class:
                try:
                    bot_instance = bot_class(self.file_path.name)  # Instantiate the bot class
                    self.bot_instances[platform_name] = bot_instance
                    logger.info(f"Created new instance of {bot_class.__name__}.")
                    return bot_instance
                except Exception as e:
                    logger.error(f"Error instantiating bot for platform {platform_name}: {e}")
            else:
                logger.error(f"No bot class found for platform: {platform_name}")

        return self.bot_instances.get(platform_name)
