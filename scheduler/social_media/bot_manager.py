import importlib


class BotManager:
    def __init__(self, bots_directory: str):
        self.bots_directory = bots_directory

    def load_bot(self, platform_name: str):
        """Dynamically loads a bot based on the platform name."""
        try:
            # Assuming bot class names follow a consistent naming convention
            class_name = platform_name.capitalize() + 'Bot'
            module_path = f"{self.bots_directory}.{platform_name.lower()}"
            module = importlib.import_module(module_path)
            bot_class = getattr(module, class_name)
            return bot_class()  # Instantiate the bot class
        except (ImportError, AttributeError) as e:
            # Handle error (e.g., log it, raise an exception)
            pass
