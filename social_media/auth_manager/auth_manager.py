# social_media/auth_manager/auth_manager.py
import importlib
from pathlib import Path
from social_media.auth_manager.auth_manager_base import AbstractAuthManager


class AuthManager:
    _auth_strategies = {}  # Class-level registry for auth strategies

    def __init__(self):
        self.load_builtin_strategies()  # Ensure strategies are loaded and registered

    @classmethod
    def register_auth_strategy(cls, name):
        def decorator(strategy_cls):
            if not issubclass(strategy_cls, AbstractAuthManager):
                raise TypeError(f"Strategy {strategy_cls.__name__} must inherit from AbstractAuthManager")
            cls._auth_strategies[name] = strategy_cls
            return strategy_cls
        return decorator

    @classmethod
    def load_builtin_strategies(cls):
        """Dynamically load all auth strategies defined in the strategies folder."""
        strategies_dir = Path(__file__).parent / 'strategies'
        for file in strategies_dir.glob('*.py'):
            if file.name not in ["__init__.py"]:
                module_path = f"social_media.auth_manager.strategies.{file.stem}"
                importlib.import_module(module_path)
        # No need to manually fill _auth_strategies here, as strategies register themselves via decorator

    @classmethod
    def get_strategy_instance(cls, strategy_name: str, *args, **kwargs):
        """Instantiate and return an auth strategy instance by its name."""
        strategy_class = cls._auth_strategies.get(strategy_name)
        if not strategy_class:
            raise ValueError(f"No authentication strategy found for name: {strategy_name}")
        return strategy_class(*args, **kwargs)
