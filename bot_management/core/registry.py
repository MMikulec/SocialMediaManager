# bot_management/core/registry.py
import importlib
from pathlib import Path
from typing import Dict, Type
from bot_management.core.bots_base import BotProtocol


class BotRegistry:
    def __init__(self):
        self._bot_classes: Dict[str, Type[BotProtocol]] = {}
        self._load_all_bots()

    @property
    def bot_classes(self) -> Dict[str, Type[BotProtocol]]:
        return self._bot_classes

    def register_bot(self, platform_name):
        def decorator(bot_cls):
            self._bot_classes[platform_name.lower()] = bot_cls
            return bot_cls
        return decorator

    def get_bot_class(self, platform_name: str) -> Type[BotProtocol]:
        return self._bot_classes.get(platform_name.lower(), None)

    def _load_all_bots(self):
        """Private method to load all bot classes from the bots directory."""
        bots_dir = Path(__file__).resolve().parent.parent / 'bots'  # Adjust path as necessary
        for file in bots_dir.iterdir():
            if file.is_file() and file.suffix == '.py' and file.name != '__init__.py':
                module_name = file.stem
                module = importlib.import_module(f'bot_management.bots.{module_name}')
                class_name = module_name.capitalize() + 'Bot'
                bot_class = getattr(module, class_name, None)
                if bot_class and issubclass(bot_class, BotProtocol):
                    self.register_bot(module_name)(bot_class)
