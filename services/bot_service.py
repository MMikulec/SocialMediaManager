# bot_management/bot_service.py
from typing import Optional, Tuple, Dict
from data_management.data_holder import DataHolder
from bot_management.core.registry import BotRegistry
from bot_management.core.bots_base import BotProtocol
from logger_config import logger
from data_management.auth_manager.auth_manager import AuthManager
from data_management.auth_manager.auth_manager_base import AuthManagerProtocol


class BotService:
    def __init__(self, data_holder: DataHolder):
        self.data_holder = data_holder
        self.source = data_holder.data_source
        self.credential_source = data_holder.credential_source

        self.bot_registry = BotRegistry()  # One instance of BotRegistry per BotService
        self.bot_instances: Dict[Tuple[str, str], BotProtocol] = {}

        self.auth_strategy = self.get_auth_strategy()

        logger.debug(f"Loading platform post classes from\n{self.bot_registry.bot_classes}")

    def get_auth_strategy(self) -> AuthManagerProtocol:
        """
        Creates an AuthManager instance, determines the type of credentials source,
        and retrieves the appropriate authentication strategy.

        :return: An instance of the relevant AuthStrategy class.
        """
        auth_manager = AuthManager()
        credentials_type = self.data_holder.check_credentials_source(self.credential_source)

        strategy_instance = auth_manager.get_strategy_instance(credentials_type, self.credential_source)
        if not strategy_instance:
            raise ValueError(f"No strategy found for credentials type: {credentials_type}")
        return strategy_instance

    def load_bot(self, user_name: str, platform_name: str) -> Optional[BotProtocol]:
        platform_name = platform_name.lower()
        bot_class = self.bot_registry.get_bot_class(platform_name)

        if not bot_class:
            logger.error(f"No bot class found for platform: {platform_name}")
            return None

        # Use credentials to instantiate the bot correctly
        user_credentials = self.auth_strategy.get_credentials(platform_name, user_name)

        if not user_credentials:
            logger.error(f"No credentials found for user {user_name} on platform {platform_name}")
            return None

        # Adjusted to key instances by both platform and user
        key = (platform_name, user_name.lower())
        if key not in self.bot_instances:
            try:
                bot_instance = bot_class(user_name, self.source, user_credentials)
                self.bot_instances[key] = bot_instance
                logger.debug(f"Created new instance of {bot_class.__name__} for user {user_name} on platform {platform_name}.")
            except Exception as e:
                logger.error(f"Error instantiating bot for platform {platform_name} and user {user_name}: {e}")
                return None

        return self.bot_instances[key]